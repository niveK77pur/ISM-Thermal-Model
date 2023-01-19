#!/usr/bin/env python3

import thermalmodel.thermalmodel as tm
import thermalmodel.links as links

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                                    Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def C2K(temperature):
    return temperature + 273.15


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                                Model description
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

model_description = [

    (  # HSN
        'Antenna-Plate',  # HSN name
        {
            'mass': 0.02,
            'heatCapacity': 887,
            'heatGeneration': 0,
            'temperature': C2K(22),
        },
        [  # list of attached IFN
            (
                'Antenna-Plate-bottom',  # IFN name
                {  # IFN parameters
                    'emissivity': 0.045,
                    'absorptivity': 0,
                },
                [
                    (
                        'SSI-top-Antenna-Plate-bottom', ('Antenna-Plate', 'Antenna-Plate-bottom'),
                        [
                            links.ContactLink,
                        ],
                        {
                            'contactArea': 0.003,
                            'resistance': 0.05,
                        }
                    ),
                ]
            ),
        ]
    ),

    (
        'SSI',
        {
            'mass': 0.03,
            'heatCapacity': 887,
            'heatGeneration': 0,
            'temperature': C2K(22),
        },
        [
            (
                'SSI-top',
                {
                    'emissivity': 0.045,
                    'absorptivity': 0,
                },
                [ ],
            ),
            (
                'SSI-side',  # IFN name
                {  # IFN parameters
                    'emissivity': 0.045,
                    'absorptivity': 0,
                },
                [
                    (
                        'SSI-MS-Z--inner', ('MS-Z-', 'MS-Z--inner'),
                        [
                            links.ContactLink,
                        ],
                        {
                            'contactArea': 0.00044,       # used by contact calculations
                            'resistance': 0.05,           # used by contact calculations
                        }
                    )
                ]
            ),
            (
                'SSI-bottom',
                {
                    'emissivity': 0.045,
                    'absorptivity': 0,
                },
                [
                    (
                        'SSI-MAG-Ycoil-top', ('MAG-Ycoil', 'MAG-Ycoil-top'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.002,
                            'radiationArea2': 0.002,
                            'viewingFactor': 0.8,
                        }
                    ),
                ]
            ),
        ]
    ),

]

model_description.append(
    (
        'MS-Z+',
        {
            'mass': 0.07,
            'heatCapacity': 887,
            'heatGeneration': 0,
            'temperature': C2K(22),
        },
        [
            (
                'MS-Z+-inner',
                {
                    'emissivity': 0.045,
                    'absorptivity': 0,
                },
                [
                    (
                        '3C2-MS-Z+-inner', ('MS-Z+', 'MS-Z+-inner'),
                        [
                            links.ConductionLink,
                        ],
                        {
                            'conductionArea': 0.0000135,
                            'conductivity': 398,
                            'length': 0.108,
                        }
                    ),
                    (
                        'MS-Z-inner-MS-Z+-inner', ('MS-Z+', 'MS-Z+-inner'),
                        [
                            links.ConductionLink,
                        ],
                        {
                            'conductionArea': 0.00036,
                            'conductivity': 237,
                            'length': 0.096,
                        }
                    ),
                    (
                        '3C2-top-MS-Z+-inner', ('MS-Z+', 'MS-Z+-inner'),
                        [
                            links.ConductionLink,
                        ],
                        {
                            'conductionArea': 0.000135,
                            'conductivity': 398,
                            'length': 0.108,
                        }
                    ),
                ]
            ),
            (
                'MS-Z+-outer',
                {
                    'emissivity': 0.045,
                    'absorptivity': 0,
                },
                [
                    (
                        'MS-Z+-SSI-side', ('SSI', 'SSI-side'),
                        [
                            links.ContactLink,
                        ],
                        {
                            'contactArea': 0.000108,       # used by contact calculations
                            'resistance': 0.05,            # used by contact calculations
                        }
                    ),
                ]
            ),
        ]
    )
)

