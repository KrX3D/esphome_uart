import esphome.config_validation as cv
import esphome.codegen as cg
from esphome.components import switch
from esphome import automation
from esphome.components.logger import LOG_LEVELS, is_log_level
from esphome.const import CONF_ID

# Configuration keys
CONF_ENABLE_UART_LOG = "enable_uart_log"
CONF_BAUD_RATE = "baud_rate"
CONF_TX_PIN = "tx_pin"
CONF_STRIP_COLORS = "strip_colors"
CONF_MIN_LEVEL = "min_level"
CONF_ALWAYS_FULL_LOGS = "always_full_logs"

uartlog_ns = cg.esphome_ns.namespace('uartlog')
UartLogComponent = uartlog_ns.class_('UartLogComponent', cg.Component)
UartLogSwitch = uartlog_ns.class_('UartLogSwitch', switch.Switch, cg.Component)

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

# Define a schema for the custom switch.
UARTLOG_SWITCH_SCHEMA = cv.Schema({
    cv.Required(CONF_ID): cv.use_id(UartLogComponent),
})

@switch.register_switch('uartlog_switch', UARTLOG_SWITCH_SCHEMA)
async def uartlog_switch_to_code(config, key, template_args):
    parent = await cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(config[CONF_ID], parent)
    cg.add(var.set_parent(parent))
    return var
