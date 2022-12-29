#!/usr/bin/env python3

from typing import Dict, List, Tuple, Type
import numpy as np

from .nodes import HeatStorageNode, LinkType


class ThermalModel():

    def __init__(self, simulation_duration: float, timestep: float,
                 model_description: List[
                     Tuple[str, Dict, List[
                         Tuple[str, Dict, List[
                             Tuple[str, Tuple[str, str], List[Type[LinkType]], Dict]
                         ]]
                     ]]
                 ]):
        """
        The main ThermalModel incorporating all sub-components.

        Parameters:

            - simulation_duration: int

                The number of seconds the simulation should run for. This does not correspond to real-life seconds.

            - timestep: float

                The number of seconds between each time step. Since the simulation is discrete, we are modelling it using "time steps".

            - model_description

                This one allows for a very high level, transparent and descriptive definition of the model. The creation of all the nodes, links, and matrices is taken care of through the data passed in here. It is important to understand the structure of the data requested here.

                The data should look as follows (consider this an example demystifying the type hint):

                    [
                        ('Battery', {<HSN parameters>}, [
                            ('top', {<IFN parameters>}, [
                                ('BoardComputerBottom', ('BoardComputer', 'bottom'), [<Link types>], {<link parameters>}),
                                ('ADCTop', ('ADC', 'top'), [<Link types>], {<link parameters>}),
                                ...
                            ])
                            ('bottom', {<IFN parameters>}, [
                                ('Link1-name', (<HSN-name>, <IFN-name>), [<Link types>], {<link parameters>}),
                                ('Link2-name', (<HSN-name>, <IFN-name>), [<Link types>], {<link parameters>}),
                                ...
                            ])
                            ('front', {<IFN parameters>}, [
                                ('Link1-name', (<HSN-name>, <IFN-name>), [<Link types>], {<link parameters>}),
                                ('Link2-name', (<HSN-name>, <IFN-name>), [<Link types>], {<link parameters>}),
                                ...
                            ])
                            ...
                        ])
                        ('BoardComputer', {<HSN parameters>}, [
                            ('top', {<IFN parameters>}, [
                                ('Link1-name', (<HSN-name>, <IFN-name>), [<Link types>], {<link parameters>}),
                                ('Link2-name', (<HSN-name>, <IFN-name>), [<Link types>], {<link parameters>}),
                                ...
                            ])
                            ('bottom', {<IFN parameters>}, [
                                ('Link1-name', (<HSN-name>, <IFN-name>), [<Link types>], {<link parameters>}),
                                ...
                            ])
                            ...
                        ])
                        ('ADC', {<HSN parameters>}, [
                            ('top', {<IFN parameters>}, [
                                ...
                            ])
                            ...
                        ])
                    ]

        Methods:

            - simulate()

        """

        self.duration: float = simulation_duration  # seconds
        self.timestep: float = timestep  # seconds

        self.heatStorageNodes: Dict[str, HeatStorageNode] = {}

        # create all HSN nodes
        self._addHeatStorageNodes([ (nameHSN, paramsHSN) for nameHSN, paramsHSN, _ in model_description ])
        # create all IFN nodes
        for nameHSN, _, nodesIFN in model_description:
            self._addInterfaceNodes(nameHSN, [ (nameIFN, paramsIFN) for nameIFN, paramsIFN, _ in nodesIFN ])
        # create all IFN links
        for nameHSN, _, nodesIFN in model_description:
            for nameIFN, _, linksIFN in nodesIFN:
                self._addInterfaceLinks(nameHSN, nameIFN, linksIFN)

        # TODO: populate arrays using known data
        self.IFNHeatExchanges: np.ndarray = None
        self.HSNHeatExchanges: np.ndarray = None
        self.LinkHeatExchanges: np.ndarray = None
        self.HSNTemperatureDifferences: np.ndarray = None
        self.HSNTemperatures: np.ndarray = None

    def _createLabelIndex(self) -> dict:
        return {}

    def _createMatrices(self):
        pass

    def _addHeatStorageNodes(self, nodes: List[Tuple[str, Dict]]):
        # TODO: generate numeric ID for indexing in matrix
        for nodeHSN in nodes:
            nameHSN, parameters = nodeHSN
            if self.heatStorageNodes.get(nameHSN, None):
                raise KeyError(f"HSN named '{nameHSN}' already exists in ThermalModel")
            parameters['timestep'] = self.timestep
            self.heatStorageNodes[nameHSN] = HeatStorageNode(parameters=parameters)

    def _addInterfaceNodes(self, nameHSN: str, nodes: List[Tuple[str, Dict]]):
        # TODO: generate numeric ID for indexing in matrix
        for nodeIFN in nodes:
            nameIFN, parameters = nodeIFN
            self.heatStorageNodes[nameHSN].addInterfaceNode(nameIFN, parameters=parameters)

    def _addInterfaceLinks(self, nameHSN: str, nameIFN: str,
                           links: List[Tuple[str, Tuple[str, str], List[Type[LinkType]], Dict]]):
        # TODO: Track missing links in opposite direction (maintain a list)
        # TODO: If link in opposite direction is given, remove it from the list of missing links
        # TODO: following steps in new method? i.e. 'generateMissingLinks()'
        # TODO: Appropriately generate missing links (in opposite direction)
        # TODO: How to make opposite link return negative heat exchange of specified link
        for link in links:
            nameLink, (nameTargetHSN, nameTargetIFN), linkTypes, parameters = link
            self.heatStorageNodes[nameHSN].addInterfaceLink(
                nameLink,
                nameIFN,
                self.heatStorageNodes[nameTargetHSN].interfaces[nameTargetIFN],
                linkTypes,
                parameters
            )

    def simulate(self):
        # TODO: manage data using the matrices
        t = 0
        while t < self.duration:
            t += self.timestep
            print(f"=== Time: {t} ===")
            for heatStorageNode in self.heatStorageNodes.items():
                name, HSN = heatStorageNode
                temperature = HSN.computeTemperature()
                # TODO: create new matrix with new values?
                # TODO: add new matrix to existing matrix?
                # TODO: add temperatures to an array for later use/processing
                print(f'{name} temperature: {temperature}')
