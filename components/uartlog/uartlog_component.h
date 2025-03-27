#pragma once
#ifndef UARTLOG_COMPONENT_H_
#define UARTLOG_COMPONENT_H_

#include "esphome/core/component.h"
#include "esphome/core/defines.h"
#include "esphome/core/log.h"      // Make sure this is included before using ESP_LOGCONFIG
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

 protected:
  bool enable_uart_log{true};
  bool strip_colors{true};
  uint32_t baud_rate{115200};
  uint8_t tx_pin{1};
  int min_log_level{7};
#ifdef ESP32
  HardwareSerial *uart_{nullptr};
#elif defined(ESP8266)
  HardwareSerial *uart_{&Serial1};
#endif
};

}  // namespace uartlog
}  // namespace esphome

#endif