model_description.append(

    (  # HSN
        'MAG-Ycoil',  # HSN name
        {  # HSN parameters
            'mass': 0.14,
            'heatCapacity': 387,
            'heatGeneration': 0,
            'temperature': C2K(22),
        },
        [  # list of attached IFN
            (
                'MAG-Ycoil-top',  # IFN name
                {  # IFN parameters
                    'emissivity': 0.03,
                    'absorptivity': 0,
                },
                [ ]  # links to other IFN
            ),
            (
                'MAG-Ycoil-outercirc',
                {
                    'emissivity': 0.03,
                    'absorptivity': 0,
                },
                [
                    (
                        'MAG-Ycoil-outercirc-MS-Z+-inner', ('MS-Z+', 'MS-Z+-inner'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.000892,  # used by radiation calculations
                            'radiationArea2': 2.4,   # used by radiation calculations
                            'viewingFactor': 2.4,    # used by radiation calculations
                        }
                    ),
                    (
                        'MAG-Ycoil-outercirc-MS-Z--inner', ('MS-Z-', 'MS-Z--inner'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.0042,
                            'radiationArea2': 0.0035,
                            'viewingFactor': 0.45,
                        }
                    ),
                ]
            ),
            (
                'MAG-Ycoil-innercirc',
                {
                    'emissivity': 0.03,
                    'absorptivity': 0,
                },
                [
                    (
                        'MAG-Ycoil-innercirc-BAT-curved', ('Batteries', 'BAT-curved'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.0042,
                            'radiationArea2': 0.0035,
                            'viewingFactor': 0.45,
                        }
                    ),
                ]
            ),
            (
                'MAG-Ycoil-bottom',
                {
                    'emissivity': 0.03,
                    'absorptivity': 0,
                },
                [
                    (
                        'MAG-Ycoil-bottom-EPS-top', ('EPS', 'EPS-top'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.008,
                            'radiationArea2': 0.002,
                            'viewingFactor': 0.64,
                        }
                    ),
                ]
            ),
        ]
    ),
)

model_description.append(
    (  # HSN
        'Batteries',  # HSN name
        {  # HSN parameters
            'mass': 0.096,
            'heatCapacity': 1040,
            'heatGeneration': 0,
            'temperature': C2K(22),
        },
        [  # list of attached IFN
            (
                'BAT-curved',  # IFN name
                {  # IFN parameters
                    'emissivity': 0.87,
                    'absorptivity': 0,
                },
                [ ]  # links to other IFN
            ),
            (
                'BAT-flat-face',
                {
                    'emissivity': 0.87,
                    'absorptivity': 0,
                },
                [ ]
            ),
        ]
    )
)

model_description.append(
    (
        'EPS',
        {
            'mass': 0.013,
            'heatCapacity': 387,
            'heatGeneration': 0.2,
            'temperature': C2K(22),
        },
        [
            (
                'EPS-top',
                {
                    'emissivity': 0.03,
                    'absorptivity': 0,
                },
                [ ]
            ),
            (
                'EPS-bottom',
                {
                    'emissivity': 0.03,
                    'absorptivity': 0,
                },
                [
                    (
                        'Batteries-EPS-top', ('Batteries', 'BAT-curved'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.008,    # used by radiation calculations
                            'radiationArea2': 0.004,    # used by radiation calculations
                            'viewingFactor': 0.4,       # used by radiation calculation
                        }
                    ),
                    (
                        'EPS-BAT-flat-face', ('Batteries', 'BAT-flat-face'),
                        [
                            links.ConductionLink,
                        ],
                        {
                            'conductionArea': 0.000064,
                            'conductivity': 398,
                            'length': 0.011,
                        }
                    ),
                ]
            ),
        ]
    )
)

