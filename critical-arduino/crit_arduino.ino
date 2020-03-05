void setup() {
  Serial.begin(9600);
}

void loop() {
  state = Serial.read();
  // “safe_to_approach” = 0
// “ready_to_launch” = 1
//“launching” = 2
//“coasting” = 3
//“braking” = 4
//“crawling” = 5
//“fault” = 6

  switch (state) {
  case 0:
  //
  break;
  case 1:
  break;
  case 2:
  break;
  case 3:
  break;
  case 4:
  break;
  case 5:
  break;
  case 6:
  break;
  }
  Serial.println(data);//data that is being Sent
  delay(200);
}

void send(string s)
{
  //
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
imu2_accel_x (float)
imu2_accel_y (float)
imu2_accel_z (float)
imu2_gyro_x (float)
imu2_gyro_y (float)
imu2_gyro_z (float)
thrust_valve_opened (boolean)
levitation_valve_opened (boolean)
high_speed_solenoid_engaged (boolean)
 low_speed_solenoid_engaged (boolean)
