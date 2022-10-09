#!/usr/bin/env python3

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from links import Link, LinkType



class Node():

    def __init__(self):
        self._temperature: float = 0

    def getTemperature(self) -> float:
        return self._temperature



class HeatStorageNode(Node):

    def __init__(self, parameters: dict):

        self.mass: float         = parameters.get('mass', -1)
        self.heatCapacity: float = parameters.get('heatCapacity', -1)

        self._interfaces: { str: InterfaceNode } = {}

    def sumInterfaceTemperatures(self):
        self._temperature = sum(( ifn.getTemperature() for ifn in self._interfaces.values() ))
        return self._temperature

    def addInterfaceNode(self, name, parameters):
        if self._interfaces.get(name, None):
            raise KeyError(f"Key {name} already exists in HeatStorageNode")
        self._interfaces[name] = InterfaceNode(self, parameters)
        return self._interfaces[name]



class InterfaceNode(Node):

    def __init__(self, referenceNode: HeatStorageNode, parameters: dict):

        self.referenceNode: HeatStorageNode = referenceNode

        # self._temperature: float   = parameters.get('temperature', -1)
        self._emissivity: float    = parameters.get('emissivity', -1)
        self._absorptivity: float  = parameters.get('absorptivity', -1)
        self._interfaceArea: float = parameters.get('interfaceArea', -1)

        self._interfaceLinks: { str: Link } = {}

    def addLink(self, name: str, node2: InterfaceNode, parameters: dict):
        if self._interfaceLinks.get(name, None):
            raise KeyError(f"Key {name} already exists in HeatStorageNode")
        self._interfaceLinks[name] = Link(self, node2, parameters)
        return self._interfaceLinks[name]
