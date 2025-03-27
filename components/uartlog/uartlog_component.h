#pragma once
#ifndef UARTLOG_COMPONENT_H_
#define UARTLOG_COMPONENT_H_

#include "esphome/core/component.h"
#include "esphome/core/defines.h"
#include "esphome/core/automation.h"
#ifdef USE_SWITCH
#include "esphome/components/switch/switch.h"
#endif

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

  // Setters that can be used by a custom switch or service
  void set_enable_uart_log(bool en) { this->enable_uart_log = en; }
  void set_baud_rate(uint32_t baud_rate) { this->baud_rate = baud_rate; }
  void set_tx_pin(uint8_t tx_pin) { this->tx_pin = tx_pin; }
  void set_strip_colors(bool strip) { this->strip_colors = strip; }

  // Optionally, if you want to ignore the min_level filtering
  void set_always_full_logs(bool always) { this->always_full_logs = always; }

 protected:
  bool strip_colors{true};
  bool enable_uart_log{true};
  bool always_full_logs{false};  // If true, bypass the min_level check.
  uint32_t baud_rate{115200};
  uint8_t tx_pin{1};
  int min_log_level{7}; // This is used to filter out lower priority logs.
#ifdef ESP32
  HardwareSerial *uart_{nullptr};
#elif defined(ESP8266)
  HardwareSerial *uart_{&Serial1};
#endif
};

#ifdef USE_SWITCH
class UartLogSwitch : public switch_::Switch, public Component {
 public:
  void set_parent(UartLogComponent *parent) { this->parent_ = parent; }
  void write_state(bool state) override {
    if (this->parent_ != nullptr) {
      this->parent_->set_enable_uart_log(state);
    }
    publish_state(state);
  }
 protected:
  UartLogComponent *parent_{nullptr};
};
#endif

// ... (your action class can remain unchanged)

}  // namespace uartlog
}  // namespace esphome

#endif
