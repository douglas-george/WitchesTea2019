enum GameState
{
  UNKNOWN_GAME_STATE,
  WAITING_TO_START,
  AT_ATTENTION,
  SMOKING,
  REGINAS_WARNING,
  WANDS_AT_THE_READY,
  CHECK_FOR_POISONING
};



String currentState = "UNKNOWN";

int lastProcessedMessageId = -1;


void setup()
{
  // Initilize hardware:
  Serial.begin(115200);

  InitComms();

  InitLeds();

  SendHeartbeat();
}


void loop()
{
  ServiceLeds();
  
  /*
  bool gameStateIsValid;
  int messageId;
  int messageCount;
  GameState latestState;

  
  SendHeartbeatIfNeeded();

  
  
  bool validGameState = GetGameState(messageId, messageCount, latestState);

  if (validGameState)
  {
    if (messageId == lastProcessedMessageId)
    {
      Serial.println("I have already handled this state...");
    }
    else
    {
      switch(latestState)
      {
        case UNKNOWN_GAME_STATE:
          Serial.println("Uh-oh!!!!! We are in an unknown state!!!");
          break;
          
        case WAITING_TO_START:
          Serial.println("WAITING_TO_START");
          lastProcessedMessageId = messageId;
          break;

        case AT_ATTENTION:
          Serial.println("AT_ATTENTION");
          lastProcessedMessageId = messageId;
          break;          
        
        case SMOKING:
          Serial.println("SMOKING");
          lastProcessedMessageId = messageId;
          break;
        
        case REGINAS_WARNING:
          Serial.println("REGINAS_WARNING");
          lastProcessedMessageId = messageId;
          break;
        
        case WANDS_AT_THE_READY:
          Serial.println("WANDS_AT_THE_READY");
          lastProcessedMessageId = messageId;
          break;
        
        case CHECK_FOR_POISONING:
          Serial.println("CHECK_FOR_POISONING");
          lastProcessedMessageId = messageId;
          break;
      }
    }
  }
  else
  {
    Serial.println("Uh-oh!!!!! Missed heartbeat!!!");
  }
  */
}
