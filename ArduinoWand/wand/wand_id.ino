#include "SPIFFS.h"


#define WAND_OWNER_TO_WRITE "Alexis"

#define UPDATE_STORED_WAND_OWNER 0





void InitWandId(void)
{
  File f;
  int i;
  char dataByte;

  SPIFFS.begin();
    
#if UPDATE_STORED_WAND_OWNER==1
  Serial.print("Formatting...");
  SPIFFS.format();
  Serial.println("Done");

  f = SPIFFS.open("/id.txt", "w");
  if (!f) {
      Serial.println("file open failed");
  }
  Serial.println("====== Writing to SPIFFS file =========");
  f.print(WAND_OWNER_TO_WRITE);
  f.close();
#endif

  f = SPIFFS.open("/id.txt", "r");
  if (!f) 
  {
      Serial.println("file open failed");
  }
  else
  {  
    storedWandOwner = f.readStringUntil('\n');
    Serial.print("This wand belongs to: ");
    Serial.println(storedWandOwner);
  }
}
