import esphome.config_validation as cv
import esphome.codegen as cg
from esphome import automation
from esphome.components.logger import LOG_LEVELS, is_log_level

# These names are not defined in the core so we use literal strings.
CONF_BAUD_RATE = "baud_rate"
CONF_TX_PIN = "tx_pin"
CONF_ENABLE_UART_LOG = "enable_uart_log"
CONF_STRIP_COLORS = "strip_colors"
CONF_MIN_LEVEL = "min_level"

DEPENDENCIES = ['logger']

uartlog_ns = cg.esphome_ns.namespace('uartlog')
UartLogComponent = uartlog_ns.class_('UartLogComponent', cg.Component)
UartLogAction = uartlog_ns.class_('UartLogAction', automation.Action)

CONFIG_SCHEMA = cv.All(
    cv.Schema({
        cv.GenerateID(): cv.declare_id(UartLogComponent),
        cv.Optional(CONF_ENABLE_UART_LOG, default=True): cv.boolean,
        cv.Optional(CONF_BAUD_RATE, default=115200): cv.positive_int,
        # Replace cv.pin with an integer range validator
        cv.Optional(CONF_TX_PIN, default=1): cv.int_range(min=0, max=40),
        cv.Optional(CONF_STRIP_COLORS, default=True): cv.boolean,
        cv.Optional(CONF_MIN_LEVEL, default="DEBUG"): is_log_level,
    }),
    cv.only_with_arduino,
)

UARTLOG_LOG_ACTION_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.use_id(UartLogComponent),
    cv.Required("level"): cv.templatable(cv.int_range(min=0, max=7)),
    cv.Required("tag"): cv.templatable(cv.string),
    cv.Required("payload"): cv.templatable(cv.string),
})

def to_code(config):
    var = cg.new_Pvariable(config[cv.GenerateID()])
    yield cg.register_component(var, config)
    cg.add(var.set_enable_uart_log(config[CONF_ENABLE_UART_LOG]))
    cg.add(var.set_baud_rate(config[CONF_BAUD_RATE]))
    cg.add(var.set_tx_pin(config[CONF_TX_PIN]))
    cg.add(var.set_strip_colors(config[CONF_STRIP_COLORS]))
    cg.add(var.set_min_log_level(LOG_LEVELS[config[CONF_MIN_LEVEL]]))

@automation.register_action('uartlog.log', UartLogAction, UARTLOG_LOG_ACTION_SCHEMA)
def uartlog_log_action_to_code(config, action_id, template_arg, args):
    parent = yield cg.get_variable(config[cv.GenerateID()])
    var = cg.new_Pvariable(action_id, template_arg, parent)
    template_ = yield cg.templatable(config["level"], args, cg.uint8)
    cg.add(var.set_level(template_))
    template_ = yield cg.templatable(config["tag"], args, cg.std_string)
    cg.add(var.set_tag(template_))
    template_ = yield cg.templatable(config["payload"], args, cg.std_string)
    cg.add(var.set_payload(template_))
    yield var
