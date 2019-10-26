

void ServiceCurrentState(void)
{
  switch(currentState)
  {
    case UNKNOWN_GAME_STATE:
      heartbeatRate = 10000;
      ServiceUnknownState();
      break;
      
    case SETTING_UP:
    case FAMILY_PICTURES:
    case GROUP_PICTURES:
      heartbeatRate = 10000;
      ServiceWandIdle(true);
      break;
    
    case REGINA_ARRIVES:
    case REGINA_EXPLAINS:
    case DINNER:
    case FOGGER_WARMUP:
    case FOGGER_COUNTDOWN:
    case POISONING:
    case EVIL_ANNOUNCEMENT:
    case REGINAS_PLAN:
    case SPELL_BOOKS_APPEAR:
    case PASS_OUT_BOOKS:
    case ANTIDOTE_EXPLANATION:
    case REGINA_SUGGESTS_PUMPKIN_CAKE:
    case EATING_PUMPKIN_CAKE:
    case REGINA_SAYS_YOU_ARE_POISONED:
    case REGINA_ASKS_IF_YOU_HAVE_DESERT_TOAD:
    case WAIT_TO_FIND_TOAD:
    case REGINA_SAYS_THE_BRAVEST_MUST_EAT_IT:
    case REGINA_SUGGESTS_KOUING_AMAN:
    case EAT_KOUING_AMAN:
    case REGINA_SUGGESTS_POPCORN:
    case EAT_POPCORN:
    case REGINA_SUGGESTS_COCKROACH_CLUSTERS:
    case REGINA_EXPLAINS_RISUS_MAGNA:
    case REGINA_EXPLAINS_LINGUA_GUSTARE:
    case REGINA_SAYS_FIND_DRAGONFLY_THORAX:
    case FINDING_DRAGONFLY_THORAX:
    case NOT_ENOUGH_NEED_THE_BEST_CANTANTA_CANTICUM_SPELL:
    case PEDERSENS_SING:
    case REGINA_DEPARTS_IN_A_RUSH_SAYS_USE_DENTIS_FORTIS:
    case CRAFT_CURE:
      heartbeatRate = 5000;
      ServiceWandIdle(true);
      break;

    case EAT_TOAD:
    case HYSTERICAL_LAUGHING:
    case EAT_CAULDRON_CAKES:
    case EAT_CHOCOLATE_KEYS:
    case EAT_GOLD_ROCKS:
    case FOGGER_OFF:
      heartbeatRate = 5000;
      ServiceWandIdle(false);
      break;

    case CAST_PROHIBERE:
    case CAST_AFFLICTO:
    case CAST_FORTISSIMI:
    case CAST_RISUS_MAGNA:
    case CAST_LINGUA_GUSTARE:
    case CAST_CANTATA_CANTICUM:
    case CAST_DENTIS_FORTIS:
      heartbeatRate = 500;
      currentStateString = "PREPARING";
      ServiceBuzzSequence(false);
      break;

    case WAIT_ON_PROHIBERE:
    case WAIT_ON_AFFLICTO:
    case WAIT_ON_FORTISSIMI:
    case WAIT_ON_RISUS_MAGNA:
    case WAIT_ON_LINGUA_GUSTARE:
    case WAIT_ON_CANTATA_CANTICUM:
    case WAIT_ON_DENTIS_FORTIS:
    {
      bool spellHasBeenCast = ServiceSpell();
      
      heartbeatRate = 500;
      
      ServiceBuzzSequence(spellHasBeenCast);

      if (spellHasBeenCast)
      {
        currentStateString = "LIT";
      }
      else
      {
        currentStateString = "STILL_TRYING";
      }
      
      break;
    }
  }
}


void ServiceUnknownState(void)
{
  if (stateChanged)
  {
    currentStateString = "Unknown State!!!";
    Serial.println(currentStateString);
    stateChanged = false;

    SetLedColor(0, 0, 0);
    SetBuzzer(2, false);
    SetBuzzer(3, false);
    startWandMotionSampling = false;
    wandSamplingInProgress = false;
  }
}


