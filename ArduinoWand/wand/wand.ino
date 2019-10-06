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



GameState currentState;
String currentStateString;
bool stateChanged = false;

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
  
    
    gameStateIsValid = GetGameState(messageId, messageCount, currentState);
  
    if (gameStateIsValid)
    {
      timeOfLastHeartbeatRx = currentTime;
      
      if (messageId == lastProcessedMessageId)
      {
        // already handled this state - do nothing.
        stateChanged = false;
      }
      else
      {
        stateChanged = true;
      }

      lastProcessedMessageId = messageId;
      
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

    ServiceCurrentState();
  }
}