model_description.append(
    (
        '3C2',
        {
            'mass': 0.18,
            'heatCapacity': 387,
            'heatGeneration': 1.33,
            'temperature': C2K(22),
        },
        [
            (
                '3C2-top',
                {
                    'emissivity': 0.03,
                    'absorptivity': 0,
                },
                [
                    (
                        '3C2-top-EPS-bottom', ('EPS', 'EPS-bottom'),
                        [
                            links.ConductionLink,
                        ],
                        {
                            'conductionArea': 0.0001,
                            'conductivity': 237,
                            'length': 0.011,
                        }
                    ),
                    (
                        'Panel-X--inner-3C2-top', ('3C2', '3C2-top'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.008,
                            'radiationArea2': 0.026,
                            'viewingFactor': 0.17,
                        }
                    ),
                    (
                        'Panel-X+-inner-3C2-top', ('3C2', '3C2-top'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.008,
                            'radiationArea2': 0.026,
                            'viewingFactor': 0.17,
                        }
                    ),
                ]
            ),
            (
                '3C2-bottom',
                {
                    'emissivity': 0.03,
                    'absorptivity': 0,
                },
                [
                    (
                        '3C2-bottom-EPS-bottom2', ('EPS', 'EPS-bottom'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.008,
                            'radiationArea2': 0.008,
                            'viewingFactor': 0.799,
                        }
                    ),
                ]
            ),
        ]
    )
)

model_description.append(
    (
        'SSII',
        {
            'mass': 0.03,
            'heatCapacity': 887,
            'heatGeneration': 0,
            'temperature': C2K(22),
        },
        [
            (
                'SSII-top',
                {
                    'emissivity': 0.045,
                    'absorptivity': 0,
                },
                [
                    (
                        '3C2-bottom-SSII-top', ('SSII', 'SSII-top'),
                        [
                            links.ConductionLink,
                        ],
                        {
                            'conductionArea': 0.000103,
                            'conductivity': 237,
                            'length': 0.03,
                        }
                    ),
                    (
                        'EPS-bottom-SSII-top', ('SSII', 'SSII-top'),
                        [
                            links.ConductionLink,
                        ],
                        {
                            'conductionArea': 0.000103,
                            'conductivity': 237,
                            'length': 0.03,
                        }
                    ),
                ]
            ),
            (
                'SSII-side',
                {
                    'emissivity': 0.045,
                    'absorptivity': 0,
                },
                [
                    (
                        'SSII-MS-Z+-inner', ('MS-Z+', 'MS-Z+-inner'),
                        [
                            links.ContactLink,
                        ],
                        {
                            'contactArea': 0.00044,
                            'resistance': 0.05,
                        }
                    ),
                ]
            ),
        ]
    )
)

model_description.append(
    (
        'MS-Z-',
        {
            'mass': 0.07,
            'heatCapacity': 887,
            'heatGeneration': 0,
            'temperature': C2K(22),
        },
        [
            (
                'MS-Z--inner',
                {
                    'emissivity': 0.045,
                    'absorptivity': 0,
                },
                [
                    (
                        '3C2-top-MS-Z--inner', ('MS-Z-', 'MS-Z--inner'),
                        [
                            links.ConductionLink,
                        ],
                        {
                            'conductionArea': 0.000013,
                            'conductivity': 398,
                            'length': 0.108,
                        }
                    ),
                    (
                        'SSII-MS-Z--inner', ('MS-Z-', 'MS-Z--inner'),
                        [
                            links.ContactLink,
                        ],
                        {
                            'contactArea': 0.00044,  # used by contact calculations
                            'resistance': 0.05,  # used by contact calculations
                        }
                    ),
                ]
            ),
            (
                'MS-Z--outer',
                {
                    'emissivity': 0.045,
                    'absorptivity': 0,
                },
                [
                    (
                        'Panel-X--inner-MS-Z--outer', ('MS-Z-', 'MS-Z--outer'),
                        [
                            links.ContactLink,
                        ],
                        {
                            'contactArea': 0.0004,
                            'resistance': 0.05,
                        }
                    ),
                ]
            ),
        ]
    ),
)