void ServiceWandIdle(bool turnOffLed)
{
  if (stateChanged)
  {
    currentStateString = "IDLE";
    Serial.println(currentStateString);
    stateChanged = false;

    if (turnOffLed)
    {
      SetLedColor(0, 0, 0);
    }
    
    SetBuzzer(2, false);
    SetBuzzer(3, false);
    startWandMotionSampling = false;
    wandSamplingInProgress = false;    
  }
}


void ServiceBuzzSequence(bool dontDoBuzz)
{
  static unsigned long timeOfNextBuzz;
  static uint8_t whichBuzz;

  if (dontDoBuzz)
  {
    SetBuzzer(2, false);
    SetBuzzer(3, false);
    return;
  }
  
  if (stateChanged)
  {
    SetLedColor(0, 0, 0);
    SetBuzzer(2, false);
    SetBuzzer(3, false);
    startWandMotionSampling = false;
    wandSamplingInProgress = false;

    timeOfNextBuzz = millis();
    whichBuzz = 1;

    stateChanged = false;
  }

  if (millis() > timeOfNextBuzz)
  {
    whichBuzz++;

    if (whichBuzz % 4 == 0)
    {
      SetBuzzer(2, false);
      SetBuzzer(3, false);
      timeOfNextBuzz = millis() + 150;
    }
    else if (whichBuzz % 4 == 1)
    {
      SetBuzzer(2, true);
      SetBuzzer(3, false);
      timeOfNextBuzz = millis() + 350;
    }

    else if (whichBuzz % 4 == 2)
    {
      SetBuzzer(2, false);
      SetBuzzer(3, false);
      timeOfNextBuzz = millis() + 150;
    }

    else if (whichBuzz % 4 == 3)
    {
      SetBuzzer(2, false);
      SetBuzzer(3, true);
      timeOfNextBuzz = millis() + 350;
    }

    
  }
}


bool ServiceSpell(void)
{
  static unsigned long startTime;
  
  unsigned long timeInState;
  static bool spellComplete;
  static bool allDone;
  
  if (stateChanged)
  {
    SetLedColor(0, 0, 0);
    SetBuzzer(2, false);
    SetBuzzer(3, false);
    startWandMotionSampling = true;
    wandSamplingInProgress = true;
    movementPercentage = 0.0;

    startTime = millis();
      
    stateChanged = false;

    spellComplete = false;
    allDone = false;
  }

  timeInState = millis() - startTime;

  if (!spellComplete)
  {
    if (timeInState > 20000)
    {
      spellComplete = true;
    }
    else if ((timeInState > 15000) && (movementPercentage > 0.20))
    {
      spellComplete = true;
    }
    else if ((timeInState > 10000) && (movementPercentage > 0.30))
    {
      spellComplete = true;
    }
    else if ((timeInState > 7500) && (movementPercentage > 0.40))
    {
      spellComplete = true;
    }
    else if (movementPercentage > 0.50)
    {
      spellComplete = true;
    }
  }
  
  if (!allDone && spellComplete)
  {
    switch (currentState)
    {
      case WAIT_ON_PROHIBERE:
        SetLedColor(0, 255, 0);
        break;

      
      case WAIT_ON_AFFLICTO:
        SetLedColor(255, 0, 0);
        break;

      
      case WAIT_ON_FORTISSIMI:
        if (storedWandOwner == "Isaac")
        {
          SetLedColor(255, 125, 0);
        }
        break;

      
      case WAIT_ON_RISUS_MAGNA:
        if ((storedWandOwner == "Sam") || (storedWandOwner == "Erin") || (storedWandOwner == "Sariah") || (storedWandOwner == "Emma") || (storedWandOwner == "Hyrum"))
        {
          SetLedColor(125, 255, 0);
        }
        break;

      
      case WAIT_ON_LINGUA_GUSTARE:
        SetLedColor(125, 255, 255);
        break;

      
      case WAIT_ON_CANTATA_CANTICUM:
        if ((storedWandOwner == "Alexis") || (storedWandOwner == "Amber"))
        {
          SetLedColor(255, 0, 0);
        }
        
        break;

      
      case WAIT_ON_DENTIS_FORTIS:
        SetLedColor(255, 255, 255);
        break;
    }

    allDone = true;
  }

  return allDone;
}
