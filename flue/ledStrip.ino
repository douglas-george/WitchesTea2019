#include "FastLED.h"
#define NUM_LEDS 300


CRGB leds[NUM_LEDS];

void InitLeds()
{
  FastLED.addLeds<NEOPIXEL, 6>(leds, NUM_LEDS);
}


void UpdateLedMode()
{

  
}


void ServiceLeds()
{
  leds[0] = CRGB::White; 
  FastLED.show(); 
  delay(30);
  
  leds[0] = CRGB::Black; FastLED.show(); delay(30);

}
