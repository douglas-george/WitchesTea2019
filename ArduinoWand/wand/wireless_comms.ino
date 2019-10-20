#include <WiFi.h>
#include <WiFiUdp.h>


//const char* ssid = "WitchesTea";
const char* ssid = "Dave";
const char* password = "553N280W";

const char* ANNOUNCEMENT_BCAST_ADDR = "192.168.5.255";
const int ANNOUNCEMENT_PORT = 10103;

const char* GADGET_BCAST_ADDR = "192.168.5.255";
const int WAND_PORT = 10109;

WiFiUDP outgoing_udp;
WiFiUDP incoming_udp;

int heartbeatRate = 2500;
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

    if      (gameState == String("SETTING_UP"))                                         {currentState = SETTING_UP;                                         return true; }
    else if (gameState == String("FAMILY_PICTURES"))                                    {currentState = FAMILY_PICTURES;                                    return true; }
    else if (gameState == String("GROUP_PICTURES"))                                     {currentState = GROUP_PICTURES;                                     return true; }
    else if (gameState == String("REGINA_ARRIVES"))                                     {currentState = REGINA_ARRIVES;                                     return true; }
    else if (gameState == String("REGINA_EXPLAINS"))                                    {currentState = REGINA_EXPLAINS;                                    return true; }
    else if (gameState == String("DINNER"))                                             {currentState = DINNER;                                             return true; }
    else if (gameState == String("FOGGER_WARMUP"))                                      {currentState = FOGGER_WARMUP;                                      return true; }
    else if (gameState == String("FOGGER_COUNTDOWN"))                                   {currentState = FOGGER_COUNTDOWN;                                   return true; }
    else if (gameState == String("POISONING"))                                          {currentState = POISONING;                                          return true; }
    else if (gameState == String("EVIL_ANNOUNCEMENT"))                                  {currentState = EVIL_ANNOUNCEMENT;                                  return true; }
    else if (gameState == String("CAST_PROHIBERE"))                                     {currentState = CAST_PROHIBERE;                                     return true; }
    else if (gameState == String("WAIT_ON_PROHIBERE"))                                  {currentState = WAIT_ON_PROHIBERE;                                  return true; }
    else if (gameState == String("FOGGER_OFF"))                                         {currentState = FOGGER_OFF;                                         return true; }
    else if (gameState == String("REGINAS_PLAN"))                                       {currentState = REGINAS_PLAN;                                       return true; }
    else if (gameState == String("SPELL_BOOKS_APPEAR"))                                 {currentState = SPELL_BOOKS_APPEAR;                                 return true; }
    else if (gameState == String("PASS_OUT_BOOKS"))                                     {currentState = PASS_OUT_BOOKS;                                     return true; }
    else if (gameState == String("ANTIDOTE_EXPLANATION"))                               {currentState = ANTIDOTE_EXPLANATION;                               return true; }
    else if (gameState == String("REGINA_SUGGESTS_PUMPKIN_CAKE"))                       {currentState = REGINA_SUGGESTS_PUMPKIN_CAKE;                       return true; }
    else if (gameState == String("EATING_PUMPKIN_CAKE"))                                {currentState = EATING_PUMPKIN_CAKE;                                return true; }
    else if (gameState == String("CAST_AFFLICTO"))                                      {currentState = CAST_AFFLICTO;                                      return true; }
    else if (gameState == String("WAIT_ON_AFFLICTO"))                                   {currentState = WAIT_ON_AFFLICTO;                                   return true; }
    else if (gameState == String("REGINA_SAYS_YOU_ARE_POISONED"))                       {currentState = REGINA_SAYS_YOU_ARE_POISONED;                       return true; }
    else if (gameState == String("REGINA_ASKS_IF_YOU_HAVE_DESERT_TOAD"))                {currentState = REGINA_ASKS_IF_YOU_HAVE_DESERT_TOAD;                return true; }
    else if (gameState == String("WAIT_TO_FIND_TOAD"))                                  {currentState = WAIT_TO_FIND_TOAD;                                  return true; }
    else if (gameState == String("REGINA_SAYS_THE_BRAVEST_MUST_EAT_IT"))                {currentState = REGINA_SAYS_THE_BRAVEST_MUST_EAT_IT;                return true; }
    else if (gameState == String("CAST_FORTISSIMI"))                                    {currentState = CAST_FORTISSIMI;                                    return true; }
    else if (gameState == String("WAIT_ON_FORTISSIMI"))                                 {currentState = WAIT_ON_FORTISSIMI;                                 return true; }
    else if (gameState == String("EAT_TOAD"))                                           {currentState = EAT_TOAD;                                           return true; }
    else if (gameState == String("REGINA_SUGGESTS_KOUING_AMAN"))                        {currentState = REGINA_SUGGESTS_KOUING_AMAN;                        return true; }
    else if (gameState == String("EAT_KOUING_AMAN"))                                    {currentState = EAT_KOUING_AMAN;                                    return true; }
    else if (gameState == String("REGINA_SUGGESTS_POPCORN"))                            {currentState = REGINA_SUGGESTS_POPCORN;                            return true; }
    else if (gameState == String("EAT_POPCORN"))                                        {currentState = EAT_POPCORN;                                        return true; }
    else if (gameState == String("REGINA_SUGGESTS_COCKROACH_CLUSTERS"))                 {currentState = REGINA_SUGGESTS_COCKROACH_CLUSTERS;                 return true; }
    else if (gameState == String("REGINA_EXPLAINS_RISUS_MAGNA"))                        {currentState = REGINA_EXPLAINS_RISUS_MAGNA;                        return true; }
    else if (gameState == String("CAST_RISUS_MAGNA"))                                   {currentState = CAST_RISUS_MAGNA;                                   return true; }
    else if (gameState == String("WAIT_ON_RISUS_MAGNA"))                                {currentState = WAIT_ON_RISUS_MAGNA;                                return true; }
    else if (gameState == String("HYSTERICAL_LAUGHING"))                                {currentState = HYSTERICAL_LAUGHING;                                return true; }
    else if (gameState == String("REGINA_EXPLAINS_LINGUA_GUSTARE"))                     {currentState = REGINA_EXPLAINS_LINGUA_GUSTARE;                     return true; }
    else if (gameState == String("CAST_LINGUA_GUSTARE"))                                {currentState = CAST_LINGUA_GUSTARE;                                return true; }
    else if (gameState == String("WAIT_ON_LINGUA_GUSTARE"))                             {currentState = WAIT_ON_LINGUA_GUSTARE;                             return true; }
    else if (gameState == String("EAT_CAULDRON_CAKES"))                                 {currentState = EAT_CAULDRON_CAKES;                                 return true; }
    else if (gameState == String("REGINA_SAYS_FIND_DRAGONFLY_THORAX"))                  {currentState = REGINA_SAYS_FIND_DRAGONFLY_THORAX;                  return true; }
    else if (gameState == String("NOT_ENOUGH_NEED_THE_BEST_CANTANTA_CANTICUM_SPELL"))   {currentState = NOT_ENOUGH_NEED_THE_BEST_CANTANTA_CANTICUM_SPELL;   return true; }
    else if (gameState == String("CAST_CANTATA_CANTICUM"))                              {currentState = CAST_CANTATA_CANTICUM;                              return true; }
    else if (gameState == String("WAIT_ON_CANTATA_CANTICUM"))                           {currentState = WAIT_ON_CANTATA_CANTICUM;                           return true; }
    else if (gameState == String("EAT_CHOCOLATE_KEYS"))                                 {currentState = EAT_CHOCOLATE_KEYS;                                 return true; }
    else if (gameState == String("PEDERSENS_SING"))                                     {currentState = PEDERSENS_SING;                                     return true; }
    else if (gameState == String("REGINA_DEPARTS_IN_A_RUSH_SAYS_USE_DENTIS_FORTIS"))    {currentState = REGINA_DEPARTS_IN_A_RUSH_SAYS_USE_DENTIS_FORTIS;    return true; }
    else if (gameState == String("CAST_DENTIS_FORTIS"))                                 {currentState = CAST_DENTIS_FORTIS;                                 return true; }
    else if (gameState == String("WAIT_ON_DENTIS_FORTIS"))                              {currentState = WAIT_ON_DENTIS_FORTIS;                              return true; }
    else if (gameState == String("EAT_GOLD_ROCKS"))                                     {currentState = EAT_GOLD_ROCKS;                                     return true; }
    else if (gameState == String("CRAFT_CURE"))                                         {currentState = CRAFT_CURE;                                         return true; }
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
  subString = String(currentStateString);
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
