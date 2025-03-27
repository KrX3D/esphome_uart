import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from esphome.const import CONF_ID
from . import uartlog_ns, UartLogComponent

# Define the custom switch class in our namespace.
UartLogSwitch = uartlog_ns.class_("UartLogSwitch", switch.Switch, cg.Component)

# Define the configuration schema for the switch.
CONFIG_SCHEMA = switch.switch_schema(UartLogSwitch).extend({
    cv.Required("parent"): cv.use_id(UartLogComponent),
}).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    parent = await cg.get_variable(config["parent"])
    var = await switch.new_switch(config)
    cg.add(var.set_parent(parent))
    await cg.register_component(var, config)
