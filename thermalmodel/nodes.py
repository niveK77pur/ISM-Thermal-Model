#!/usr/bin/env python3

from __future__ import annotations
# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
from .links import Link, LinkType



class Node():

    def __init__(self):
        self._temperature: float = 0

    def getTemperature(self) -> float:
        return self._temperature



class HeatStorageNode(Node):

    def __init__(self, parameters: dict):
        super().__init__()

        self.mass: float         = parameters.get('mass', -1)
        self.heatCapacity: float = parameters.get('heatCapacity', -1)

        self.interfaces: { str: InterfaceNode } = {}

    def sumInterfaceTemperatures(self):
        self._temperature = sum(( ifn.getTemperature() for ifn in self.interfaces.values() ))
        return self._temperature

    def addInterfaceNode(self, name, parameters):
        if self.interfaces.get(name, None):
            raise KeyError(f"Key {name} already exists in HeatStorageNode")
        self.interfaces[name] = InterfaceNode(self, parameters)
        return self.interfaces[name]



class InterfaceNode(Node):

    def __init__(self, referenceNode: HeatStorageNode, parameters: dict):
        super().__init__()

        self.referenceNode: HeatStorageNode = referenceNode

        # self._temperature: float   = parameters.get('temperature', -1)
        self._emissivity: float    = parameters.get('emissivity', -1)
        self._absorptivity: float  = parameters.get('absorptivity', -1)
        self._interfaceArea: float = parameters.get('interfaceArea', -1)

        self.interfaceLinks: { str: Link } = {}

    def addLink(self, name: str, node2: InterfaceNode, parameters: dict):
        if self.interfaceLinks.get(name, None):
            raise KeyError(f"Key {name} already exists in HeatStorageNode")
        self.interfaceLinks[name] = Link(self, node2, parameters)
        return self.interfaceLinks[name]
