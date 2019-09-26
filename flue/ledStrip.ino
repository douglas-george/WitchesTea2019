#include <Adafruit_NeoPixel.h>
 
#define NEOPIXEL_PIN  15
#define NUM_LEDS      300

// When we setup the NeoPixel library, we tell it how many pixels, and which pin to use to send signals.
// Note that for older NeoPixel strips you might need to change the third parameter--see the strandtest
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUM_LEDS, NEOPIXEL_PIN, NEO_GRB + NEO_KHZ800);


bool ledsAreOn;
int timeOfNextSwitch;
int timeOfNextTwinkle;


void InitLeds()
{
  randomSeed(analogRead(0));
  
  ledsAreOn = false;
  timeOfNextSwitch = millis();
  timeOfNextTwinkle = millis();
  
  pixels.begin();
}


void UpdateLedMode()
{

  
}


void ServiceLeds()
{
  if (millis() > timeOfNextSwitch)
  {
    int timeUntilNextSwitch;
    
    if (ledsAreOn)
    {
      timeUntilNextSwitch = random(100, 500);

      pixels.clear();
      
      ledsAreOn = false;
    }
    else
    {
      timeUntilNextSwitch = random(500, 1500);
      ledsAreOn = true;
    }

    timeOfNextSwitch = millis() + timeUntilNextSwitch;
    timeOfNextTwinkle = timeOfNextSwitch;

    if (ledsAreOn)
    {
      //Serial.print("Switching on. Time of next switch is in ");
    }
    else
    {
      //Serial.print("Switching off. Time of next switch is in ");
    }
    //Serial.println(timeUntilNextSwitch);
  }
  else
  {
    if (ledsAreOn)
    {
      if (millis() > timeOfNextTwinkle)
      {
        int brightnessLeft = 15000;
        int timeUntilNextTwinkle;

        for (int j = 0; j < NUM_LEDS; j++)
        {
          int lot = random(0, 100);
          int brightness = random(10, 200);
  
          if ((lot < 50) || (brightnessLeft < 0))
          {
            pixels.setPixelColor(j, pixels.Color(0, 0, 0));
            continue;
          }
          else if (lot < 60)
          {
            pixels.setPixelColor(j, pixels.Color(brightness, 0, 0));
          }
          else
          {
            pixels.setPixelColor(j, pixels.Color(0, brightness, 0));
          }
  
          brightnessLeft -= brightness;
        }

        timeUntilNextTwinkle = random(25, 100);
        timeOfNextTwinkle = millis() + timeUntilNextTwinkle;

        //Serial.print("\tTwinkle update complete. Time of next is in ");
        //Serial.println(timeUntilNextTwinkle);
        

        pixels.show();
      }
    }
  }
}
