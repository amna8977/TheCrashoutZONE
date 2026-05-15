# The Crashout Zone

Sometimes you do not need a productivity app. Sometimes you need to punch something, yell your feelings at a computer, and let the void do its thing.

The Crashout Zone connects a physical punching bag button to a browser page. You can type a crashout, use voice input, or let the Python bridge listen for punches from an Arduino/Pico and control the page for you.

## What Is In Here

- `Screamintoahole.html` is the web page.
- `intro.html` is also a web page
- `Punchingbag.ino` is the Arduino sketch that detects a punch/button press.
- `punching_bag_integration.py` connects the hardware, microphone, text-to-speech, and browser together.
- `This is fine.jpg` is the background image for the page.

## The Basic Idea

The Arduino watches a button on pin `2`. When the button is pressed, it sends the word `punch` over serial.

The Python script listens for that serial message. The first punch starts the interaction, asks whether you want to enter The Crashout Zone, records your answer, and puts your spoken crashout into the web page. A second punch sends it.


## Try Just the Website

You do not need the hardware to use the page.

Open:

```text
Screamintoahole.html
```

The website lets you:

- type a crashout
- use browser voice recognition, if your browser supports it
- keep a local count of how many crashouts have been sent

Chrome or Edge will usually work best for the voice button.

# Hardware

The Arduino sketch expects a simple button or impact switch:

- one side goes to digital pin `2`
- the other side goes to `GND`

The sketch uses `INPUT_PULLUP`, so you do not need an extra pull-up resistor.

When the button is pressed, the board sends this over serial:

```text
punch
```

The baud rate is `9600`.

## Arduino Setup

Upload `Punchingbag.ino` with the Arduino IDE.

If the sketch complains about the first line, change:

```cpp
#include < Arduino.h>
```

to:

```cpp
#include <Arduino.h>
```

You can also remove that line if your Arduino setup already includes it automatically.

# Python Setup

From this project folder, create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the Python packages:

```powershell
pip install pyserial pyttsx3 SpeechRecognition selenium pyaudio
```

On Windows, `pyaudio` can be fussy. If it does not install cleanly, try:

```powershell
pip install pipwin
pipwin install pyaudio
```

## Configuration

Before running the Python script, open `punching_bag_integration.py` and check these lines:

```python
SERIAL_PORT = 'COM3'
BAUD_RATE = 9600
CHROMEDRIVER_PATH = None
HTML_FILE = 'file:///C:/Users/sguls/OneDrive/BEEST/Screamintoahole.html'
```

The important one is `SERIAL_PORT`. Change it to whatever port your board is using, usually `COM3`, `COM4`, or `COM5` on Windows.

If Selenium cannot find ChromeDriver by itself, download ChromeDriver and set:

```python
CHROMEDRIVER_PATH = r'C:\path\to\chromedriver.exe'
```

# Running Everything

1. Plug in the Arduino or Pico.
2. Upload `Punchingbag.ino`.
3. Activate the Python virtual environment.
4. Run the bridge:

```powershell
python punching_bag_integration.py
```

Chrome should open the web page.

Then the flow is:

1. Punch once.
2. Say yes when it asks if you want to enter The Crashout Zone.
3. Say your crashout.
4. Punch again to send it.

# Troubleshooting

## The serial port will not open

Check that the Arduino IDE Serial Monitor is closed, the board is plugged in, and `SERIAL_PORT` matches the board's port.

## ChromeDriver will not start

Make sure Chrome is installed and Selenium is up to date. If you are using a manual ChromeDriver, make sure it matches your Chrome version.

## Browser voice input does not work

Try Chrome or Edge. Some browsers do not support the Web Speech API.

## Python cannot hear you

Check your microphone permissions, default input device, and whether `pyaudio` installed correctly.

# Privacy Note

The web page runs in your browser. The Python speech recognition uses Google's online recognition through the `SpeechRecognition` package, so that part needs an internet connection.

# Common Questions And Concerns!

#### Can I use this if I am not a coder?
    Of Course!!!!
#### What are these Buttons You Speaf Of???
    They are one-key macropads! THey are really easy to use, and you can bulk buy on of Amazon!
#### Regular Punching bags are just fine.....
    Well, this is cooler. Just Kidding. This machine is more of a comfort buddy as well, as you cand shout into it and then send the words away.
#### How Much do you think it costs to make?
    Around 40-60 dollars including the punching bag, and you can always DIY a punching bag out of pillows if you cant afford the punching bag
