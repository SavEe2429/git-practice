/**
 * @file test_main.cpp
 * @brief ไฟล์เริ่มต้น (Starter) สำหรับเขียน Unit Test ด้วย Unity บน [env:native]
 *
 * อ้างอิงคู่มือ: docs/workshop-manual.pdf (Module 4: Unit Testing บน PlatformIO)
 * อ้างอิงโจทย์: exercises/exercises.md (Module 4)
 * ไฟล์เฉลย:   exercises/solutions/test/test_native/test_main.cpp
 */

#include <unity.h>
#include "blink_math.h"

// 1. setUp(): ฟังก์ชันที่รันอัตโนมัติ "ก่อน" เริ่มแต่ละ Test Case (ใช้เตรียมค่าเริ่มต้น)
void setUp(void) {}

// 2. tearDown(): ฟังก์ชันที่รันอัตโนมัติ "หลัง" จบแต่ละ Test Case (ใช้คืนค่า/เคลียร์ทรัพยากร)
void tearDown(void) {}

// 3. Test Case ตัวอย่าง: ทดสอบฟังก์ชันจาก lib/blink_math/
// TODO (แบบฝึกหัด Module 4): เขียน Test Cases เพิ่มเติม เช่น
//   - test_add_numbers_positive
//   - test_clamp_interval_bounds
//   - test_next_led_state_toggles
//   - test_calculate_cycle_ms
void test_starter_example(void) { TEST_ASSERT_EQUAL_INT(5, blink_math::add_numbers(2, 3)); }

// 4. main(): จุดเริ่มต้นของ Native Test Runner (รันบน PC / GitHub Actions CI)
int main(int argc, char** argv) {
  UNITY_BEGIN();
  RUN_TEST(test_starter_example);
  // TODO: เรียก RUN_TEST(...) สำหรับ Test Case ที่คุณเขียนเพิ่มตรงนี้
  return UNITY_END();
}
