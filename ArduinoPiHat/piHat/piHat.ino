#include <Adafruit_NeoPixel.h>
 
#define PIN     14
#define N_LEDS  300

enum faceColor
{
  RED,
  GREEN
};


enum blinkState
{
  BLINK_STATE_UNINITIALIZED = 0,
  BLINK_STATE_WARM_TWINKLE = 1,
  BLINK_STATE_RED_SNAKE = 2,
  BLINK_STATE_RED_SNAKE_DONE = 3,
  BLINK_STATE_RED_FIRE = 4,
  BLINK_STATE_GREEN_FIRE = 5,
  BLINK_STATE_OFF = 6,
  BLINK_STATE_LOW_RED_FIRE = 7
};



Adafruit_NeoPixel strip = Adafruit_NeoPixel(N_LEDS, PIN, NEO_GRB + NEO_KHZ800);

blinkState currentState = BLINK_STATE_RED_FIRE;
bool stateChange = true;

 
void setup() 
{
  randomSeed(1);
  
  strip.begin();
  Serial.begin(115200);
  Serial1.begin(115200);
}


void loop()
{
  uint8_t readByte = 0xff;

  while (Serial1.available())
  {
    readByte = Serial1.read();
  }

  if (readByte != 0xff)
  {
    Serial.print("I received a ");
    Serial.println(readByte);

    if (63 == readByte)
    {
      Serial.println("Got a query");
      ;  // just return the current state
    }
    else if (currentState != readByte)
    {
      stateChange = true;
      currentState = readByte;
    }

    Serial.println(currentState);
    Serial1.write(currentState);
  }


  switch (currentState)
  {
    case BLINK_STATE_UNINITIALIZED:
    {
      ServiceUninitialized();
      break;
    }
    case BLINK_STATE_WARM_TWINKLE:
    {
      ServiceWarmTwinkle();
      break;
    }
    case BLINK_STATE_RED_SNAKE:
    {
      ServiceRedSnake();
      break;
    }
    case BLINK_STATE_RED_SNAKE_DONE:
    {
      ServiceRedSnakeDone();
      break;
    }  

    case BLINK_STATE_RED_FIRE:
    {
      ServiceFace(RED, 255);
      break;
    }  
    
    case BLINK_STATE_GREEN_FIRE:
    {
      ServiceFace(GREEN, 255);
      break;
    }  

    case BLINK_STATE_OFF:
    {
      ServiceOff();
      break;
    }

    case BLINK_STATE_LOW_RED_FIRE:
    {
      ServiceFace(RED, 40);
      break;
    }            
  }
}


void ServiceOff(void)
{
  if (stateChange)
  {
    for (uint16_t i = 0; i < N_LEDS; i++)
    {
      strip.setPixelColor(i, strip.Color(0, 0, 0));
    }

    strip.show();
    stateChange = false;
  }
}

void ServiceUninitialized(void)
{
  static unsigned long timeOfNextChange = 0;
  static bool statusIsOn = false;
  
  if (stateChange)
  {
    for (uint16_t i = 0; i < N_LEDS; i++)
    {
      strip.setPixelColor(i, strip.Color(0, 0, 0));
    }
    strip.setPixelColor(0, strip.Color(255, 0, 0));

    strip.show();

    statusIsOn = true;
    timeOfNextChange = millis() + 500;

    stateChange = false;
  }

  if (millis() > timeOfNextChange)
  {
    
    if (statusIsOn)
    {
      Serial.println("OFF");
      strip.setPixelColor(0, strip.Color(0, 0, 0));
      statusIsOn = false;
    }
    else
    {
      Serial.println("ON");
      strip.setPixelColor(0, strip.Color(255, 0, 0));
      statusIsOn = true;
    }

    strip.show();

    timeOfNextChange = millis() + 500;
  }
}


