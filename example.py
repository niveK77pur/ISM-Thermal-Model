#!/usr/bin/env python3

from thermalmodel.nodes import HeatStorageNode
import thermalmodel.links as links

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                                   Create HSN
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Battery = HeatStorageNode({
    'mass': 10,
    'heatCapacity': 20,
    'heatGeneration': 13.2,
    'temperature': 20,
})
BoardComputer = HeatStorageNode({
    'mass': 5,
    'heatCapacity': 8,
    # heat generation is assumed 0 if not specified
    'temperature': 21.2,
})

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                                Attach IFN to HSN
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Battery.addInterfaceNode('top-face', {
    'emissivity': 10,
    'absorptivity': 0.4,
})
Battery.addInterfaceNode('bottom-face', {
    'emissivity': 10,
    'absorptivity': 0.4,
})
Battery.addInterfaceNode('front-face', {
    'emissivity': 10,
    'absorptivity': 0.4,
})


BoardComputer.addInterfaceNode('bottom-face', {
    'emissivity': 10,
    'absorptivity': 0.4,
})

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                             Add links between IFNs
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

BoardComputer.addInterfaceLink('BAT-top', 'bottom-face',
                               Battery.interfaces['top-face'],
                               [
                                   links.RadiationLink,
                                   links.ConductionLink,
                                   links.ContactLink,
                               ],
                               {
                                   'radiationArea1': 12.4,  # used by radiation calculations
                                   'radiationArea2': 2.4,   # used by radiation calculations
                                   'viewingFactor': 2.4,    # used by radiation calculations
                                   'contactArea': 20,       # used by contact calculations
                                   'resistance': 4.2,       # used by contact calculations
                                   'conductionArea': 8.51,  # used by conduction calculations
                                   'conductivity': 3.8,     # used by conduction calculations
                                   'length': 0.4,           # used by conduction calculations
                               }
                               )

BoardComputer.addInterfaceLink('BAT-bottom', 'bottom-face',
                               Battery.interfaces['bottom-face'],
                               [
                                   links.ContactLink,
                               ],
                               {
                                   'contactArea': 5.2,
                                   'resistance': 4.2,
                               }
                               )

BoardComputer.addInterfaceLink('BAT-front', 'bottom-face',
                               Battery.interfaces['front-face'],
                               [
                                   links.ConductionLink,
                               ],
                               {
                                   'conductionArea': 8.51,
                                   'conductivity': 3.8,
                                   'length': 0.4,
                               }
                               )

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                                 Get temperature
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Get temperature of HSN at current time step
# This would perform the computations behind the scenes

print(f'[BEFORE]: board_temperature = {BoardComputer.getTemperature()}')
print(f'[BEFORE]: battery_temperature = {Battery.getTemperature()}')

board_temperature = BoardComputer.computeTemperature()
battery_temperature = Battery.computeTemperature()
print(f'[AFTER]: board_temperature = {board_temperature}')
print(f'[AFTER]: battery_temperature = {battery_temperature}')
