/*************************************************************
Motor Shield 2-Channel DC Motor Demo
by Randy Sarafan

For more information see:
https://www.instructables.com/id/Arduino-Motor-Shield-Tutorial/

*************************************************************/

#define CHAN_A_BRAKE 9
#define CHAN_A_SPEED 3
#define CHAN_A_DIRECTION 12 //


#define CHAN_B_BRAKE 8
#define CHAN_B_SPEED 11
#define CHAN_B_DIRECTION 13 // HIGH fwd, LOW backward

void setup() {
  
  //Setup Channel A
  pinMode(12, OUTPUT); //Initiates Motor Channel A pin
  pinMode(9, OUTPUT); //Initiates Brake Channel A pin

  //Setup Channel B
  pinMode(13, OUTPUT); //Initiates Motor Channel A pin
  pinMode(8, OUTPUT);  //Initiates Brake Channel A pin

  Serial.begin( 115200 );
  
}

// Assuming A=drive & B=steering

void Forward( int speed )
{
  //Motor A forward @ full speed
  digitalWrite(CHAN_A_DIRECTION, LOW); //Establishes forward direction of Channel A
  digitalWrite(CHAN_A_BRAKE, LOW);   //Disengage the Brake for Channel A
  analogWrite(CHAN_A_SPEED, speed);   //Spins the motor on Channel A at full speed
}

void Backward( int speed )
{
  //Motor A forward @ full speed
  digitalWrite(CHAN_A_DIRECTION, HIGH); //Establishes backward direction of Channel A
  digitalWrite(CHAN_A_BRAKE, LOW);   //Disengage the Brake for Channel A
  analogWrite(CHAN_A_SPEED, speed);   //Spins the motor on Channel A at full speed
}

void FwdRight( int speed )
{
  //Motor A forward @ full speed
  digitalWrite(CHAN_A_DIRECTION, LOW); //Establishes forward direction of Channel A
  digitalWrite(CHAN_B_DIRECTION, LOW);  //Establishes backward direction of Channel B

  digitalWrite(CHAN_A_BRAKE, LOW);   //Disengage the Brake for Channel A
  digitalWrite(CHAN_B_BRAKE, LOW);   //Disengage the Brake for Channel B

  analogWrite(CHAN_B_SPEED, 255);     //Spins the motor on Channel B at half speed
  analogWrite(CHAN_A_SPEED, speed);   //Spins the motor on Channel A at full speed
}

void FwdLeft( int speed )
{
  //Motor A forward @ full speed
  digitalWrite(CHAN_A_DIRECTION, LOW); //Establishes forward direction of Channel A
  digitalWrite(CHAN_B_DIRECTION, HIGH);  //Establishes backward direction of Channel B

  digitalWrite(CHAN_A_BRAKE, LOW);   //Disengage the Brake for Channel A
  digitalWrite(CHAN_B_BRAKE, LOW);   //Disengage the Brake for Channel B

  analogWrite(CHAN_B_SPEED, 255);     //Spins the motor on Channel B at half speed
  analogWrite(CHAN_A_SPEED, speed);   //Spins the motor on Channel A at full speed
}

void BackwdRight( int speed )
{
  //Motor A forward @ full speed
  digitalWrite(CHAN_A_DIRECTION, HIGH); //Establishes forward direction of Channel A
  digitalWrite(CHAN_B_DIRECTION, LOW);  //Establishes backward direction of Channel B

  digitalWrite(CHAN_A_BRAKE, LOW);   //Disengage the Brake for Channel A
  digitalWrite(CHAN_B_BRAKE, LOW);   //Disengage the Brake for Channel B

  analogWrite(CHAN_B_SPEED, 255);     //Spins the motor on Channel B at half speed
  analogWrite(CHAN_A_SPEED, speed);   //Spins the motor on Channel A at full speed
}

void BackwdLeft( int speed )
{
  //Motor A forward @ full speed
  digitalWrite(CHAN_A_DIRECTION, HIGH); //Establishes forward direction of Channel A
  digitalWrite(CHAN_B_DIRECTION, HIGH);  //Establishes backward direction of Channel B

  digitalWrite(CHAN_A_BRAKE, LOW);   //Disengage the Brake for Channel A
  digitalWrite(CHAN_B_BRAKE, LOW);   //Disengage the Brake for Channel B

  analogWrite(CHAN_B_SPEED, 255);     //Spins the motor on Channel B at half speed
  analogWrite(CHAN_A_SPEED, speed);   //Spins the motor on Channel A at full speed
}

void Stop()
{
  digitalWrite(CHAN_A_BRAKE, HIGH);  //Engage the Brake for Channel A
}

void Straighten()
{
  digitalWrite(CHAN_B_BRAKE, HIGH);  //Engage the Brake for Channel A
}

void TurnRight()
{
  //Motor B backward @ half speed
  digitalWrite(CHAN_B_DIRECTION, LOW);  //Establishes backward direction of Channel B
  digitalWrite(CHAN_B_BRAKE, LOW);   //Disengage the Brake for Channel B
  analogWrite(CHAN_B_SPEED, 255);    //Spins the motor on Channel B at half speed
}

void TurnLeft()
{
  //Motor B backward @ half speed
  digitalWrite(CHAN_B_DIRECTION, HIGH);  //Establishes backward direction of Channel B
  digitalWrite(CHAN_B_BRAKE, LOW);   //Disengage the Brake for Channel B
  analogWrite(CHAN_B_SPEED, 255);    //Spins the motor on Channel B at half speed
}

void loop()
{
  FwdRight( 200 );
  delay( 1000 );
  Stop();  
  delay( 1000 );

  FwdLeft( 200 );
  delay( 1000 );
  Stop();  
  delay( 1000 );

  BackwdLeft( 200 );
  delay( 1000 );
  Stop();  
  delay( 1000 );

  BackwdRight( 200 );
  delay( 1000 );
  Stop();  
  delay( 1000 );

}

void loop2(){
  //Motor A forward @ full speed
  digitalWrite(12, HIGH); //Establishes forward direction of Channel A
  digitalWrite(9, LOW);   //Disengage the Brake for Channel A
  analogWrite(3, 255);   //Spins the motor on Channel A at full speed

  //Motor B backward @ half speed
  digitalWrite(13, LOW);  //Establishes backward direction of Channel B
  digitalWrite(8, LOW);   //Disengage the Brake for Channel B
  analogWrite(11, 123);    //Spins the motor on Channel B at half speed

  
  delay(3000);

  
  digitalWrite(9, HIGH);  //Engage the Brake for Channel A
  digitalWrite(9, HIGH);  //Engage the Brake for Channel B


  delay(1000);
  
  
  //Motor A forward @ full speed
  digitalWrite(12, LOW);  //Establishes backward direction of Channel A
  digitalWrite(9, LOW);   //Disengage the Brake for Channel A
  analogWrite(3, 123);    //Spins the motor on Channel A at half speed
  
  //Motor B forward @ full speed
  digitalWrite(13, HIGH); //Establishes forward direction of Channel B
  digitalWrite(8, LOW);   //Disengage the Brake for Channel B
  analogWrite(11, 255);   //Spins the motor on Channel B at full speed
  
  delay(3000);
  
  digitalWrite(9, HIGH);  //Engage the Brake for Channel A
  digitalWrite(9, HIGH);  //Engage the Brake for Channel B
  
  delay(1000); 
}

