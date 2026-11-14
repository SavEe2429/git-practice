#include "blink_math.h"

namespace blink_math {

int add_numbers(int a, int b) {
  return a + b;
}

int clamp_interval(int interval_ms, int min_ms, int max_ms) {
  if (interval_ms < min_ms) {
    return min_ms;
  }
  if (interval_ms > max_ms) {
    return max_ms;
  }
  return interval_ms;
}

uint8_t next_led_state(uint8_t current_state) {
  return (current_state == 0) ? 1 : 0;
}

int calculate_cycle_ms(int on_ms, int off_ms) {
  int safe_on = clamp_interval(on_ms, 50, 10000);
  int safe_off = clamp_interval(off_ms, 50, 10000);
  return safe_on + safe_off;
}

}  // namespace blink_math
