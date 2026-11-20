/**
 * @file test_hardware.cpp
 * @brief ไฟล์เริ่มต้น (Starter) สำหรับเขียน Test บนบอร์ด DOIT ESP32 DevKit v1 จริง
 *
 * อ้างอิงคู่มือ: exercises/labs/LAB04-PlatformIO_Unit_Testing.pdf (Module 4: Unit Testing บน PlatformIO)
 * อ้างอิงโจทย์: exercises/exercises.md (Module 4)
 */

#include <Arduino.h>
#include <unity.h>
#include "blink_math.h"

#ifndef LED_BUILTIN
#define LED_BUILTIN 2
#endif

// 1. setUp(): เตรียมขา GPIO ก่อนรันแต่ละ Test Case บนบอร์ดจริง
void setUp(void) { pinMode(LED_BUILTIN, OUTPUT); }

// 2. tearDown(): ปิดไฟ LED หลังจบแต่ละ Test Case
void tearDown(void) { digitalWrite(LED_BUILTIN, LOW); }

// 3. Test Case บนฮาร์ดแวร์จริง
// TODO (แบบฝึกหัด Module 4): เพิ่ม Test Case ทดสอบการทำงานของ LED หรือขา GPIO
void test_hardware_starter_example(void) {
  TEST_ASSERT_EQUAL_UINT8(HIGH, blink_math::next_led_state(LOW));
}

// 4. setup() / loop(): จุดเริ่มต้นของ Unity Runner บนบอร์ด ESP32
void setup() {
  delay(2000);  // รอ Serial Monitor เชื่อมต่อหลังรีเซ็ตบอร์ด
  UNITY_BEGIN();
  RUN_TEST(test_hardware_starter_example);
  UNITY_END();
}

void loop() {}
