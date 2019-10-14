enum GameState
{
  UNKNOWN_GAME_STATE,
  SETTING_UP,
  FAMILY_PICTURES,
  GROUP_PICTURES,
  REGINA_ARRIVES,
  REGINA_EXPLAINS,
  DINNER,
  FOGGER_WARMUP,
  FOGGER_COUNTDOWN,
  POISONING,
  EVIL_ANNOUNCEMENT,
  CAST_PROHIBERE,
  WAIT_ON_PROHIBERE,
  FOGGER_OFF,
  REGINAS_PLAN,
  SPELL_BOOKS_APPEAR,
  PASS_OUT_BOOKS,
  ANTIDOTE_EXPLANATION,
  REGINA_SUGGESTS_PUMPKIN_CAKE,
  EATING_PUMPKIN_CAKE,
  CAST_AFFLICTO,
  WAIT_ON_AFFLICTO,
  REGINA_SAYS_YOU_ARE_POISONED,
  REGINA_ASKS_IF_YOU_HAVE_DESERT_TOAD,
  WAIT_TO_FIND_TOAD,
  REGINA_SAYS_THE_BRAVEST_MUST_EAT_IT,
  CAST_FORTISSIMI,
  WAIT_ON_FORTISSIMI,
  EAT_TOAD,
  REGINA_SUGGESTS_KOUING_AMAN,
  EAT_KOUING_AMAN,
  REGINA_SUGGESTS_POPCORN,
  EAT_POPCORN,
  REGINA_SUGGESTS_COCKROACH_CLUSTERS,
  REGINA_EXPLAINS_RISUS_MAGNA,
  CAST_RISUS_MAGNA,
  WAIT_ON_RISUS_MAGNA,
  HYSTERICAL_LAUGHING,
  REGINA_EXPLAINS_LINGUA_GUSTARE,
  CAST_LINGUA_GUSTARE,
  WAIT_ON_LINGUA_GUSTARE,
  EAT_CAULDRON_CAKES,
  REGINA_SAYS_FIND_DRAGONFLY_THORAX,
  FINDING_DRAGONFLY_THORAX,
  NOT_ENOUGH_NEED_THE_BEST_CANTANTA_CANTICUM_SPELL,
  CAST_CANTATA_CANTICUM,
  WAIT_ON_CANTATA_CANTICUM,
  EAT_CHOCOLATE_KEYS,
  PEDERSENS_SING,
  REGINA_DEPARTS_IN_A_RUSH_SAYS_USE_DENTIS_FORTIS,
  CAST_DENTIS_FORTIS,
  WAIT_ON_DENTIS_FORTIS,
  EAT_GOLD_ROCKS,
  CRAFT_CURE
};



GameState currentState;
String currentStateString;
bool stateChanged = false;

int lastProcessedMessageId = -1;

int timeOfNextInterval;

int timeOfLastHeartbeatRx = millis();

int timeOfLastMissedHeartbeatWarning = 0;

const int maxOwnerLength = 50;
char storedWandOwner[maxOwnerLength];

bool startWandMotionSampling = false;
bool wandSamplingInProgress = false;
double movementPercentage = 0;
int LoopCounts = 0;
int movementCounts = 0;
int motionCheckPeriod = 1500;

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

    if (wandSamplingInProgress)
    {
      if (startWandMotionSampling)
      {
        timeOfNextInterval = currentTime + motionCheckPeriod;
        LoopCounts = 0;
        movementCounts = 0;

        startWandMotionSampling = false;
      }

      if (currentTime > timeOfNextInterval)
      {
        startWandMotionSampling = true;
        movementPercentage = double(movementCounts) / double(LoopCounts);
        Serial.println(movementPercentage);
        
      }
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
