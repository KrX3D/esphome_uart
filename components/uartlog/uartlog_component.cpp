#include "uartlog_component.h"
#include "esphome/core/log.h"
#include <regex>
#include <cstring>

#ifdef USE_LOGGER
#include "esphome/components/logger/logger.h"
#endif

namespace esphome {
namespace uartlog {

static const char *TAG = "uartlog";

#ifdef USE_LOGGER
// ESPHome 2026.x replaced add_on_log_callback(std::function) with
// add_log_callback(instance, fn-pointer, message_len). Pick whichever the logger has.
template<typename L>
static auto register_log_callback(L *logger, UartLogComponent *self, int)
    -> decltype(logger->add_log_callback(nullptr, nullptr), void()) {
  logger->add_log_callback(self, [](void *s, uint8_t level, const char *tag, const char *message, size_t len) {
    static_cast<UartLogComponent *>(s)->on_logger_message(level, tag, message, len);
  });
}

template<typename L>
static void register_log_callback(L *logger, UartLogComponent *self, long) {
  logger->add_on_log_callback([self](int level, const char *tag, const char *message) {
    self->on_logger_message(level, tag, message, strlen(message));
  });
}
#endif

void UartLogComponent::setup() {
  if (!this->enable_uart_log) {
    ESP_LOGI(TAG, "UART log disabled");
    // uart_ is not created yet on ESP32 when logging is disabled
    if (this->uart_ != nullptr)
      this->uart_->println("============================= UART log disabled =============================");
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
  this->uart_->println("============================= UART log started =============================");

  // Format the ESP_LOGI message and send it to UART
  std::string log_message = "UART log started on TX pin " + std::to_string(this->tx_pin) + 
                            " with baud " + std::to_string(this->baud_rate);
  this->uart_->println(log_message.c_str());
  
  ESP_LOGI(TAG, "UART log started on TX pin %d with baud %d", this->tx_pin, this->baud_rate);

#ifdef USE_LOGGER
  if (logger::global_logger != nullptr) {
    register_log_callback(logger::global_logger, this, 0);
  }
#endif
}

void UartLogComponent::on_logger_message(uint8_t level, const char *tag, const char *message, size_t message_len) {
  if (!this->enable_uart_log || (level > this->min_log_level))
    return;
  std::string final_message(message, message_len);
  // Strip "\033[0;xxm" (7 chars) at the start and "\033[0m" (4 chars) at the end
  if (this->strip_colors && final_message.size() > 11 && final_message[0] == '\033')
    final_message = final_message.substr(7, final_message.size() - 11);
  this->log(level, tag, final_message);
}

void UartLogComponent::loop() {
  // Nothing to do here.
}

void UartLogComponent::log(uint8_t level, const std::string &tag, const std::string &payload) {
  if (!this->enable_uart_log)
    return;

  std::string clean_payload = payload;  // Copy payload since it's const

  // Find and remove the second occurrence of [ ... ]
  size_t first_bracket = clean_payload.find('[');
  if (first_bracket != std::string::npos) {
    size_t second_bracket = clean_payload.find('[', first_bracket + 1);
    if (second_bracket != std::string::npos) {
      size_t closing_bracket = clean_payload.find(']', second_bracket);
      if (closing_bracket != std::string::npos) {
        // Remove the second [ ... ] completely
        clean_payload.erase(second_bracket, closing_bracket - second_bracket + 1);

        // Remove an optional ":" if it appears right after the second bracket
        if (clean_payload[second_bracket] == ':') {
          clean_payload.erase(second_bracket, 1);
        }
      }
    }
  }

  // Trim any extra spaces left after removal
  size_t first_char = clean_payload.find_first_not_of(" ");
  if (first_char != std::string::npos) {
    clean_payload = clean_payload.substr(first_char);
  }

  // Format the log message
  std::string out = "[" + tag + "] " + clean_payload;

  if (this->uart_ != nullptr) {
    this->uart_->println(out.c_str());
  }
}

}  // namespace uartlog
}  // namespace esphome
