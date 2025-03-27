#include "uartlog_component.h"
#include "esphome/core/log.h"

#ifdef USE_LOGGER
#include "esphome/components/logger/logger.h"
#endif

namespace esphome {
namespace uartlog {


static const char *TAG = "uartlog_switch.switch";
static const char *TAG = "uartlog";

void UartLogComponent::setup() {
  if (!this->enable_uart_log) {
    ESP_LOGI(TAG, "UART log disabled");
    return;
  }
#ifdef ESP32
  // For ESP32, create a new hardware serial instance on UART1.
  // For TX-only operation, we pass -1 for the RX pin.
  this->uart_ = new HardwareSerial(1);
  this->uart_->begin(this->baud_rate, SERIAL_8N1, -1, this->tx_pin);
#elif defined(ESP8266)
  // On ESP8266, Serial1 TX is fixed so we simply begin with the baud rate.
  this->uart_->begin(this->baud_rate);
#endif
  // Send an initial message on UART and print to logger.
  this->uart_->println("##################################");
  this->uart_->println("##################################");
  this->uart_->println("##########UART Log started########");
  this->uart_->println("##################################");
  this->uart_->println("##################################");
  ESP_LOGI(TAG, "UART Log started on TX pin %d with baud %d", this->tx_pin, this->baud_rate);

#ifdef USE_LOGGER
  if (logger::global_logger != nullptr) {
    logger::global_logger->add_on_log_callback([this](int level, const char *tag, const char *message) {
      if (!this->enable_uart_log || (level > this->min_log_level))
        return;
      std::string final_message;
      if (this->strip_colors) {
        std::string org_msg(message);
        if (org_msg.size() > 11)
          final_message = org_msg.substr(7, org_msg.size() - 11);
        else
          final_message = org_msg;
      } else {
        final_message = message;
      }
      this->log(level, tag, final_message);
    });
  }
#endif
}

void UartLogComponent::loop() {
  // Nothing to do here.
}

void UartLogComponent::log(uint8_t level, const std::string &tag, const std::string &payload) {
  if (!this->enable_uart_log)
    return;
  // Format the log message.
  std::string out = "[" + tag + "] " + payload;
  if (this->uart_ != nullptr) {
    this->uart_->println(out.c_str());
  }
}

void UartLogComponent::dump_config(){
    ESP_LOGCONFIG(TAG, "Empty custom switch");
}

}  // namespace uartlog
}  // namespace esphome