model_description.append(
    (
        'SSIII',
        {
            'mass': 0.03,
            'heatCapacity': 887,
            'heatGeneration': 0,
            'temperature': C2K(22),
        },
        [
            (
                'SSIII-side',
                {
                    'emissivity': 0.045,
                    'absorptivity': 0,
                },
                [
                    (
                        'SSIII-side-MS-Z+-inner', ('MS-Z+', 'MS-Z+-inner'),
                        [
                            links.ContactLink,
                        ],
                        {
                            'contactArea': 0.00044,
                            'resistance': 0.05,
                        }
                    ),
                ]
            ),
            (
                'SSIII-bottom',
                {
                    'emissivity': 0.045,
                    'absorptivity': 0,
                },
                [
                    (
                        'SSIII-MS-Z+-inner', ('MS-Z+', 'MS-Z+-inner'),
                        [
                            links.ContactLink,
                        ],
                        {
                            'contactArea': 0.00044,
                            'resistance': 0.05,
                        }
                    ),
                    (
                        'SSIII-MS-Z--inner', ('MS-Z-', 'MS-Z--inner'),
                        [
                            links.ContactLink,
                        ],
                        {
                            'contactArea': 0.00044,       # used by contact calculations
                            'resistance': 0.05,           # used by contact calculations
                        }
                    ),
                ]
            ),
        ]
    )
)


model_description.append(
    (
        'Panel-Z-',
        {
            'mass': 0.08,
            'heatCapacity': 887,
            'heatGeneration': 0,
            'temperature': C2K(22),
        },
        [
            (
                'Panel-Z--inner',
                {
                    'emissivity': 0.03,
                    'absorptivity': 0,
                },
                [
                    (
                        'Panel-Z--inner-BAT-curved', ('Batteries', 'BAT-curved'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.008,    # used by radiation calculations
                            'radiationArea2': 0.004,    # used by radiation calculations
                            'viewingFactor': 0.15,
                        }
                    ),
                    (
                        'Panel-Z--EPS-top', ('EPS', 'EPS-top'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.008,       # used by contact calculations
                            'radiationArea2': 0.004,          # used by contact calculations
                            'viewingFactor': 0.15,
                        }
                    ),
                    (
                        'Panel-Z--3C2-top', ('3C2', '3C2-top'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.008,
                            'radiationArea2': 0.004,
                            'viewingFactor': 0.06,
                        }
                    ),
                    (
                        'MS-Z--outer-Panel-Z--inner', ('Panel-Z-', 'Panel-Z--inner'),
                        [
                            links.ContactLink,
                        ],
                        {
                            'contactArea': 0.004,
                            'resistance': 0.05,
                        }
                    ),
                ]
            ),
        ]
    )
)

model_description.append(
    (
        'Panel-X+',
        {
            'mass': 0.08,
            'heatCapacity': 887,
            'heatGeneration': 0,
            'temperature': C2K(22),
        },
        [
            (
                'Panel-X+-inner',
                {
                    'emissivity': 0.03,
                    'absorptivity': 0,
                },
                [
                    (
                        'Panel-X+-inner-BAT-curved', ('Batteries', 'BAT-curved'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.008,
                            'radiationArea2': 0.004,
                            'viewingFactor': 0.15,
                        }
                    ),
                    (
                        'Panel-X+-inner-EPS-top', ('EPS', 'EPS-top'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.008,
                            'radiationArea2': 0.004,
                            'viewingFactor': 0.15,
                        }
                    ),
                    (
                        'Panel-X+-inner-MS-Z--outer', ('MS-Z-', 'MS-Z--outer'),
                        [
                            links.ContactLink,
                        ],
                        {
                            'contactArea': 0.0004,
                            'resistance': 0.05,
                        }
                    ),
                    (
                        'MS-Z+-outer-Panel-X+-inner', ('Panel-X+', 'Panel-X+-inner'),
                        [
                            links.ContactLink,
                        ],
                        {
                            'contactArea': 0.0004,
                            'resistance': 0.05,
                        }
                    ),
                    (
                        'Panel-X+-inner-MAG-Zcoil-outer', ('MAG-Zcoil', 'MAG-Zcoil-outer'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.005,
                            'radiationArea2': 0.026,
                            'viewingFactor': 0.36,
                        }
                    ),
                ]
            ),
        ]
    ),
)

