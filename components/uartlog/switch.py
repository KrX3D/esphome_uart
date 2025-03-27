import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch

uartlog_ns = cg.esphome_ns.namespace("uartlog")
UartLogSwitch = empty_switcuartlog_nsh_ns.class_("UartLogComponent", switch.Switch, cg.Component)

CONFIG_SCHEMA = switch.switch_schema(UartLogSwitch).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = await switch.new_switch(config)
    await cg.register_component(var, config)