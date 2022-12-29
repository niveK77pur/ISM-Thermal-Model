#!/usr/bin/env python3

from typing import Dict, List, Tuple, Type
import numpy as np
import itertools

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
        # number of nodes/links
        self.counters: Dict[str, int] = { 'HSN': 0, 'IFN': 0, 'links': 0 }
        # map nodes/links to numeric IDs for use on matrices
        # also see 'ID2label()' and 'label2ID()' functions
        self.IDmap: Dict[str, List[Tuple[str, int]]] = { 'HSN': [], 'IFN': [], 'links': [] }

        # create all HSN nodes
        self._addHeatStorageNodes([ (nameHSN, paramsHSN) for nameHSN, paramsHSN, _ in model_description ])
        self.counters['HSN'] = len(model_description)
        hsnID = itertools.count()
        self.IDmap['HSN'] += [ (nameHSN, next(hsnID)) for (nameHSN, _, _) in model_description ]
        del hsnID
        # create all IFN nodes
        ifnID = itertools.count()
        for nameHSN, _, nodesIFN in model_description:
            self._addInterfaceNodes(nameHSN, [ (nameIFN, paramsIFN) for nameIFN, paramsIFN, _ in nodesIFN ])
            self.counters['IFN'] += len(nodesIFN)
            self.IDmap['IFN'] += [ (nameIFN, next(ifnID)) for (nameIFN, _, _) in nodesIFN ]
        del ifnID
        # create all IFN links
        linkID = itertools.count()
        for nameHSN, _, nodesIFN in model_description:
            for nameIFN, _, linksIFN in nodesIFN:
                self._addInterfaceLinks(nameHSN, nameIFN, linksIFN)
                self.counters['links'] += len(linksIFN)
                self.IDmap['links'] += [ (nameLink, next(linkID)) for (nameLink, _, _, _) in linksIFN ]
        del linkID

        # TODO: populate arrays using known data
        # TODO: when adding data for each timestep, gradually increase the dimension (the one saying 1 below)
        self.IFNHeatExchanges: np.ndarray = np.zeros((self.counters['IFN'], self.counters['IFN'], 1))
        self.HSNHeatExchanges: np.ndarray = np.zeros((self.counters['HSN'], self.counters['HSN'], 1))
        self.HSNTemperatures: np.ndarray = np.zeros((self.counters['HSN'], 1))

    def ID2label(self, _class: str, ID: int) -> str:
        """Convert ID from element class to corresponding label string
            _class: String value containing one of the dict keys of self.IDmap
        """
        for idmap in self.IDmap[_class]:
            name, givenID = idmap
            if ID == givenID:
                return name
        raise KeyError(f'ID {ID} not found in list of class {_class}')

    def label2ID(self, _class: str, label: str) -> int:
        """Convert label from element class to corresponding ID
            _class: String value containing one of the dict keys of self.IDmap
        """
        for idmap in self.IDmap[_class]:
            givenName, ID = idmap
            if label == givenName:
                return ID
        raise KeyError(f'Name {label} not found in list of class {_class}')

    def _createMatrices(self):
        raise NotImplementedError()

    def _addHeatStorageNodes(self, nodes: List[Tuple[str, Dict]]):
        for nodeHSN in nodes:
            nameHSN, parameters = nodeHSN
            if self.heatStorageNodes.get(nameHSN, None):
                raise KeyError(f"HSN named '{nameHSN}' already exists in ThermalModel")
            parameters['timestep'] = self.timestep
            self.heatStorageNodes[nameHSN] = HeatStorageNode(parameters=parameters)

    def _addInterfaceNodes(self, nameHSN: str, nodes: List[Tuple[str, Dict]]):
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
        print('Counters:', self.counters)
        print('IDs:', self.IDmap)
        print('ID2label() example:', self.ID2label('IFN', 2))
        print('label2ID() example:', self.label2ID('HSN', 'Battery'))

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