model_description.append(
    (
        'Panel-X-',
        {
            'mass': 0.08,
            'heatCapacity': 887,
            'heatGeneration': 0,
            'temperature': C2K(22),
        },
        [
            (
                'Panel-X--inner',
                {
                    'emissivity': 0.045,
                    'absorptivity': 0,
                },
                [
                    (
                        'Panel-X--inner-BAT-curved', ('Batteries', 'BAT-curved'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.008,
                            'radiationArea2': 0.004,
                            'viewingFactor': 0.15,
                        }
                    ),
                    (
                        'Panel-X--inner-MAG-Zcoil-outer', ('MAG-Zcoil', 'MAG-Zcoil-outer'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.005,
                            'radiationArea2': 0.026,
                            'viewingFactor': 0.36,
                        }
                    ),
                    (
                        'MS-Z+-outer-Panel-X--inner', ('Panel-X-', 'Panel-X--inner'),
                        [
                            links.ContactLink,
                        ],
                        {
                            'contactArea': 0.004,
                            'resistance': 0.05,
                        }
                    ),
                ]
            ),
        ]
    ),
)

model_description.append(
    (
        'Panel-Z+',
        {
            'mass': 0.08,
            'heatCapacity': 887,
            'heatGeneration': 0,
            'temperature': C2K(22),
        },
        [
            (
                'Panel-Z+-inner',
                {
                    'emissivity': 0.045,
                    'absorptivity': 0,
                },
                [
                    (
                        'Panel-Z+-BAT-curved', ('Batteries', 'BAT-curved'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.008,
                            'radiationArea2': 0.004,
                            'viewingFactor': 0.15,
                        }
                    ),
                    (
                        'Panel-Z+-EPS-top', ('EPS', 'EPS-top'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.008,
                            'radiationArea2': 0.004,
                            'viewingFactor': 0.15,
                        }
                    ),
                    (
                        'Panel-Z+-MS-Z+-outer', ('MS-Z-', 'MS-Z--outer'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.008,
                            'radiationArea2': 0.008,
                            'viewingFactor': 0.95,
                        }
                    ),
                    (
                        'Panel-Z+inner-3C2-top', ('3C2', '3C2-top'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.008,
                            'radiationArea2': 0.0053,
                            'viewingFactor': 0.17,
                        }
                    ),
                ]
            ),
        ]
    ),
)

model_description.append(
    (
        'SSIV',
        {
            'mass': 0.03,
            'heatCapacity': 887,
            'heatGeneration': 0,
            'temperature': C2K(22),
        },
        [
            (
                'SSIV-side',
                {
                    'emissivity': 0.045,
                    'absorptivity': 0,
                },
                [
                    (
                        'MS-Z-inner-SSIV-side', ('SSIV', 'SSIV-side'),
                        [
                            links.ContactLink,
                        ],
                        {
                            'contactArea': 0.00044,
                            'resistance': 0.05,
                        }
                    ),
                    (
                        'MS-Z+-inner-SSIV-side', ('SSIV', 'SSIV-side'),
                        [
                            links.ContactLink,
                        ],
                        {
                            'contactArea': 0.00044,
                            'resistance': 0.05,
                        }
                    ),
                ]
            ),
            (
                'SSIV-top',
                {
                    'emissivity': 0.045,
                    'absorptivity': 0,
                },
                [
                    (
                        'SSIV-top-MS-Z+-inner', ('MS-Z+', 'MS-Z+-inner'),
                        [
                            links.ContactLink,
                        ],
                        {
                            'contactArea': 0.00044,
                            'resistance': 0.05,
                        }
                    ),
                    (
                        'SSIV-MS-Z--inner', ('MS-Z-', 'MS-Z--inner'),
                        [
                            links.ContactLink,
                        ],
                        {
                            'contactArea': 0.00044,       # used by contact calculations
                            'resistance': 0.05,           # used by contact calculations
                        }
                    ),
                ]
            ),
        ]
    )
)

