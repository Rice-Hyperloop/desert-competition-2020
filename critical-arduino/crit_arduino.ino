float imu2Value;
float imu2_accel_x;
float imu2_accel_y;
float imu2_accel_z;
float imu2_gyro_x;
float imu2_gyro_y;
float imu2_gyro_z;
boolean thrust_valve_opened;
boolean levitation_valve_opened;
boolean high_speed_solenoid_engaged;
boolean low_speed_solenoid_engaged;

int state;
char out;

const int imu2Pin = A0;
const int thrustValvePin = 8;
const int levValvePin = 9;

void setup() {
  pinMode(thrustValvePin, OUTPUT);
  pinMode(levValvePin, OUTPUT);
  //pinMode(imu2pin, INPUT);
  Serial.begin(9600);
}

void loop() {
  state = Serial.read(); // read state from RPi over serial
  imu2Value = analogRead(imu2Pin); // read in values from imu2

  // State machine
  switch (state) {
  case 0: // “safe_to_approach” = 0
    digitalWrite(thrustValvePin, LOW);
    digitalWrite(levValvePin, LOW);
    break;
  case 1: // “ready_to_launch” = 1
    break;
  case 2: //“launching” = 2
    break;
  case 3: //“coasting” = 3
    break;
  case 4: //“braking” = 4
    break;
  case 5: //“crawling” = 5
    break;
  case 6: //“fault” = 6
    digitalWrite(thrustValvePin, LOW);
    digitalWrite(levValvePin, LOW);
    break;
  }
  out = send();
  Serial.println(out);//data that is being Sent
  delay(200);
}

char send()
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

float imu2()
{
  //
}

boolean thrust_valve(){
  //
}

boolean levitation_valve(){
  //
}

boolean solenoid(){
  
}
