#include "uCOM.h"

uCOM M(2);

String test(){
  return "test";
}
String test2(){
  return "test";
}


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  M.Start();
  M.Addcommand("test", &test);
  M.Addcommand("test2", &test2);
}

void loop() {
  // put your main code here, to run repeatedly:
  M.HandleInput();
  delay(10);
}