model_description.append(
    (
        'SSV',
        {
            'mass': 0.03,
            'heatCapacity': 887,
            'heatGeneration': 0,
            'temperature': C2K(22),
        },
        [
            (
                'SSV-side',
                {
                    'emissivity': 0.045,
                    'absorptivity': 0,
                },
                [
                    (
                        'MS-Z+-inner-SSV-side', ('SSV', 'SSV-side'),
                        [
                            links.ContactLink,
                        ],
                        {
                            'contactArea': 0.00044,
                            'resistance': 0.05,
                        }
                    ),
                    (
                        'MS-Z-inner-SSV-side', ('SSV', 'SSV-side'),
                        [
                            links.ContactLink,
                        ],
                        {
                            'contactArea': 0.00044,
                            'resistance': 0.05,
                        }
                    ),
                ]
            ),
        ]
    )
)

model_description.append(
    (
        'SSVI',
        {
            'mass': 0.03,
            'heatCapacity': 887,
            'heatGeneration': 0,
            'temperature': C2K(22),
        },
        [
            (
                'SSVI-side',
                {
                    'emissivity': 0.045,
                    'absorptivity': 0,
                },
                [
                    (
                        'MS-Z+-SSVI-side', ('SSV', 'SSV-side'),
                        [
                            links.ContactLink,
                        ],
                        {
                            'contactArea': 0.00044,
                            'resistance': 0.05,
                        }
                    ),
                    (
                        'MS-Z--SSVI-side', ('SSV', 'SSV-side'),
                        [
                            links.ContactLink,
                        ],
                        {
                            'contactArea': 0.00044,       # used by contact calculations
                            'resistance': 0.05,           # used by contact calculations
                        }
                    ),
                ]
            ),
        ]
    )
)

model_description.append(
    (
        'RW',
        {
            'mass': 0.03,
            'heatCapacity': 887,
            'heatGeneration': 0,
            'temperature': C2K(22),
        },
        [
            (
                'RW-curved',
                {
                    'emissivity': 0.045,
                    'absorptivity': 0,
                },
                [ ]
            ),
            (
                'RW-bottom',
                {
                    'emissivity': 0.045,
                    'absorptivity': 0,
                },
                [
                    (
                        'Panel-Z+-RW-curved', ('RW', 'RW-curved'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.002,
                            'radiationArea2': 0.026,
                            'viewingFactor': 0.15,
                        }
                    ),
                    (
                        'Panel-X+-inner-RW-curved', ('RW', 'RW-curved'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.002,
                            'radiationArea2': 0.026,
                            'viewingFactor': 0.05,
                        }
                    ),
                    (
                        'Panel-Z-inner-RW-curved', ('RW', 'RW-curved'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.002,
                            'radiationArea2': 0.026,
                            'viewingFactor': 0.05
                        }
                    ),
                    (
                        'Panel-X--inner-RW-curved', ('RW', 'RW-curved'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.002,
                            'radiationArea2': 0.026,
                            'viewingFactor': 0.05,
                        }
                    ),
                ]
            ),
        ]
    )
)


