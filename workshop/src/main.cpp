#include <Arduino.h>
#include "blink_math.h"

#ifndef LED_BUILTIN
#define LED_BUILTIN 2
#endif

static uint8_t led_state = LOW;
static int blink_interval_ms = 500;

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);

  blink_interval_ms = blink_math::clamp_interval(500);
  int sum = blink_math::add_numbers(2, 3);

  Serial.println("ESP32 DOIT DevKit v1 - Git & CI/CD Workshop");
  Serial.print("2 + 3 = ");
  Serial.println(sum);
  Serial.print("Blink interval (ms): ");
  Serial.println(blink_interval_ms);
}

void loop() {
  led_state = blink_math::next_led_state(led_state);
  digitalWrite(LED_BUILTIN, led_state);
  delay(blink_interval_ms);
}
