import serial
import time
import pyttsx3
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException


SERIAL_PORT = 'COM3'  # Change this to your Arduino or Pico COM port
BAUD_RATE = 9600
CHROMEDRIVER_PATH = None  # Set to the ChromeDriver path if needed
HTML_FILE = 'file:///C:/Users/sguls/OneDrive/BEEST/Screamintoahole.html'
DEBOUNCE_SECONDS = 0.3

engine = pyttsx3.init()
recognizer = sr.Recognizer()

def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen(timeout=5, phrase_time_limit=8):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print('Listening...')
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            text = recognizer.recognize_google(audio).lower()
            print(f'You said: {text}')
            return text
        except sr.WaitTimeoutError:
            print('Listening timed out.')
            return ''
        except sr.UnknownValueError:
            print('Could not understand audio.')
            return ''
        except sr.RequestError as exc:
            print(f'Speech recognition request failed: {exc}')
            return ''

def listen_yes_no():
    response = listen(timeout=5, phrase_time_limit=4)
    if any(word in response for word in ('yes', 'yeah', 'yep', 'sure', 'ok', 'okay')):
        return 'yes'
    if any(word in response for word in ('no', 'nah', 'nope', 'not')):
        return 'no'
    return ''

def listen_for_scream():
    speak('Say your scream now.')
    text = listen(timeout=5, phrase_time_limit=10)
    if not text:
        speak('I did not hear your scream. Please try again.')
    return text

def create_webdriver():
    options = Options()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-notifications')

    if CHROMEDRIVER_PATH:
        service = Service(CHROMEDRIVER_PATH)
        return webdriver.Chrome(service=service, options=options)

    return webdriver.Chrome(options=options)

def fill_scream_text(driver, text):
    textarea = driver.find_element(By.ID, 'screamText')
    driver.execute_script('arguments[0].value = arguments[1];', textarea, text)

def click_scream_button(driver):
    button = driver.find_element(By.ID, 'screamBtn')
    button.click()

def main():
    try:
        arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
    except serial.SerialException as exc:
        print(f'Could not open serial port {SERIAL_PORT}: {exc}')
        return

    try:
        driver = create_webdriver()
    except WebDriverException as exc:
        print(f'Could not start Chrome WebDriver: {exc}')
        print('If ChromeDriver is not installed or not on PATH, set CHROMEDRIVER_PATH in the script.')
        return

    driver.get(HTML_FILE)
    state = 'waiting'
    last_punch_time = 0
    scream_text = ''

    speak('Punching bag controller is ready.')

    while True:
        if arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8', errors='ignore').strip()
            if line == 'punch':
                now = time.time()
                if now - last_punch_time < DEBOUNCE_SECONDS:
                    continue
                last_punch_time = now

                print(f'Punch detected, state={state}')

                if state == 'waiting':
                    speak('Do you want to scream into a hole?')
                    state = 'asked'
                elif state == 'ready_to_send':
                    try:
                        click_scream_button(driver)
                        speak('Your scream has been sent into the void.')
                    except Exception as exc:
                        print(f'Error clicking Scream button: {exc}')
                        speak('There was a problem sending the scream.')
                    state = 'waiting'
                    scream_text = ''

        if state == 'asked':
            answer = listen_yes_no()
            if answer == 'yes':
                speak('Okay Confirmed. Scream into the hole now.')
                scream_text = listen_for_scream()
                if scream_text:
                    fill_scream_text(driver, scream_text)
                    speak('Punch again to send the scream.')
                    state = 'ready_to_send'
                else:
                    state = 'waiting'
            elif answer == 'no':
                speak('Okay, maybe next time.')
                state = 'waiting'
        time.sleep(0.1)

if __name__ == '__main__':
    main()