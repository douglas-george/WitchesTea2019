#include <WiFi.h>
#include <WiFiUdp.h>


const char* ssid = "Dave";
const char* password = "553N280W";

const char* ANNOUNCEMENT_BCAST_ADDR = "192.168.5.255";
const int ANNOUNCEMENT_PORT = 10103;

const char* GADGET_BCAST_ADDR = "192.168.5.255";
const int WAND_PORT = 10109;

WiFiUDP outgoing_udp;
WiFiUDP incoming_udp;

int heartbeatRate = 1000;
unsigned long timeOfLastHeartbeatTx = 0;


void InitComms(void)
{
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);

  InitFOTA();

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println(".");
  }
 
  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());

  outgoing_udp.begin(WAND_PORT);
  incoming_udp.begin(ANNOUNCEMENT_PORT);
}


String parseOutTag(String& fullStr, String& tagName)
{
  String openTag = String("<") + tagName + String(">");
  String closeTag = String("</") + tagName + String(">");

  int indexOfOpenTag = fullStr.indexOf(openTag);
  int indexOfCloseTag = fullStr.indexOf(closeTag);

  if ((indexOfOpenTag < 0) || (indexOfCloseTag < 0))
  {
    return String("");
  }
  else
  {
    return fullStr.substring(indexOfOpenTag + openTag.length(), indexOfCloseTag);
  }
}


bool GetGameState(int& messageId, int& messageCount, GameState& currentState)
{
  int packetSize;

  uint8_t incomingPacket[500];
  
  packetSize = incoming_udp.parsePacket();

  if (packetSize > 0)
  {
    //Serial.printf("Received %d bytes from %s, port %d\n", packetSize, incoming_udp.remoteIP().toString().c_str(), incoming_udp.remotePort());
    int len = incoming_udp.read(incomingPacket, 500);

    String fullStr = String((const char*) incomingPacket); 
    
    String tagName = String("MESSAGE_TYPE");
    String contents = parseOutTag(fullStr, tagName);
    if (contents != String("GAME_HEARTBEAT"))
    {
      Serial.println(contents);
    }

    tagName = String("GADGET_ID");
    String gadgetId = parseOutTag(fullStr, tagName);

    tagName = String("MESSAGE_ID");
    messageId = parseOutTag(fullStr, tagName).toInt();

    tagName = String("MESSAGE_COUNT");
    messageCount = parseOutTag(fullStr, tagName).toInt();

    tagName = String("GAME_STATE");
    String gameState = parseOutTag(fullStr, tagName);

    if (gameState == String("WAITING TO START"))
    {
      currentState = WAITING_TO_START;
      return true;
    }
    else if (gameState == String("AT ATTENTION"))
    {
      currentState = AT_ATTENTION;
      return true;
    }
    else if (gameState == String("SMOKING"))
    {
      currentState = SMOKING;
      return true;
    }
    else if (gameState == String("REGINA'S WARNING"))
    {
      currentState = REGINAS_WARNING;
      return true;
    }
    else if (gameState == String("WANDS AT THE READY"))
    {
      currentState = WANDS_AT_THE_READY;
      return true;
    }
    else if (gameState == String("CHECK FOR POISONING"))
    {
      currentState = CHECK_FOR_POISONING;
      return true;
    }
  }

  // didn't receive heartbeat this time
  return false;
}


void SendHeartbeatIfNeeded(void)
{
  unsigned long currentTime = millis();

  if (currentTime > (timeOfLastHeartbeatTx + heartbeatRate))
  {
    SendHeartbeat();
  }
}


void SendHeartbeat(void)
{
    String heartbeat;
    int stringLength;

    unsigned long currentTime = millis();
    
    FormHeartbeat(heartbeat);
    stringLength = heartbeat.length();

    Serial.println("Transmitting Heartbeat!!!!!!!!!!!!!!!!");
    
    outgoing_udp.beginPacket(GADGET_BCAST_ADDR, WAND_PORT);
    outgoing_udp.write((const uint8_t*)heartbeat.c_str(), stringLength);
    outgoing_udp.endPacket();

    timeOfLastHeartbeatTx = currentTime;
}


void FormHeartbeat(String& heartbeat)
{
  static uint32_t messageId = 0;

  String subString;

  heartbeat = String(heartbeat + "<GADGET_MESSAGE>\n\r");
  
  heartbeat = String(heartbeat + "\t<MESSAGE_TYPE>GADGET_HEARTBEAT</MESSAGE_TYPE>\n\r");
  
  heartbeat = String(heartbeat + "\t<GADGET_ID>");
  subString = String(storedWandOwner);
  heartbeat = String(heartbeat + subString);
  heartbeat = String(heartbeat + "\t</GADGET_ID>\n\r");

  heartbeat = String(heartbeat + "\t<MESSAGE_ID>");
  subString = String(messageId);
  heartbeat = String(heartbeat + subString);
  heartbeat = String(heartbeat + "\t</MESSAGE_ID>\n\r");

  heartbeat = String(heartbeat + "\t<GADGET_STATE>");
  subString = String(currentState);
  heartbeat = String(heartbeat + subString);
  heartbeat = String(heartbeat + "\t</GADGET_STATE>\n\r");

  heartbeat = String(heartbeat + "\t<COMPILE_DATE>");
  subString = String(__DATE__);
  heartbeat = String(heartbeat + subString);
  heartbeat = String(heartbeat + "\t</COMPILE_DATE>\n\r");

  heartbeat = String(heartbeat + "\t<COMPILE_TIME>");
  subString = String(__TIME__);
  heartbeat = String(heartbeat + subString);
  heartbeat = String(heartbeat + "\t</COMPILE_TIME>\n\r");    

  heartbeat = String(heartbeat + "</GADGET_MESSAGE>\n\r");

  messageId += 1;
}
