import esphome.config_validation as cv
import esphome.codegen as cg
from esphome.components.logger import LOG_LEVELS, is_log_level
from esphome.const import CONF_ID
from esphome import automation

# Configuration keys for our uartlog component.
CONF_ENABLE_UART_LOG = "enable_uart_log"
CONF_BAUD_RATE = "baud_rate"
CONF_TX_PIN = "tx_pin"
CONF_STRIP_COLORS = "strip_colors"
CONF_MIN_LEVEL = "min_level"
CONF_ALWAYS_FULL_LOGS = "always_full_logs"

uartlog_ns = cg.esphome_ns.namespace('uartlog')
UartLogComponent = uartlog_ns.class_('UartLogComponent', cg.Component)

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(UartLogComponent),
    cv.Optional(CONF_ENABLE_UART_LOG, default=True): cv.boolean,
    cv.Optional(CONF_BAUD_RATE, default=115200): cv.positive_int,
    cv.Optional(CONF_TX_PIN, default=1): cv.int_range(min=0, max=40),
    cv.Optional(CONF_STRIP_COLORS, default=True): cv.boolean,
    cv.Optional(CONF_MIN_LEVEL, default="DEBUG"): is_log_level,
    cv.Optional(CONF_ALWAYS_FULL_LOGS, default=False): cv.boolean,
})

def to_code(config):
    var = cg.new_Pvariable(config[cv.GenerateID()])
    cg.add(var.set_enable_uart_log(config[CONF_ENABLE_UART_LOG]))
    cg.add(var.set_baud_rate(config[CONF_BAUD_RATE]))
    cg.add(var.set_tx_pin(config[CONF_TX_PIN]))
    cg.add(var.set_strip_colors(config[CONF_STRIP_COLORS]))
    cg.add(var.set_min_log_level(LOG_LEVELS[config[CONF_MIN_LEVEL]]))
    cg.add(var.set_always_full_logs(config[CONF_ALWAYS_FULL_LOGS]))
    yield var

#
# Register a custom service to set (toggle) the UART logging at runtime.
#
UARTLOG_SERVICE_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.use_id(UartLogComponent),
    cv.Required("enable"): cv.boolean,
})

@automation.register_service("uartlog.set_enabled", UARTLOG_SERVICE_SCHEMA, name="Set UART Log Enabled")
def uartlog_set_enabled_to_code(config, action_id, template_arg, args):
    parent = yield cg.get_variable(config[cv.GenerateID()])
    templ = yield cg.templatable(config["enable"], args, cg.bool_)
    cg.add(parent.set_enable_uart_log(templ))
    yield
