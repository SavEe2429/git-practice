#include <Arduino.h>
#include <unity.h>
#include "blink_math.h"

#ifndef LED_BUILTIN
#define LED_BUILTIN 2
#endif

void setUp(void) {
  pinMode(LED_BUILTIN, OUTPUT);
}

void tearDown(void) {
  digitalWrite(LED_BUILTIN, LOW);
}

void test_led_pin_toggle_hardware(void) {
  uint8_t state = blink_math::next_led_state(LOW);
  digitalWrite(LED_BUILTIN, state);
  delay(50);
  TEST_ASSERT_EQUAL_UINT8(HIGH, state);
}

void setup() {
  delay(2000);
  UNITY_BEGIN();
  RUN_TEST(test_led_pin_toggle_hardware);
  UNITY_END();
}

void loop() {}
