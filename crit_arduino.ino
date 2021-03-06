// controls signals on critical Arduino
// receives info about state from Raspberry Pi

// from what I know, input voltage will be 12V from external battery,
// so Arduino just needs to act like a switch for certain components 
// and read in values from the IMU

float imu2data;
float imu2_accel_x;
float imu2_accel_y;
float imu2_accel_z;
float imu2_gyro_x;
float imu2_gyro_y;
float imu2_gyro_z;
bool thrust_valve_opened;
bool levitation_valve_opened;
bool high_speed_solenoid_engaged;
bool low_speed_solenoid_engaged;

bool newData = false;
int state;
char out;

const int imu2Pin = A0; // change based on which port sensor is plugged in to
const int thrustValvePin = 8;
const int levValvePin = 9;   

void setup() {
  pinMode(thrustValvePin, OUTPUT);
  pinMode(levValvePin, OUTPUT);
  //pinMode(imu2pin, INPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    state = Serial.read(); // read state from RPi over serial
    newData = true;        // set flag to allow Arduino to process new data
    Serial.print("/nCurrent state: ");
    Serial.println(state);
  }
  imu2Value = analogRead(imu2Pin); // read in values from imu2

  // State machine
  switch (state) {
  case 0: // “safe_to_approach”
    thrust_valve_opened = 0;          // turn thrust valve off
    levitation_valve_opened = 0;
    high_speed_solenoid_engaged = 0;
    low_speed_solenoid_engaged = 0;
    
    //digitalWrite(thrustValvePin, LOW); // necessary if supplying power from Arduino
    //digitalWrite(levValvePin, LOW);
    break;
  case 1: // “ready_to_launch”
    break;
  case 2: //“launching”
    break;
  case 3: //“coasting”
    break;
  case 4: //“braking”
    imu2();
    break;
  case 5: //“crawling”
    break;
  case 6: //“fault”
    thrust_valve_opened = 0;
    levitation_valve_opened = 0;
    high_speed_solenoid_engaged = 0;
    low_speed_solenoid_engaged = 0;
    break;
  default: 
    imu2_accel_x = 0;
    imu2_accel_y = 0;
    imu2_accel_z = 0;
    imu2_gyro_x = 0;
    imu2_gyro_z = 0;
    imu2_gyro_z = 0;
    thrust_valve_opened = 0;
    levitation_valve_opened = 0;
    high_speed_solenoid_engaged = 0;
    low_speed_solenoid_engaged = 0;
    break;  
  }
  imu2();
  out = send();
  Serial.println(out); // data that is being sent to RPi
  newData = false;     // clear newData flag
  delay(200); // delay .2 seconds --> change delay value based on RPi update speed
}

/*
char send()
 // send info to RPi
 // idk if this works at all...
 // this is probably more complicated than it needs to be, but hopefully easier for Rpi to parse 
{
  char a = char(imu2_accel_x);
  char b = char(imu2_accel_x);
  char c = char(imu2_accel_y);
  char d = char(imu2_accel_z);
  char e = char(imu2_gyro_x);
  char f = char(imu2_gyro_y);
  char g = char(imu2_gyro_z);
  char h = char(thrust_valve_opened);
  char i = char(levitation_valve_opened);
  char j = char(high_speed_solenoid_engaged);
  char k = char(low_speed_solenoid_engaged);
  
  char data[11] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k'};
  return data;
}
*/

void send(){
  Serial.print("/nAcceleration_x: ");
  Serial.println(imu2_accel_x);
  Serial.print("/nAcceleration_y: ");
  Serial.println(imu2_accel_y);
  Serial.print("/nAcceleration_z: ");
  Serial.println(imu2_accel_z);
  Serial.print("/nGyro_x: ");
  Serial.println(imu2_gyro_x);
  Serial.print("/nGyro_y: ");
  Serial.println(imu2_gyro_y);
  Serial.print("/nGyro_z: ");
  Serial.println(imu2_gyro_z);
}

void imu2()
 // gather data from imu about acceleration and gyro
{
  imu2data = analogread(imu2Pin);
}
