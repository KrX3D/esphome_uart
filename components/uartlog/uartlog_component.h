#pragma once
#ifndef UARTLOG_COMPONENT_H_
#define UARTLOG_COMPONENT_H_

#include "esphome/core/component.h"
#include "esphome/core/defines.h"
#include "esphome/core/automation.h"
#include "esphome/core/log.h"
#include "esphome/core/version.h"

#ifdef ESP32
  #include "HardwareSerial.h"
#elif defined(ESP8266)
  #include <Arduino.h>   // For Serial1 on ESP8266 (note: TX pin is fixed)
#endif

// ESPHome 2025.11.0 changed Action::play(Ts... x) to play(const Ts &...x)
#if ESPHOME_VERSION_CODE >= VERSION_CODE(2025, 11, 0)
#define UARTLOG_PLAY_ARGS const Ts &...x
#else
#define UARTLOG_PLAY_ARGS Ts... x
#endif

namespace esphome {
namespace uartlog {

class UartLogComponent : public Component {
 public:
  UartLogComponent() {}

  // Component methods
  void setup() override;
  void loop() override;
  float get_setup_priority() const override { return setup_priority::AFTER_WIFI; }

  // Setters for configuration options
  void set_baud_rate(uint32_t baud_rate) { this->baud_rate = baud_rate; }
  void set_tx_pin(uint8_t tx_pin) { this->tx_pin = tx_pin; }
  void set_enable_uart_log(bool en) { this->enable_uart_log = en; }
  void set_min_log_level(int log_level) { this->min_log_level = log_level; }
  void set_strip_colors(bool strip_colors) { this->strip_colors = strip_colors; }

  // The log function that outputs via UART
  void log(uint8_t level, const std::string &tag, const std::string &payload);

  // Handles a message received from the ESPHome logger
  void on_logger_message(uint8_t level, const char *tag, const char *message, size_t message_len);

 protected:
  bool strip_colors{true};
  bool enable_uart_log{true};
  uint32_t baud_rate{115200};
  uint8_t tx_pin{1};
  int min_log_level{7}; // default, note: lower values mean higher priority
#ifdef ESP32
  HardwareSerial *uart_{nullptr};
#elif defined(ESP8266)
  // On ESP8266, Serial1 is used (TX only, fixed pin)
  HardwareSerial *uart_{&Serial1};
#endif
};

// An automation action to trigger a UART log manually.
template<typename... Ts> class UartLogAction : public Action<Ts...> {
 public:
  UartLogAction(UartLogComponent *parent) : parent_(parent) {}
  TEMPLATABLE_VALUE(uint8_t, level)
  TEMPLATABLE_VALUE(std::string, tag)
  TEMPLATABLE_VALUE(std::string, payload)

  void play(UARTLOG_PLAY_ARGS) override {
    this->parent_->log(this->level_.value(x...), this->tag_.value(x...), this->payload_.value(x...));
  }

 protected:
  UartLogComponent *parent_;
};

}  // namespace uartlog
}  // namespace esphome

#endif
