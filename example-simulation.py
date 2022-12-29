#!/usr/bin/env python3

import thermalmodel.thermalmodel as tm
import thermalmodel.links as links

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                                Model description
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

model_description = [

    (  # HSN
        'Battery',  # HSN name
        {  # HSN parameters
            'mass': 10,
            'heatCapacity': 20,
            'heatGeneration': 13.2,
            'temperature': 20,
        },
        [  # list of attached IFN
            (
                'top',  # IFN name
                {  # IFN parameters
                    'emissivity': 10,
                    'absorptivity': 0.4,
                },
                [ ]  # links to other IFN
            ),
            (
                'bottom',
                {
                    'emissivity': 10,
                    'absorptivity': 0.4,
                },
                [ ]
            ),
            (
                'front',
                {
                    'emissivity': 10,
                    'absorptivity': 0.4,
                },
                [ ]
            ),
        ]
    ),

    (
        'BoardComputer',
        {
            'mass': 5,
            'heatCapacity': 8,
            # heat generation is assumed 0 if not specified
            'temperature': 21.2,
        },
        [
            (
                'bottom',
                {
                    'emissivity': 10,
                    'absorptivity': 0.4,
                },
                [
                    (
                        'BAT-top', ('Battery', 'top'),
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
                    ),
                    (
                        'BAT-bottom', ('Battery', 'bottom'),
                        [
                            links.ContactLink,
                        ],
                        {
                            'contactArea': 5.2,
                            'resistance': 4.2,
                        }
                    ),
                    (
                        'BAT-front', ('Battery', 'front'),
                        [
                            links.ConductionLink,
                        ],
                        {
                            'conductionArea': 8.51,
                            'conductivity': 3.8,
                            'length': 0.4,
                        }
                    ),
                ]
            ),
        ]
    ),

]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                      Create ThermalModel simulation class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

thermalmodel = tm.ThermalModel(
    simulation_duration=0.1666 * 60,  # seconds
    timestep=1,  # seconds
    model_description=model_description,
)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                                 Run Simulation
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

thermalmodel.simulate()
