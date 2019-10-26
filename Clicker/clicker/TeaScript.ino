static uint32_t timeOfLastStatePrint = millis();



void ServiceCurrentState(void)
{
  static bool reginaSaysYouArePoisonedInitialized = false;
  static uint32_t reginaSaysYouArePoisonedStartTime = 0;
  
  if (millis() > timeOfLastStatePrint + 3000)
  {
    Serial.print("The current state is: ");
    Serial.println(currentState);
    timeOfLastStatePrint = millis();    
  }

  
  switch(currentState)
  {
    case UNKNOWN_GAME_STATE:
    case REGINA_ARRIVES:
    case REGINA_EXPLAINS:
    case FOGGER_WARMUP:
    case FOGGER_COUNTDOWN:
    case EVIL_ANNOUNCEMENT:
    case FOGGER_OFF:
    case REGINAS_PLAN:
    case SPELL_BOOKS_APPEAR:
    case ANTIDOTE_EXPLANATION:
    case REGINA_SUGGESTS_PUMPKIN_CAKE:
    case REGINA_ASKS_IF_YOU_HAVE_DESERT_TOAD:
    case REGINA_SAYS_THE_BRAVEST_MUST_EAT_IT:
    case REGINA_SUGGESTS_KOUING_AMAN:
    case REGINA_SUGGESTS_POPCORN:
    case REGINA_EXPLAINS_RISUS_MAGNA:
    case REGINA_EXPLAINS_LINGUA_GUSTARE:
    case NOT_ENOUGH_NEED_THE_BEST_CANTANTA_CANTICUM_SPELL:
    case EAT_CHOCOLATE_KEYS:
    case REGINA_DEPARTS_IN_A_RUSH_SAYS_USE_DENTIS_FORTIS:
    case CRAFT_CURE:
    case CAST_PROHIBERE:
    case CAST_AFFLICTO:
    case CAST_FORTISSIMI:
    case CAST_RISUS_MAGNA:
    case CAST_LINGUA_GUSTARE:
    case CAST_CANTATA_CANTICUM:
    case CAST_DENTIS_FORTIS:
    case WAIT_ON_PROHIBERE:
    case WAIT_ON_AFFLICTO:
    case WAIT_ON_FORTISSIMI:
    case WAIT_ON_RISUS_MAGNA:
    case WAIT_ON_LINGUA_GUSTARE:
    case WAIT_ON_CANTATA_CANTICUM:
    case WAIT_ON_DENTIS_FORTIS:
      reginaSaysYouArePoisonedInitialized = false;
      SetLedBrightness(0);
      heartbeatRate = 2500;
      currentStatus = "HOLD";
      
      delay(250);
      break;

    case REGINA_SAYS_YOU_ARE_POISONED:
      if (reginaSaysYouArePoisonedInitialized)
      {
        int32_t timeUntilLedTurnsOn = (reginaSaysYouArePoisonedStartTime + 25000) - millis();
        
        if (timeUntilLedTurnsOn < 0)
        {
          SetLedBrightness(255);
          
          if (SwitchIsPressed())
          {
            delay(150);
            if (SwitchIsPressed())
            {
              Serial.println("Pressed");
              currentStatus = "PROCEED";
              heartbeatRate = 250;
            }        
          }
        }
      }
      else
      {
        Serial.println("Initializing REGINA_SAYS_YOU_ARE_POISONED");
        
        SetLedBrightness(0);
        heartbeatRate = 250;
        currentStatus = "HOLD";
        
        reginaSaysYouArePoisonedStartTime = millis();
        reginaSaysYouArePoisonedInitialized = true;
      }
      
      break;
      
    case SETTING_UP:
    case FAMILY_PICTURES:
    case GROUP_PICTURES:
    case DINNER:
    case POISONING:    
    case PASS_OUT_BOOKS:      
    case EATING_PUMPKIN_CAKE:
    case WAIT_TO_FIND_TOAD:    
    case EAT_TOAD:    
    case REGINA_SUGGESTS_COCKROACH_CLUSTERS:    
    case EAT_KOUING_AMAN:    
    case EAT_POPCORN:
    case REGINA_SAYS_FIND_DRAGONFLY_THORAX:    
    case HYSTERICAL_LAUGHING:
    case EAT_CAULDRON_CAKES:
    case FINDING_DRAGONFLY_THORAX:
    case PEDERSENS_SING:
    case EAT_GOLD_ROCKS:
      reginaSaysYouArePoisonedInitialized = false;
      SetLedBrightness(255);
      
      if (SwitchIsPressed())
      {
        delay(150);
        if (SwitchIsPressed())
        {
          Serial.println("Pressed");
          currentStatus = "PROCEED";
          heartbeatRate = 250;
        }        
      }
      else
      {
        currentStatus = "HOLD";
      }
      break;
  }
}
