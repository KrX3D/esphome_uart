import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from . import uartlog_ns, UartLogComponent

UartLogSwitch = uartlog_ns.class_("UartLogSwitch", switch.Switch, cg.Component)

CONFIG_SCHEMA = switch.switch_schema(UartLogSwitch).extend(cv.COMPONENT_SCHEMA).extend({
    cv.Required("parent"): cv.use_id(UartLogComponent)
})

async def to_code(config):
    parent = await cg.get_variable(config["parent"])
    var = await switch.new_switch(config)
    cg.add(var.set_parent(parent))
    await cg.register_component(var, config)
