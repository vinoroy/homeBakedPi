/*  espEnvNodeMock
   
    This is an ess node for environmental sensors where the sensor readings are mocked by random values. This code is for testing purposes.
 
   
*/
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
#include <DHT.h>


#define DHTPIN 14
#define DHTTYPE DHT22

int ldrPin = 12;

const char* ssid     = "VIDEOTRON3761";
const char* password = "3EEMTCVC333XA";

//const char* ssid     = "My ASUS";
//const char* password = "vino70mtl";


// DHT sensor
DHT dht(DHTPIN, DHTTYPE, 15);



ESP8266WebServer server(80);
 
 
float humidity, temp_f;  // Values read from sensor
String webString="";     // String to display
// Generally, you should use "unsigned long" for variables that hold time
unsigned long previousMillis = 0;        // will store last temp was read
const long interval = 2000;              // interval at which to read sensor
float randNumber;
 
void handle_root() {
  server.send(200, "text/plain", "Hello from the esp8266 envNodeMock, read from /temp /humid /baro /ldr ");
  delay(100);
}
 
void setup(void)
{
  // You can open the Arduino IDE Serial Monitor window to see what the code is doing
  Serial.begin(115200);  // Serial connection from ESP-01 via 3.3v console cable
  
  // Connect to WiFi network
  WiFi.begin(ssid, password);
  Serial.print("\n\r \n\rWorking to connect");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("DHT Weather Reading Server");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
   
  server.on("/", handle_root);
  
  server.on("/temp", [](){  // if you add this subdirectory to your webserver call, you get text below :)

    int temperature_data = (int)dht.readTemperature();
      
    webString="KITCHEN;TMP-1;"+String(temperature_data);   
    
    server.send(200, "text/plain", webString); // send to someones browser when asked
    Serial.println("sent the temp data");
  });

  server.on("/humid", [](){  // if you add this subdirectory to your webserver call, you get text below :)
  
    int humidity_data = (int)dht.readHumidity();

    webString="KITCHEN;HUMID-1;"+String(humidity_data);
    
    server.send(200, "text/plain", webString);               // send to someones browser when asked
    Serial.println("sent the humidity");
  });

  server.on("/ldr", [](){  // if you add this subdirectory to your webserver call, you get text below :)
    randNumber = random(0,999);

    int ldr_data = (unsigned int) analogRead(A0);
    
    webString="KITCHEN;LDR-1;"+String(ldr_data);
    
    server.send(200, "text/plain", webString);               // send to someones browser when asked
    Serial.println("sent the light");
  });

  
  server.begin();
  Serial.println("HTTP server started");
}
 
void loop(void)
{
  server.handleClient();
}



