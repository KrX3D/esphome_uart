#pragma once
#ifndef UARTLOG_COMPONENT_H_
#define UARTLOG_COMPONENT_H_

#include "esphome/core/component.h"
#include "esphome/core/defines.h"
#include "esphome/components/switch/switch.h"

#ifdef ESP32
  #include "HardwareSerial.h"
#elif defined(ESP8266)
  #include <Arduino.h>
#endif

namespace esphome {
namespace uartlog {

class UartLogComponent : public Component {
 public:
  UartLogComponent() {}

  float get_setup_priority() const override { return setup_priority::AFTER_WIFI; }
  void setup() override;
  void loop() override;
  void log(uint8_t level, const std::string &tag, const std::string &payload);

  // Setters for configuration options
  void set_enable_uart_log(bool en) { this->enable_uart_log = en; }
  void set_baud_rate(uint32_t baud_rate) { this->baud_rate = baud_rate; }
  void set_tx_pin(uint8_t tx_pin) { this->tx_pin = tx_pin; }
  void set_strip_colors(bool strip) { this->strip_colors = strip; }
  void set_min_log_level(int log_level) { this->min_log_level = log_level; }
  void set_always_full_logs(bool always) { this->always_full_logs = always; }

  // Public so our switch can read its state if desired.
  bool enable_uart_log{true};

 protected:
  bool strip_colors{true};
  bool always_full_logs{false};  // If true, bypass min_level filtering.
  uint32_t baud_rate{115200};
  uint8_t tx_pin{1};
  int min_log_level{7}; // Used to filter out lower-priority logs.
#ifdef ESP32
  HardwareSerial *uart_{nullptr};
#elif defined(ESP8266)
  HardwareSerial *uart_{&Serial1};
#endif
};

// Custom switch to toggle UART logging.
// This is defined in the same header as the component.
class UartLogSwitch : public switch_::Switch, public Component {
 public:
  void set_parent(UartLogComponent *parent) { this->parent_ = parent; }
  void setup() override { }
  void write_state(bool state) override {
    if (this->parent_ != nullptr) {
      this->parent_->set_enable_uart_log(state);
    }
    publish_state(state);
  }
  void dump_config() override {
    ESP_LOGCONFIG("uartlog.switch", "UART Log Switch");
  }
 protected:
  UartLogComponent *parent_{nullptr};
};

}  // namespace uartlog
}  // namespace esphome

#endif
