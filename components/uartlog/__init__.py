import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from esphome.components.logger import LOG_LEVELS, is_log_level
from esphome.const import CONF_ID

# Configuration keys
CONF_ENABLE_UART_LOG = "enable_uart_log"
CONF_BAUD_RATE = "baud_rate"
CONF_TX_PIN = "tx_pin"
CONF_STRIP_COLORS = "strip_colors"
CONF_MIN_LEVEL = "min_level"
CONF_ALWAYS_FULL_LOGS = "always_full_logs"

# Namespace for the component
uartlog_ns = cg.esphome_ns.namespace("uartlog")

# Define the main UART log component
UartLogComponent = uartlog_ns.class_("UartLogComponent", cg.Component)
# Define the switch class
UartLogSwitch = uartlog_ns.class_("UartLogSwitch", switch.Switch, cg.Component)

# **Main UART Log Component Schema**
CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(UartLogComponent),
    cv.Optional(CONF_ENABLE_UART_LOG, default=True): cv.boolean,
    cv.Optional(CONF_BAUD_RATE, default=115200): cv.positive_int,
    cv.Optional(CONF_TX_PIN, default=1): cv.int_range(min=0, max=40),
    cv.Optional(CONF_STRIP_COLORS, default=True): cv.boolean,
    cv.Optional(CONF_MIN_LEVEL, default="DEBUG"): is_log_level,
    cv.Optional(CONF_ALWAYS_FULL_LOGS, default=False): cv.boolean,
}).extend(cv.COMPONENT_SCHEMA)

# **UART Log Switch Schema**
UARTLOG_SWITCH_SCHEMA = switch.switch_schema(UartLogSwitch).extend({
    cv.Required(CONF_ID): cv.use_id(UartLogComponent),
})

# **Async Function to Handle Component**
async def to_code(config):
    # Register the main component
    var = await cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    
    # Set configuration parameters
    cg.add(var.set_enable_uart_log(config[CONF_ENABLE_UART_LOG]))
    cg.add(var.set_baud_rate(config[CONF_BAUD_RATE]))
    cg.add(var.set_tx_pin(config[CONF_TX_PIN]))
    cg.add(var.set_strip_colors(config[CONF_STRIP_COLORS]))
    cg.add(var.set_min_log_level(LOG_LEVELS[config[CONF_MIN_LEVEL]]))
    cg.add(var.set_always_full_logs(config[CONF_ALWAYS_FULL_LOGS]))

# **Async Function for Switch Handling**
async def uartlog_switch_to_code(config):
    # Get the parent component (UartLogComponent)
    parent = await cg.get_variable(config[CONF_ID])
    
    # Create a new switch object and attach it to the parent
    var = await switch.new_switch(config)
    cg.add(var.set_parent(parent))

    # Register switch as a component
    await cg.register_component(var, config)
