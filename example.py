#!/usr/bin/env python3

from thermalmodel.nodes import HeatStorageNode
import thermalmodel.links as links

# create  HSN
Battery = HeatStorageNode({ 'mass': 10, 'heatCapacity': 20 })
BoardComputer = HeatStorageNode({ 'mass': 5, 'heatCapacity': 8 })

# attach IFN to HSN
battery_global_interface_properties = {  'emissivity': 0.2, 'absorptivity': 0.6  }
Battery.addInterfaceNode('top-face', { 'area': 12.4, **battery_global_interface_properties })
Battery.addInterfaceNode('bottom-face', { 'area': 12.4, **battery_global_interface_properties })
Battery.addInterfaceNode('front-face', { 'area': 3.8, **battery_global_interface_properties })

BoardComputer.addInterfaceNode('bottom-face', { 'emissivity': 0.7, 'absorptivity': 0.2, 'area': 8.2 })

# add links between IFNs
BoardComputer.addInterfaceLink('bottom-face', 'BAT-top', Battery.interfaces['top-face'], {
    'linkType': links.Manual({ 'viewingFactor': 10 }),
})
BoardComputer.addInterfaceLink('bottom-face', 'BAT-bottom', Battery.interfaces['bottom-face'], {
    'linkType': links.Manual({ 'viewingFactor': 0 }),
})
BoardComputer.addInterfaceLink('bottom-face', 'BAT-front', Battery.interfaces['front-face'], {
    'linkType': links.Manual({ 'viewingFactor': 0 }),
})


# Get temperature of HSN at current time step
# This would perform the computations behind the scenes
BoardComputer.computeInterfaceTemperatures()
BoardComputer.sumInterfaceTemperatures()
BAT_TEMP = BoardComputer.getTemperature()
print(BAT_TEMP)