model_description.append(
    (
        'RW-PCB',
        {
            'mass': 0.15,
            'heatCapacity': 389,
            'heatGeneration': 0,
            'temperature': C2K(22),
        },
        [
            (
                'RW-PCB-top',
                {
                    'emissivity': 0.03,
                    'absorptivity': 0,
                },
                [ ]
            ),
            (
                'RW-PCB-bottom',
                {
                    'emissivity': 0.03,
                    'absorptivity': 0,
                },
                [
                    (
                        'RW-bottom-RW-PCB-top', ('RW-PCB', 'RW-PCB-top'),
                        [
                            links.ContactLink,
                        ],
                        {
                            'contactArea': 0.0016,
                            'resistance': 0.05,
                        }
                    ),
                    (
                        'RW-PCB-bottom-SSIV-top', ('SSIV', 'SSIV-top'),
                        [
                            links.ConductionLink,
                        ],
                        {
                            'conductionArea': 0.0001036,
                            'conductivity': 237,
                            'length': 0.023,
                        }
                    ),
                ]
            ),
        ]
    )
)

model_description.append(
    (
        'ZXMAG-PCB',
        {
            'mass': 0.15,
            'heatCapacity': 389,
            'heatGeneration': 0,
            'temperature': C2K(22),
        },
        [
            (
                'ZXMAG-PCB-top',
                {
                    'emissivity': 0.03,
                    'absorptivity': 0,
                },
                [
                    (
                        'SSIII-bottom-ZXMAG-PCB-top', ('ZXMAG-PCB', 'ZXMAG-PCB-top'),
                        [
                            links.ConductionLink,
                        ],
                        {
                            'conductionArea': 0.0001,
                            'conductivity': 237,
                            'length': 0.04,
                        }
                    ),
                    (
                        'ZXMAG-PCB-top-MAG-Zarm-outer', ('MAG-Zarm', 'MAG-Zarm-outer'),
                        [
                            links.ConductionLink,
                        ],
                        {
                            'conductionArea': 0.00014,
                            'conductivity': 237,
                            'length': 0.008,
                        }
                    ),
                ]
            ),
            (
                'ZXMAG-PCB-bottom',
                {
                    'emissivity': 0.03,
                    'absorptivity': 0,
                },
                [
                    (
                        'ZXMAG-PCB-bottom-RW-PCB-top', ('RW-PCB', 'RW-PCB-top'),
                        [
                            links.ConductionLink
                        ],
                        {
                            'conductionArea': 0.000103,
                            'conductivity': 237,
                            'length': 0.02
                        }
                    ),
                ]
            ),
        ]
    ),
)

model_description.append(
    (
        'MAG-Xcoil',
        {
            'mass': 0.01,
            'heatCapacity': 389,
            'heatGeneration': 0,
            'temperature': C2K(22),
        },
        [
            (
                'MAG-Xcoil-outer',
                {
                    'emissivity': 0.03,
                    'absorptivity': 0,
                },
                [
                    (
                        'Panel-X+-inner-MAG-Xcoil-outer', ('MAG-Xcoil', 'MAG-Xcoil-outer'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.005,
                            'radiationArea2': 0.026,
                            'viewingFactor': 0.36,
                        }
                    ),
                    (
                        'Panel-X--inner-MAG-Xcoil-outer', ('MAG-Xcoil', 'MAG-Xcoil-outer'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.005,
                            'radiationArea2': 0.026,
                            'viewingFactor': 0.36,
                        }
                    ),
                    (
                        'Panel-Z+-MAG-Xcoil-outer', ('MAG-Xcoil', 'MAG-Xcoil-outer'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.005,
                            'radiationArea2': 0.026,
                            'viewingFactor': 0.36,
                        }
                    ),
                    (
                        'Panel-Z--inner-MAG-Xcoil-outer', ('MAG-Xcoil', 'MAG-Xcoil-outer'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.005,
                            'radiationArea2': 0.026,
                            'viewingFactor': 0.36,
                        }
                    ),
                ]
            ),
            (
                'MAG-Xcoil-inner',
                {
                    'emissivity': 0.03,
                    'absorptivity': 0,
                },
                [
                    (
                        'ZXMAG-PCB-MAG-Xcoil-outer', ('MAG-Xcoil', 'MAG-Xcoil-outer'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.005,
                            'radiationArea2': 0.006,
                            'viewingFactor': 0.011,
                        }
                    ),
                ]
            ),
        ]
    )
)

