
int NUM=5;

void setup() {
  Serial.begin(115200);
}
void loop() {
  if(Serial.available() > 0) {
    int data = Serial.read();
    Serial.write(data);
  }
}
