#include <Arduino.h>

const int buttonPin = 2;
const unsigned long debounceDelay = 50;
int lastButtonState = HIGH;
int lastStableState = HIGH;
unsigned long lastDebounceTime = 0;

void setup() {
  pinMode(buttonPin, INPUT_PULLUP);
  Serial.begin(9600);
  delay(2000);
  Serial.println("The Zone bag is ready");
}

void loop() {
  int reading = digitalRead(buttonPin);

  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading != lastStableState) {
      lastStableState = reading;
      if (lastStableState == LOW) {
        Serial.println("punch");
      }
    }
  }

  lastButtonState = reading;
}
