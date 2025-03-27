import esphome.config_validation as cv
import esphome.codegen as cg
from esphome.components import switch
from esphome.components.logger import LOG_LEVELS, is_log_level
from esphome.const import CONF_ID

# Configuration keys for our UART log component.
CONF_ENABLE_UART_LOG = "enable_uart_log"
CONF_BAUD_RATE = "baud_rate"
CONF_TX_PIN = "tx_pin"
CONF_STRIP_COLORS = "strip_colors"
CONF_MIN_LEVEL = "min_level"

# Create a namespace for our component.
uartlog_ns = cg.esphome_ns.namespace("uartlog")

# Define the main UART log component.
# Note: We inherit from both cg.Component and switch.Switch so that our component acts as a switch.
UartLogComponent = uartlog_ns.class_("UartLogComponent", cg.Component, switch.Switch)
UartLogAction = uartlog_ns.class_("UartLogAction", cg.Component)

# The configuration schema for the UART log component.
CONFIG_SCHEMA = cv.All(
    cv.Schema({
        cv.GenerateID(): cv.declare_id(UartLogComponent),
        cv.Optional(CONF_ENABLE_UART_LOG, default=True): cv.boolean,
        cv.Optional(CONF_BAUD_RATE, default=115200): cv.positive_int,
        cv.Optional(CONF_TX_PIN, default=1): cv.int_range(min=0, max=40),
        cv.Optional(CONF_STRIP_COLORS, default=True): cv.boolean,
        cv.Optional(CONF_MIN_LEVEL, default="DEBUG"): is_log_level,
    }),
    cv.only_with_arduino,
    cv.COMPONENT_SCHEMA
)

# Define the switch schema for our custom switch.
UARTLOG_SWITCH_SCHEMA = switch.switch_schema(UartLogComponent).extend({
    cv.Required(CONF_ID): cv.use_id(UartLogComponent),
})

# Define an async function to register the switch.
async def uartlog_switch_to_code(config, key, template_args):
    # Get the parent UART log component.
    parent = await cg.get_variable(config[CONF_ID])
    # Create a new PVariable for the switch.
    var = cg.new_Pvariable(config[CONF_ID] + "_switch", parent)
    cg.add(var.set_parent(parent))
    return var

# Main to_code function.
async def to_code(config):
    # Instantiate and register the main component.
    var = cg.new_Pvariable(config[CONF_ID], UartLogComponent)
    await cg.register_component(var, config)
    cg.add(var.set_enable_uart_log(config[CONF_ENABLE_UART_LOG]))
    cg.add(var.set_baud_rate(config[CONF_BAUD_RATE]))
    cg.add(var.set_tx_pin(config[CONF_TX_PIN]))
    cg.add(var.set_strip_colors(config[CONF_STRIP_COLORS]))
    cg.add(var.set_min_log_level(LOG_LEVELS[config[CONF_MIN_LEVEL]]))
    # Register our custom switch with platform "uartlog".
    await switch.register_switch("uartlog", UARTLOG_SWITCH_SCHEMA, uartlog_switch_to_code)
