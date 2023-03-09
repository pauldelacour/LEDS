#include <FastLED.h>
#define NUM_LEDS 255
#define DATA_PIN 2 //How boring and obvious!
#define COLOR_ORDER GRB //Green (G), Red (R), Blue (B)
#define CHIPSET WS2812B
#define BRIGHTNESS 25
#define VOLTS 5
#define MAX_AMPS 500 //value in milliamps

//ENOUGH NONSENSE!
void printArray ( const int [][ 2 ] );
CRGB leds[NUM_LEDS];
int RAND1;
int RAND2;
int RAND3;
int incomingByte; // for incoming serial data

const int X= 4;
const int Y = 4;
int pin[X][Y];


void setup() {
  for (int i =0; i < X; i++) {
    for (int j =0; j < Y; j++) {
      pin[i][j] = int(i*X+j);
    }
  }
  

FastLED.addLeds<CHIPSET,DATA_PIN,COLOR_ORDER>(leds,NUM_LEDS);
FastLED.setMaxPowerInVoltsAndMilliamps(VOLTS,MAX_AMPS);
FastLED.setBrightness(BRIGHTNESS);
FastLED.clear();
FastLED.show(); 
Serial.begin(115200); // opens serial port, sets data rate to 115200 bps
//JONNY FIVE IS ALIVE!!!!!!!!!!!!!!!!!!!!
}

void loop() {
  for(int j = 0; j< Y; j++){
    for(int i=0;  i<X; i++){
      leds[pin[i][j]]= CRGB(204,204,0);
      //leds[pin[i,j]] =  CRGB(204,204,0);
      FastLED.show();
      delay(1000); 
    }
  }
  //printArray(pin) ;  
  // put your main code here, to run repeatedly:
}

void printArray( const int a[][ Y ] ) {
   // loop through array's rows
   for ( int i = 0; i < X; ++i ) {
      // loop through columns of current row
      for ( int j = 0; j < Y; ++j )
        Serial.print (a[ i ][ j ] );
      //Serial.print (“\r” ) ; // start new line of output
   } 
// end outer for
} 

