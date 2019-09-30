
const int redLedPin = 33;
const int blueLedPin = 12;
const int greenLedPin = 15;

const int redPwmChannel = 0;
const int greenPwmChannel = 1;
const int bluePwmChannel = 2;

const int buzz1 = 2;
const int buzz2 = 4;
const int buzz3 = 26;



void InitLeds()
{
  // set lines to output

  // setup each PWM channel
  ledcSetup(redPwmChannel, 5000, 8);
  ledcSetup(greenPwmChannel, 5000, 8);
  ledcSetup(bluePwmChannel, 5000, 8);

  // associate each output with a PWM channel
  ledcAttachPin(redLedPin, redPwmChannel);
  ledcAttachPin(greenLedPin, greenPwmChannel);
  ledcAttachPin(blueLedPin, bluePwmChannel);

}


void SetLedColor(uint8_t red, uint8_t green, uint8_t blue)
{
  ledcWrite(redPwmChannel, red);
  ledcWrite(greenPwmChannel, green);
  ledcWrite(bluePwmChannel, blue);
  
}


void InitBuzzers(void)
{
  pinMode (buzz1, OUTPUT);
  pinMode (buzz2, OUTPUT);
  pinMode (buzz3, OUTPUT);
}


void SetBuzzer(uint8_t buzzerIndex, uint8_t turnOn)
{
  if (buzzerIndex == 1)
  {
    if (turnOn == 1)
    {
      digitalWrite (buzz1, HIGH);
    }
    else
    {
      digitalWrite (buzz1, LOW);
    }
  }

  if (buzzerIndex == 2)
  {
    if (turnOn == 1)
    {
      digitalWrite (buzz2, HIGH);
    }
    else
    {
      digitalWrite (buzz2, LOW);
    }
  }


  if (buzzerIndex == 3)
  {
    if (turnOn == 1)
    {
      digitalWrite (buzz3, HIGH);
    }
    else
    {
      digitalWrite (buzz3, LOW);
    }
  }


}
