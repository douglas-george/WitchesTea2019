enum GameState
{
  UNKNOWN_GAME_STATE,                                 //  0
  SETTING_UP,                                         //  1
  FAMILY_PICTURES,                                    //  2 
  GROUP_PICTURES,                                     //  3
  REGINA_ARRIVES,                                     //  4
  REGINA_EXPLAINS,                                    //  5
  DINNER,                                             //  6
  FOGGER_WARMUP,                                      //  7
  FOGGER_COUNTDOWN,                                   //  8
  POISONING,                                          //  9
  EVIL_ANNOUNCEMENT,                                  // 10
  CAST_PROHIBERE,                                     // 11
  WAIT_ON_PROHIBERE,                                  // 12
  FOGGER_OFF,                                         // 13
  REGINAS_PLAN,                                       // 14
  SPELL_BOOKS_APPEAR,                                 // 15
  PASS_OUT_BOOKS,                                     // 16
  ANTIDOTE_EXPLANATION,                               // 17
  REGINA_SUGGESTS_PUMPKIN_CAKE,                       // 18
  EATING_PUMPKIN_CAKE,                                // 19
  CAST_AFFLICTO,                                      // 20
  WAIT_ON_AFFLICTO,                                   // 21
  REGINA_SAYS_YOU_ARE_POISONED,                       // 22
  REGINA_ASKS_IF_YOU_HAVE_DESERT_TOAD,                // 23
  WAIT_TO_FIND_TOAD,                                  // 24
  REGINA_SAYS_THE_BRAVEST_MUST_EAT_IT,                // 25
  CAST_FORTISSIMI,                                    // 26
  WAIT_ON_FORTISSIMI,                                 // 27
  EAT_TOAD,                                           // 28
  REGINA_SUGGESTS_KOUING_AMAN,                        // 29
  EAT_KOUING_AMAN,                                    // 30
  REGINA_SUGGESTS_POPCORN,                            // 31
  EAT_POPCORN,                                        // 32
  REGINA_SUGGESTS_COCKROACH_CLUSTERS,                 // 33
  REGINA_EXPLAINS_RISUS_MAGNA,                        // 34
  CAST_RISUS_MAGNA,                                   // 35
  WAIT_ON_RISUS_MAGNA,                                // 36
  HYSTERICAL_LAUGHING,                                // 37
  REGINA_EXPLAINS_LINGUA_GUSTARE,                     // 38
  CAST_LINGUA_GUSTARE,                                // 39
  WAIT_ON_LINGUA_GUSTARE,                             // 40
  EAT_CAULDRON_CAKES,                                 // 41
  REGINA_SAYS_FIND_DRAGONFLY_THORAX,                  // 42
  FINDING_DRAGONFLY_THORAX,                           // 43
  NOT_ENOUGH_NEED_THE_BEST_CANTANTA_CANTICUM_SPELL,   // 44
  CAST_CANTATA_CANTICUM,                              // 45
  WAIT_ON_CANTATA_CANTICUM,                           // 46
  EAT_CHOCOLATE_KEYS,                                 // 47
  PEDERSENS_SING,                                     // 48
  REGINA_DEPARTS_IN_A_RUSH_SAYS_USE_DENTIS_FORTIS,    // 59
  CAST_DENTIS_FORTIS,                                 // 50
  WAIT_ON_DENTIS_FORTIS,                              // 51
  EAT_GOLD_ROCKS,                                     // 52
  CRAFT_CURE                                          // 53
};



GameState currentState;
String currentStateString;
bool stateChanged = false;

int lastProcessedMessageId = -1;

int timeOfNextInterval;

int timeOfLastHeartbeatRx = millis();

int timeOfLastMissedHeartbeatWarning = 0;


int heartbeatRate = 2500;

String currentStatus = "HOLD";



void setup()
{
  // Initilize hardware:
  Serial.begin(115200);
  InitLed();
  InitSwitch();

  Serial.println("Initializing Comms");
  InitComms();

  Serial.println("Starting main loop...................................................................................................");
}


void loop()
{
  bool gameStateIsValid;
  int messageId;
  int messageCount;
  int currentTime;


  currentTime = millis();
  SendHeartbeatIfNeeded();
  
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
