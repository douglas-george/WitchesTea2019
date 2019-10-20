#include "FS.h"


const char* WAND_OWNER_TO_WRITE = "Coleman";

#define UPDATE_STORED_WAND_OWNER 1





void InitWandId(void)
{
  int i;
  char dataByte;

  SPIFFS.begin();
    
#if UPDATE_STORED_WAND_OWNER==1
  SPIFFS.format();

  File f = SPIFFS.open("/f.txt", "w");
  if (!f) {
      Serial.println("file open failed");
  }
  Serial.println("====== Writing to SPIFFS file =========");
  f.println(WAND_OWNER_TO_WRITE);
  f.close();
#endif

  f = SPIFFS.open("/f.txt", "r");
  if (!f) 
  {
      Serial.println("file open failed");
  }
  else
  {  
    Serial.println("====== Reading from SPIFFS file =======");
    storedWandOwner = f.readStringUntil('\n');
  }
}
