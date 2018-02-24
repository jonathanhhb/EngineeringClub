///Code for Controling a Tumbler RC car

// with Arduino Uno and Seeed Motor Shield V2.0

// Chris 8/12/14

/*----Ardunio to Shield Pinout Controls-----

Are using a Seeed motor shield to drive 2 DC motors

Seeed motor shield uses Arduino pins 8->13

Pin 9 sets the enable and speed of shield outputs 1 & 2

Pin 10 sets the enable and speed of shield outputs 3 & 4

Pin 8 from Uno controls the state of shield output 1

Pin 11 from Uno controls the state of shield output 2

Pin 12 from Uno controls the state of shield output 3

Pin 13 from Uno controls the state of shiled output 4

*/

//--- Declared variables

int leftmotorForward = 8; // pin 8 --- left motor (+) green wire
int leftmotorBackward = 11; // pin 11 --- left motor (-) black wire
int leftmotorspeed = 9; // pin 9 --- left motor speed signal
int rightmotorForward = 12; // pin 12 --- right motor (+) green wire
int rightmotorBackward = 13; // pin 13 --- right motor (-) black
int rightmotorspeed = 10; // pin 10 --- right motor speed signal

//--- Speeds and Timers
int Think = 2000; //Long delay time between steps
int Runtime = 5000; // How long Runtime actions will last
int Slow = 100; // slow speed (of 255 max)
int Fast = 255; // fast speed (of 255 max)
int Medium = 200;

//------------------------------------------------------
#define trigPin 3
#define echoPin 2


void setup() //---6 Pins being used are outputs--- 
{
  Serial.begin(115200);

  pinMode(leftmotorForward, OUTPUT);
  pinMode(leftmotorBackward, OUTPUT);
  pinMode(leftmotorspeed, OUTPUT);
  pinMode(rightmotorForward, OUTPUT);
  pinMode(rightmotorBackward, OUTPUT);
  pinMode(rightmotorspeed, OUTPUT);
  
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  turnRight();
}

// Add a function to read ultrasonic


float readUltraSonic(){
  int duration = 0;
  float distance = 0;
  digitalWrite(trigPin, LOW);  // Added this line
  delayMicroseconds(2); // Added this line
  digitalWrite(trigPin, HIGH);
//  delayMicroseconds(1000); - Removed this line
  delayMicroseconds(10); // Added this line
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration/2) / 29.1;  
  return distance;
}

// ---Main Program Loop -----------------------------
int dir = 1;

void loop()
{
  float distance = readUltraSonic();
  Serial.println( distance ); 
  if( distance > 30 || distance < 0 ){
    dir = 1-dir;
    if( dir == 1 )
    {
      turnRight();
      goForward();
      delay( 500 );
    }
    else
    {
      turnLeft();
      goForward();
      delay( 250 );
    }
  }
  else
  {
    turnLeft();
    goBackward();
    delay( 500 );
    Stop();
  }
  //delay(10);
  //turnLeft();
  //delay(5000);
  // go forward until ultrasonic says somethign is close then stop!
  //goForward();
  //turnRight();
  //goBackward();
  //delay(Runtime);
  //Stop();
  //delay(Think);
  //goBackward();
  //delay(Runtime);
}
void turnLeft(){
  analogWrite(leftmotorspeed,Medium);  
  digitalWrite(leftmotorBackward,LOW);
  digitalWrite(leftmotorForward,HIGH);
  delay(500);   
  digitalWrite(leftmotorForward,LOW); 
}

void turnRight(){
  analogWrite(leftmotorspeed,Medium);  
  digitalWrite(leftmotorForward,LOW);
  digitalWrite(leftmotorBackward,HIGH);
  delay(500);   
  digitalWrite(leftmotorBackward,LOW);
}

//----- "Sub-rutine" Voids called by the main loop
void goBackward()
{
  //analogWrite(leftmotorspeed,Fast); //Enable left motor by setting speed
  analogWrite(rightmotorspeed,Fast); //Enable left motor by setting speed
  //digitalWrite(leftmotorBackward,LOW); // Drives LOW outputs down first to avoid damage
  digitalWrite(rightmotorBackward,LOW);
  //digitalWrite(leftmotorForward,HIGH);
  digitalWrite(rightmotorForward,HIGH);
}

void goForward()
{
  //analogWrite(leftmotorspeed,Slow);  
  analogWrite(rightmotorspeed,Fast);
  //digitalWrite(leftmotorForward,LOW);
  digitalWrite(rightmotorForward,LOW);
  //digitalWrite(leftmotorBackward,HIGH);
  digitalWrite(rightmotorBackward,HIGH);
  //digitalWrite(rightmotorBackward,LOW);
}

void Stop() // Sets speed pins to LOW disabling both motors
{
//  digitalWrite(leftmotorspeed,LOW);
  digitalWrite(rightmotorspeed,LOW);
}
