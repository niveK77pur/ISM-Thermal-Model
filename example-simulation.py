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
                'BAT-top',  # IFN name
                {  # IFN parameters
                    'emissivity': 10,
                    'absorptivity': 0.4,
                },
                [ ]  # links to other IFN
            ),
            (
                'BAT-bottom',
                {
                    'emissivity': 10,
                    'absorptivity': 0.4,
                },
                [ ]
            ),
            (
                'BAT-front',
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
                'BC-bottom',
                {
                    'emissivity': 10,
                    'absorptivity': 0.4,
                },
                [
                    (
                        'BC-BAT-top', ('Battery', 'BAT-top'),
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
                        'BC-BAT-bottom', ('Battery', 'BAT-bottom'),
                        [
                            links.ContactLink,
                        ],
                        {
                            'contactArea': 5.2,
                            'resistance': 4.2,
                        }
                    ),
                    (
                        'BC-BAT-front', ('Battery', 'BAT-front'),
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
thermalmodel.save()
