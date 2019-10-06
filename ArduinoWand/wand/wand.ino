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

int timeOfNextInterval = millis();

int timeOfLastHeartbeatRx = millis();

int timeOfLastMissedHeartbeatWarning = 0;

const int maxOwnerLength = 50;
char storedWandOwner[maxOwnerLength];

int LoopCounts = 0;
int movementCounts = 0;
int motionCheckPeriod = 1500;
double requisiteMovementPercentage = 0.55;

bool fotaInProgress = false;
int timeOfLastFotaActivity;


void setup()
{
  // Initilize hardware:
  Serial.begin(115200);

  Serial.println("Initializing Wand ID");
  InitWandId();
  Serial.print("This wand belongs to ");
  Serial.println(storedWandOwner);

  Serial.println("Initializing Buzzers");
  InitBuzzers();

  Serial.println("Initializing LEDs");
  InitLeds();

  Serial.println("Initializing IMU");
  InitImu();

  Serial.println("Initializing Comms");
  InitComms();

  Serial.println("Sending first heartbeat.");
  SendHeartbeat();

  Serial.println("Starting main loop...");
}


void loop()
{
  bool gameStateIsValid;
  int messageId;
  int messageCount;
  GameState latestState;
  bool wandIsGettingMoved;
  int currentTime;

  currentTime = millis();
  LoopCounts += 1;

  
  serviceFOTA();

  if (fotaInProgress)
  {
    if (millis() > (timeOfLastFotaActivity + 5000))
    {
      fotaInProgress = false;
    }
  }
  else
  {
    SendHeartbeatIfNeeded();
  
    wandIsGettingMoved = ServiceImu();
    if (wandIsGettingMoved)
    {
      movementCounts++;
    }
  
    if (currentTime > timeOfNextInterval)
    {
      double movementPercentage = double(movementCounts) / double(LoopCounts);
      if (movementPercentage > requisiteMovementPercentage)
      {
        Serial.print("Last second there were ");
        Serial.print(movementCounts);
        Serial.print(" / ");
        Serial.println(LoopCounts);
      }
      LoopCounts = 0;
      movementCounts = 0;
      timeOfNextInterval = currentTime + motionCheckPeriod;
    }
  
    
    gameStateIsValid = GetGameState(messageId, messageCount, latestState);
  
    if (gameStateIsValid)
    {
      timeOfLastHeartbeatRx = currentTime;
      
      if (messageId == lastProcessedMessageId)
      {
        // already handled this state - do nothing.
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
            SetLedColor(255, 0, 0);
            lastProcessedMessageId = messageId;
            break;
  
          case AT_ATTENTION:
            Serial.println("AT_ATTENTION");
            SetLedColor(0, 255, 0);
            lastProcessedMessageId = messageId;
            break;          
          
          case SMOKING:
            Serial.println("SMOKING");
            SetLedColor(0, 0, 255);
            lastProcessedMessageId = messageId;
            break;
          
          case REGINAS_WARNING:
            Serial.println("REGINAS_WARNING");
            SetLedColor(255, 255, 255);
            lastProcessedMessageId = messageId;
            break;
          
          case WANDS_AT_THE_READY:
            Serial.println("WANDS_AT_THE_READY");
  
            for (int j = 0; j < 5; j++)
            {
              SetBuzzer(2, 1);
              SetBuzzer(3, 0);
              delay(1000);
    
              SetBuzzer(2, 0);
              SetBuzzer(3, 0);
              delay(250);
    
              SetBuzzer(2, 0);
              SetBuzzer(3, 1);
              delay(1000);
    
              SetBuzzer(2, 0);
              SetBuzzer(3, 0);
              delay(250);
            }
            
  
  
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
      if (currentTime - timeOfLastMissedHeartbeatWarning > 5000)
      {
        int timeSinceLastHeartbeatRx = currentTime - timeOfLastHeartbeatRx;
        if (timeSinceLastHeartbeatRx > 5000)
        {
          double printTime = timeSinceLastHeartbeatRx / 1000.0;
          
          Serial.print("Warning, it has been over ");
          Serial.print(printTime);
          Serial.println(" seconds without hearing a heartbeat from the game server!!!!");
          timeOfLastMissedHeartbeatWarning = currentTime;
        }
      }
    }
  }
}
