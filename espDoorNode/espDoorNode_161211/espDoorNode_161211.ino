/*  espDoorNode
   
    This the code for an esp door node. This node contains
 
   
*/

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

// door switch assignments
const int doorPin = 13;     

long debouncingTimeDoor = 15; //Debouncing Time in Milliseconds
volatile unsigned long lastTimeMicrosDoor;

int doorOpenState = 0;
int doorMsgSentState = 1;

// pir motion detection assignments
const int pirPin = 12;     

long timeDelaySecondsPir = 15; //time delay in seconds between events
volatile unsigned long lastTimeSecondsPir;

int pirMotionDetectedState = 0;
int pirMotionMsgSentState = 1;

String webString=""; 

// wifi connection and server assignments
const char* ssid     = "VIDEOTRON3761";
const char* password = "3EEMTCVC333XA";

const char* host = "192.168.0.122"; // adresse to the homeBakedPi web api

ESP8266WebServer server(80);

   
void handle_root() {
  server.send(200, "text/plain", "Hello from the esp8266 envNodeMock, read from /door /motion ");
  delay(100);
}

 
void setup(void)
{
  
  Serial.begin(115200);

  // door setup
  pinMode(doorPin, INPUT);
  attachInterrupt(doorPin, doorEvent, RISING);

  // pir motion setup
  pinMode(pirPin, INPUT);
  attachInterrupt(pirPin, pirEvent, RISING);
  
  
  // Connect to WiFi network
  WiFi.begin(ssid, password);
  Serial.print("\n\r \n\rWorking to connect");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
   
  server.on("/", handle_root);
  
  server.on("/door", [](){
    int pinState = digitalRead(doorPin);
    int doorState = 0;

    // door open must produce a 1
    if (pinState == 1){
      doorState = 0;
    }
    else if (pinState == 0){
      doorState = 1;
    }

    webString="ENTRANCE;SW-1;"+String(doorState);
    server.send(200, "text/plain",webString);      
    Serial.println("sent the door open state ");
  });

  server.on("/motion", [](){
    validatePirMotionDetectedState();
    webString="ENTRANCE;MD-1;"+String(pirMotionDetectedState);
    server.send(200, "text/plain",webString);      
    Serial.println("sent the door open state ");
  });

  
  server.begin();
  Serial.println("HTTP server started");
}

 
void loop(void)
{
  server.handleClient();

  validatePirMotionDetectedState();

  if (doorOpenState == 1 and doorMsgSentState == 0){

    sendEventToWebAPI("ENTRANCE;SW-1;1","doorOpening"); 
  }

  if (pirMotionDetectedState == 1 and pirMotionMsgSentState == 0){

    sendEventToWebAPI("ENTRANCE;MD-1;1","pirMotionDetected"); 
  }
  
}


void doorEvent() {

  Serial.println("door interupt detected");

  if((long)(micros() - lastTimeMicrosDoor) >= debouncingTimeDoor * 1000) {
    
    lastTimeMicrosDoor = micros();

    Serial.println("door event detected");

    doorOpenState = 1;
    doorMsgSentState = 0;
      
  }
}

void pirEvent() {

  long curTimeSecondsPir = millis()/1000;
  
  if((long)(curTimeSecondsPir - lastTimeSecondsPir) >= timeDelaySecondsPir) {

    Serial.print("Current time : ");
    Serial.println(curTimeSecondsPir);
    
    Serial.print("Last time : ");
    Serial.println(lastTimeSecondsPir);
    
    Serial.print("Diff : ");
    long diff = curTimeSecondsPir - lastTimeSecondsPir;
    Serial.println(diff);

    lastTimeSecondsPir = millis()/1000;

    pirMotionDetectedState = 1;
    pirMotionMsgSentState = 0;

    Serial.println("motion event detected");

  }
}


void sendEventToWebAPI(String eventMsg, String eventType)
{

  Serial.print("connecting to ");
  Serial.println(host);
  
  // Use WiFiClient class to create TCP connections
  WiFiClient client;
  const int httpPort = 80;
  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return;
  }
  
  // We now create a URI for the request
  String url = "/insertSensorValue/" + eventMsg;
  Serial.print("Requesting URL: ");
  Serial.println(url);
  
  // This will send the request to the server
  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" + 
               "Connection: close\r\n\r\n");
  delay(500);
  
  // Read all the lines of the reply from server and print them to Serial
  Serial.println("Reading response from web api");
  while(client.available()){
    String line = client.readStringUntil('\r');
    Serial.print(line);  
  }
  Serial.println("");
 
  if (eventType == "doorOpening"){

    doorMsgSentState = 1;
    
  }
  else if (eventType == "pirMotionDetected"){

    pirMotionMsgSentState = 1;
    
  }
 
}


void validatePirMotionDetectedState(){

  long curTimeSecondsPir = millis()/1000;

  if(((long)(curTimeSecondsPir - lastTimeSecondsPir) >= timeDelaySecondsPir) and (pirMotionDetectedState == 1)) {

    pirMotionDetectedState = 0;

    Serial.println("No motion detected");
        
  }
  
}





