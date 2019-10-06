

void ServiceCurrentState(void)
{
  switch(currentState)
  {
    case UNKNOWN_GAME_STATE:
      ServiceUnknownState();
      break;
      
    case WAITING_TO_START:
      ServiceWaitingToStart();
      break;

    case AT_ATTENTION:
      ServiceAtAttention();
      break;          
    
    case SMOKING:
      ServiceSmoking();
      break;
    
    case REGINAS_WARNING:
      ServiceReginasWarning();
      break;
    
    case WANDS_AT_THE_READY:
      ServiceWandsAtTheReady();
      break;
    
    case CHECK_FOR_POISONING:
      ServiceCheckForPoisoning();
      break;
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
  }
}


void ServiceWaitingToStart(void)
{
  if (stateChanged)
  {
    currentStateString = "WAITING_TO_START";
    Serial.println(currentStateString);
    stateChanged = false;

    SetLedColor(255, 0, 0);
  }
}


void ServiceAtAttention(void)
{
  if (stateChanged)
  {
    currentStateString = "AT ATTENTION";
    Serial.println(currentStateString);
    stateChanged = false;

    SetLedColor(0, 255, 0);
  }
}


void ServiceSmoking(void)
{
  if (stateChanged)
  {
    currentStateString = "SMOKING";
    Serial.println(currentStateString);
    stateChanged = false;

    SetLedColor(0, 0, 255);
  }
}


void ServiceReginasWarning(void)
{
  if (stateChanged)
  {
    currentStateString = "REGINA'S WARNING";
    Serial.println(currentStateString);
    stateChanged = false;

    SetLedColor(255, 255, 255);  
  }
}


void ServiceWandsAtTheReady(void)
{
  if (stateChanged)
  {
    currentStateString = "WANDS AT THE READY";
    Serial.println(currentStateString);
    stateChanged = false;
  }

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
}


void ServiceCheckForPoisoning(void)
{
  if (stateChanged)
  {
    currentStateString = "CHECK_FOR_POISONING";
    Serial.println(currentStateString);
    stateChanged = false;

    SetLedColor(0, 0, 0);  
  }
}
