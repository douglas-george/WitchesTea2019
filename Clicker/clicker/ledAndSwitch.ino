
const int ledPin = 19;
const int switchPin = 35;

const int ledPwmChannel = 0;

uint8_t lastSetBrightness = 123;


void InitLed(void)
{
  ledcSetup(ledPwmChannel, 5000, 8);
  ledcAttachPin(ledPin, ledPwmChannel);

  SetLedBrightness(0);
}


void SetLedBrightness(uint8_t brightness)
{
  if (brightness != lastSetBrightness)
  {
    ledcWrite(ledPwmChannel, brightness);
    lastSetBrightness = brightness;
  }
}


void InitSwitch(void)
{
  pinMode(switchPin, INPUT);
}


bool SwitchIsPressed(void)
{
  return !digitalRead(switchPin);
}
