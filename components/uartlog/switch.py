import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from . import uartlog_ns, UartLogComponent

UartLogSwitch = uartlog_ns.class_("UartLogSwitch", switch.Switch, cg.Component)

UARTLOG_SWITCH_SCHEMA = switch.switch_schema(UartLogSwitch).extend({
    cv.Required("parent"): cv.use_id(UartLogComponent),  # Attach to UartLogComponent
})


async def to_code(config):
    parent = await cg.get_variable(config["parent"])
    var = await switch.new_switch(config)

    # Attach switch to parent
    cg.add(var.set_parent(parent))
    
    await cg.register_component(var, config)
