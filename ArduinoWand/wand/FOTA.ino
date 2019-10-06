#include <WiFi.h>
#include <ESPmDNS.h>
#include <WiFiUdp.h>
#include <ArduinoOTA.h>

long lastMsg = 0;
int flag = false;


void InitFOTA() {
  
  /* create a connection at port 3232 */
  ArduinoOTA.setPort(3232);

  /* we use mDNS instead of IP of ESP32 directly */
  //ArduinoOTA.setHostname("esp32");

  /* we set password for updating */
  ArduinoOTA.setPassword("iotsharing");

  /* this callback function will be invoked when updating start */
  ArduinoOTA.onStart([]() {
    Serial.println("Start updating");
    fotaInProgress = true;
    timeOfLastFotaActivity = millis();
  });

  /* this callback function will be invoked when updating end */
  ArduinoOTA.onEnd([]() {
    Serial.println("\nEnd updating");
    fotaInProgress = false;
  });
  
  /* this callback function will be invoked when a number of chunks of software was flashed
  so we can use it to calculate the progress of flashing */
  ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {
    Serial.printf("Progress: %u%%\r\n", (progress / (total / 100)));
    timeOfLastFotaActivity = millis();
  });

  /* this callback function will be invoked when updating error */
  ArduinoOTA.onError([](ota_error_t error) {
    Serial.printf("Error[%u]: ", error);
    if (error == OTA_AUTH_ERROR) Serial.println("Auth Failed");
    else if (error == OTA_BEGIN_ERROR) Serial.println("Begin Failed");
    else if (error == OTA_CONNECT_ERROR) Serial.println("Connect Failed");
    else if (error == OTA_RECEIVE_ERROR) Serial.println("Receive Failed");
    else if (error == OTA_END_ERROR) Serial.println("End Failed");
  });
  
  /* start updating */
  ArduinoOTA.begin();
}

void serviceFOTA() {
  /* this function will handle incoming chunk of SW, flash and respond sender */
  ArduinoOTA.handle();
}
