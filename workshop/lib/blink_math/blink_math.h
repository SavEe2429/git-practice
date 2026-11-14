#ifndef BLINK_MATH_H
#define BLINK_MATH_H

#include <stdint.h>

namespace blink_math {

/// Adds two integers (simple pure-logic helper for unit testing).
int add_numbers(int a, int b);

/// Clamps a blink interval (in ms) between min_ms and max_ms.
int clamp_interval(int interval_ms, int min_ms = 100, int max_ms = 5000);

/// Returns the next LED state (0 or 1) given the current state.
uint8_t next_led_state(uint8_t current_state);

/// Calculates total cycle period (ON + OFF) in milliseconds.
int calculate_cycle_ms(int on_ms, int off_ms);

}  // namespace blink_math

#endif  // BLINK_MATH_H
