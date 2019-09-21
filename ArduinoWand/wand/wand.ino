#include <WiFi.h>


const char* ssid = "Dave";
const char* password = "553N280W";

const char* ANNOUNCEMENT_BCAST_ADDR = "255.255.255.255";
const int ANNOUNCEMENT_PORT = 10103;

const char* GADGET_BCAST_ADDR = "255.255.255.255";
const int WAND_PORT = 10109;

const char* WAND_OWNER = "Doug";




WiFiUDP udp;

int heartbeatRate = 5000;
String currentState = "UNKNOWN";


const int redLedPin = 33;
const int blueLedPin = 12;
const int greenLedPin = 15;

const int redPwmChannel = 0;
const int greenPwmChannel = 1;
const int bluePwmChannel = 2;

const int buzz1 = 2;
const int buzz2 = 4;
const int buzz3 = 26;




void setup()
{
  // Initilize hardware:
  Serial.begin(115200);

  InitBuzzers();
  
  InitLeds();

  InitComms();
}

void loop()
{
  SendHeartbeatIfNeeded();
}


void FormHeartbeat(String& heartbeat)
{
  static uint32_t messageId = 0;

  String subString;

  heartbeat = String(heartbeat + "<GADGET_MESSAGE>\n\r");
  
  heartbeat = String(heartbeat + "\t<MESSAGE_TYPE>GADGET_HEARTBEAT</MESSAGE_TYPE>\n\r");
  
  heartbeat = String(heartbeat + "\t<GADGET_ID>");
  subString = String(WAND_OWNER);
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

  heartbeat = String(heartbeat + "</GADGET_MESSAGE>\n\r");

  messageId += 1;
}

void SendHeartbeatIfNeeded(void)
{
  static unsigned long timeOfLastHeartbeatTx = 0;  
  
  unsigned long currentTime = millis();

  if (currentTime > (timeOfLastHeartbeatTx + heartbeatRate))
  {
    String heartbeat;
    int stringLength;

    FormHeartbeat(heartbeat);
    stringLength = heartbeat.length();

    Serial.println(heartbeat.c_str());
    
    udp.beginPacket(GADGET_BCAST_ADDR, WAND_PORT);
    udp.write((const uint8_t*)heartbeat.c_str(), stringLength);
    udp.endPacket();

    timeOfLastHeartbeatTx = currentTime;
  }
}




void InitComms(void)
{
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println(".");
  }
 
  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());

  udp.begin(WAND_PORT);
}


void InitLeds()
{
  // set lines to output

// setup each PWM channel
  ledcSetup(redPwmChannel, 5000, 8);
  ledcSetup(greenPwmChannel, 5000, 8);
  ledcSetup(bluePwmChannel, 5000, 8);

  // associate each output with a PWM channel
  ledcAttachPin(redLedPin, redPwmChannel);
  ledcAttachPin(greenLedPin, greenPwmChannel);
  ledcAttachPin(blueLedPin, bluePwmChannel);

}


void SetLedColor(uint8_t red, uint8_t green, uint8_t blue)
{
  ledcWrite(redPwmChannel, red);
  ledcWrite(greenPwmChannel, green);
  ledcWrite(bluePwmChannel, blue);
  
}


void InitBuzzers(void)
{
  pinMode (buzz1, OUTPUT);
  pinMode (buzz2, OUTPUT);
  pinMode (buzz3, OUTPUT);
}


void SetBuzzer(uint8_t buzzerIndex, uint8_t turnOn)
{
  if (buzzerIndex == 1)
  {
    if (turnOn == 1)
    {
      digitalWrite (buzz1, HIGH);
    }
    else
    {
      digitalWrite (buzz1, LOW);
    }
  }

  if (buzzerIndex == 2)
  {
    if (turnOn == 1)
    {
      digitalWrite (buzz2, HIGH);
    }
    else
    {
      digitalWrite (buzz2, LOW);
    }
  }


  if (buzzerIndex == 3)
  {
    if (turnOn == 1)
    {
      digitalWrite (buzz3, HIGH);
    }
    else
    {
      digitalWrite (buzz3, LOW);
    }
  }


}