void ServiceWarmTwinkle(void)
{
  static unsigned long timeOfNextChange = 0;
  static int ledBrightness[N_LEDS];
  static int loopCount = 0;
  
  if (stateChange)
  {
    Serial.println("STATE CHANGE!!!!");
    for (uint16_t ledIndex = 0; ledIndex < N_LEDS; ledIndex++)
    {
      ledBrightness[ledIndex] = random(0, 4000);
    }
    timeOfNextChange = millis() + 5;

    stateChange = false;

    loopCount = 0;
  }

  if (millis() > timeOfNextChange)
  {
    loopCount++;

    Serial.println(loopCount);

    for (uint16_t ledIndex = 0; ledIndex < N_LEDS; ledIndex++)
    {
      if (ledBrightness[ledIndex] < 200)
      {
        // grow brighter
        strip.setPixelColor(ledIndex, strip.ColorHSV(2500, 255, ledBrightness[ledIndex]));
      }
      else if (ledBrightness[ledIndex] < 400)
      {
        // fade dimmer
        strip.setPixelColor(ledIndex, strip.ColorHSV(2500, 255, 400 - ledBrightness[ledIndex]));
      }
      else
      {
        // off
        strip.setPixelColor(ledIndex, strip.Color(0, 0, 0));
      }

      ledBrightness[ledIndex]++;
      if (ledBrightness[ledIndex] > 4000)
      {
        ledBrightness[ledIndex] = 0;        
      }
    }
    
    strip.show();
    timeOfNextChange = millis() + 1;
  }
}


void ServiceRedSnake(void)
{
  static unsigned long timeOfNextChange = 0;
  static int16_t indexOfOnLed;
  static uint16_t fillPoint;
  
  if (stateChange)
  {
    for (uint16_t i = 0; i < N_LEDS; i++)
    {
      strip.setPixelColor(i, strip.Color(0, 0, 0));
    }
    strip.show();

    indexOfOnLed = -1;
    fillPoint = (N_LEDS) - 1;

    timeOfNextChange = millis() + 5;
    stateChange = false;
  }

  Serial.print(indexOfOnLed);
  Serial.print(" ");
  Serial.println(fillPoint);
  
  
  if (fillPoint < 6)
  {
    currentState = BLINK_STATE_RED_SNAKE_DONE;
    stateChange = true;
    return;
  }

  indexOfOnLed++;
  strip.setPixelColor(indexOfOnLed, strip.Color(25, 0, 0));
  strip.setPixelColor(indexOfOnLed + 1, strip.Color(25, 0, 0));
  strip.setPixelColor(indexOfOnLed + 2, strip.Color(25, 0, 0));
  strip.setPixelColor(indexOfOnLed + 3, strip.Color(25, 0, 0));
  strip.setPixelColor(indexOfOnLed + 4, strip.Color(25, 0, 0));
  strip.setPixelColor(indexOfOnLed + 5, strip.Color(25, 0, 0));
  strip.setPixelColor(indexOfOnLed + 6, strip.Color(25, 0, 0));
  strip.setPixelColor(indexOfOnLed + 7, strip.Color(25, 0, 0));
  strip.setPixelColor(indexOfOnLed + 8, strip.Color(25, 0, 0));

  if (indexOfOnLed != 0)
  {
    strip.setPixelColor((indexOfOnLed - 1), strip.Color(0, 0, 0));

  }

  if (indexOfOnLed == fillPoint-9)
  {
    fillPoint -= 9;
    indexOfOnLed = -1;
  }
  
  strip.show();

}


void ServiceRedSnakeDone(void)
{
  if (stateChange)
  {
    Serial.println("Red Snake Done");
    for (uint16_t i = 0; i < N_LEDS; i++)
    {
      strip.setPixelColor(i, strip.Color(0, 0, 0));
    }
    strip.show();

    stateChange = false;
  }
}


void ServiceFace(faceColor color, uint8_t maxBrightness)
{
  static unsigned long timeOfNextChange = 0;
  static uint16_t loopCount;
  
  if (stateChange)
  {
    Serial.println("Starting Face");
    for (uint16_t i = 0; i < N_LEDS; i++)
    {
      strip.setPixelColor(i, strip.Color(0, 0, 0));
    }
    strip.show();

    timeOfNextChange = millis();
    loopCount = 0;

    stateChange = false;
  }

  if (millis() > timeOfNextChange)
  {
    for (uint16_t i = 0; i < N_LEDS; i++)
    {
      uint16_t percentage = random(0, 100);
      uint8_t brightness = random(50, maxBrightness);
      
      if (percentage > 75)
      {
        if (color == RED)
        {
          strip.setPixelColor(i, strip.Color(brightness, random(0,10), 0));
        }
        else
        {
          strip.setPixelColor(i, strip.Color(random(0,75), brightness, 0));
        }
      }
      else
      {
        strip.setPixelColor(i, strip.Color(0, 0, 0));
      }
    }
    strip.show();

    if (color == RED)
    {
      timeOfNextChange = millis() + random(50, 200);
    }
    else
    {
      timeOfNextChange = millis() + random(50, 300);
    }
    
    loopCount++;
  }
}