model_description.append(
    (
        'MAG-Zcoil',
        {
            'mass': 0.01,
            'heatCapacity': 389,
            'heatGeneration': 0,
            'temperature': C2K(22),
        },
        [
            (
                'MAG-Zcoil-inner',
                {
                    'emissivity': 0.03,
                    'absorptivity': 0,
                },
                [ ]
            ),
            (
                'MAG-Zcoil-outer',
                {
                    'emissivity': 0.03,
                    'absorptivity': 0,
                },
                [ ]
            ),
        ]
    ),
)

model_description.append(
    (
        'MAG-Zarm',
        {
            'mass': 0.01,
            'heatCapacity': 887,
            'heatGeneration': 0,
            'temperature': C2K(22),
        },
        [
            (
                'MAG-Zarm-outer',
                {
                    'emissivity': 0.045,
                    'absorptivity': 0,
                },
                [
                    (
                        'MAG-Zcoil-MAG-Zarm-outer', ('MAG-Zarm', 'MAG-Zarm-outer'),
                        [
                            links.ContactLink,
                        ],
                        {
                            'contactArea': 0.004,
                            'resistance': 0.05,
                        }
                    ),
                    (
                        'Panel-Z--MAG-Zcoil-outer', ('MAG-Zcoil', 'MAG-Zcoil-outer'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.005,
                            'radiationArea2': 0.026,
                            'viewingFactor': 0.36,
                        }
                    ),
                    (
                        'ZXMAG-PCB-MAG-Zcoil-outer', ('MAG-Zcoil', 'MAG-Zcoil-outer'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.005,
                            'radiationArea2': 0.006,
                            'viewingFactor': 0.011,
                        }
                    ),
                    (
                        'Panel-Z+-MAG-Zcoil-outer', ('MAG-Zcoil', 'MAG-Zcoil-outer'),
                        [
                            links.RadiationLink,
                        ],
                        {
                            'radiationArea1': 0.005,
                            'radiationArea2': 0.026,
                            'viewingFactor': 0.36,
                        }
                    ),
                    (
                        'ZXMAG-PCB-MAG-Zarm-outer', ('MAG-Zarm', 'MAG-Zarm-outer'),
                        [
                            links.ConductionLink,
                        ],
                        {
                            'conductionArea': 0.00014,
                            'conductivity': 237,
                            'length': 0.008,
                        }
                    ),
                ]
            ),
        ]
    ),
)

model_description.append(
    (
        'MAG-Xarm',
        {
            'mass': 0.01,
            'heatCapacity': 887,
            'heatGeneration': 0,
            'temperature': C2K(22),
        },
        [
            (
                'MAG-Xarm-outer',
                {
                    'emissivity': 0.045,
                    'absorptivity': 0,
                },
                [
                    (
                        'ZXMAG-PCB-MAG-Xarm-outer', ('MAG-Xarm', 'MAG-Xarm-outer'),
                        [
                            links.ConductionLink,
                        ],
                        {
                            'conductionArea': 0.000142,
                            'conductivity': 237,
                            'length': 0.008,
                        }
                    ),
                    (
                        'MAG-Xcoil-MAG-Xarm-outer', ('MAG-Xarm', 'MAG-Xarm-outer'),
                        [
                            links.ContactLink,
                        ],
                        {
                            'contactArea': 0.004,
                            'resistance': 0.05,
                        }
                    ),
                ]
            ),
        ]
    ),
)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                      Create ThermalModel simulation class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

thermalmodel = tm.ThermalModel(
    simulation_duration=20 * 60,  # seconds
    timestep=1,  # seconds
    model_description=model_description,
)

thermalmodel.display()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                                 Run Simulation
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

thermalmodel.simulate()
thermalmodel.plotfig()
thermalmodel.save()
