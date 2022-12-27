#!/usr/bin/env python3

from __future__ import annotations
from typing import Dict, List, Type
# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
from .links import Link, LinkType


class Node():

    def __init__(self):
        self._temperature: float = 0

    def computeHeatExchange(self):
        return NotImplementedError()

    def getTemperature(self) -> float:
        return self._temperature


class HeatStorageNode(Node):

    def __init__(self, parameters: dict):
        super().__init__()

        self._timestep: float = 0

        self.mass: float         = parameters.get('mass', -1)
        self.heatCapacity: float = parameters.get('heatCapacity', -1)

        self.heatGeneration: float = parameters.get('heatGeneration', 0)
        self._heatExchange: float = -1
        self._temperature: float = parameters.get('temperature', 0)

        self.interfaces: Dict[str, InterfaceNode] = {}

    def _computeHeatExchange(self) -> float:
        self._heatExchange = self.heatGeneration + sum((
            ifn.computeHeatExchange() for ifn in self.interfaces.values()
        ))
        return self._heatExchange

    def _computeTemperatureDifference(self) -> float:
        delta = (self._computeHeatExchange() * self._timestep) / (self.mass * self.heatCapacity)
        return delta

    def computeTemperature(self) -> float:
        self._temperature += self._computeTemperatureDifference()
        return self._temperature

    def addInterfaceNode(self, name: str, parameters: dict) -> InterfaceNode:
        if self.interfaces.get(name, None):
            raise KeyError(f"Key {name} already exists in HeatStorageNode")
        self.interfaces[name] = InterfaceNode(self, parameters)
        return self.interfaces[name]

    def addInterfaceLink(self, linkName: str, interfaceName: str,
                         node2: InterfaceNode,
                         linkTypes: List[Type[LinkType]],
                         parameters: dict) -> Link:
        self.interfaces[interfaceName].addLink(linkName, node2, linkTypes, parameters)
        return self.interfaces[interfaceName].interfaceLinks[linkName]


class InterfaceNode(Node):

    def __init__(self, referenceNode: HeatStorageNode, parameters: dict):
        super().__init__()

        self.referenceNode: HeatStorageNode = referenceNode

        self._temperature: float  = referenceNode._temperature
        self._heatExchange: float = -1

        self._emissivity: float    = parameters.get('emissivity', -1)
        self._absorptivity: float  = parameters.get('absorptivity', -1)

        self.interfaceLinks: Dict[str, Link] = {}

    def computeHeatExchange(self) -> float:
        self._heatExchange = sum((
            link.computeHeatExchange() for link in self.interfaceLinks.values()
        ))
        return self._heatExchange

    def addLink(self, name: str, node2: InterfaceNode,
                linkTypes: List[Type[LinkType]],
                parameters: dict) -> Link:
        if self.interfaceLinks.get(name, None):
            raise KeyError(f"Key {name} already exists in HeatStorageNode")
        self.interfaceLinks[name] = Link(self, node2, linkTypes, parameters)
        return self.interfaceLinks[name]
