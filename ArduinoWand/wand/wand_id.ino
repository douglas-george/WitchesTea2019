#include <EEPROM.h>


const char* WAND_OWNER_TO_WRITE = "Sitter2";

#define UPDATE_STORED_WAND_OWNER 0





void InitWandId(void)
{
  int i;
  char dataByte;

  EEPROM.begin(maxOwnerLength);
  
#if UPDATE_STORED_WAND_OWNER==1
  for (int i = 0; i < 50; i++)
  {
    EEPROM.write(i, 0);
  }

  i = 0; 
  while (i < maxOwnerLength)
  { 
    dataByte = WAND_OWNER_TO_WRITE[i];
    EEPROM.write(i, dataByte);

    if (dataByte == '\0')
    {
      break;
    }

    i++;
  }

  EEPROM.commit();

#endif

  i = 0; 
  while (i < maxOwnerLength)
  { 
    dataByte = EEPROM.read(i);

    storedWandOwner[i] = dataByte;

    if (dataByte == '\0')
    {
      break;
    }

    i++;
  }
}
