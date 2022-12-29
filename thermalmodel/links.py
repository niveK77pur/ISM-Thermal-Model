#!/usr/bin/env python3

from __future__ import annotations
from typing import TYPE_CHECKING, Callable, List, Type

if TYPE_CHECKING:
    from .nodes import InterfaceNode


class LinkType():

    def __init__(self, options: dict):
        self.options: dict = options
        self.node1: InterfaceNode = options['node1']
        self.node2: InterfaceNode = options['node2']

    def computeViewingFator(self) -> float:
        raise NotImplementedError()

    def computeHeatExchange(self) -> float:
        raise NotImplementedError()


class ManualLink(LinkType):

    def __init__(self, options: dict):
        super().__init__(options)
        self.func: Callable = options['func']

    def computeViewingFator(self) -> float:
        return self.options['viewingFactor']

    def computeHeatExchange(self) -> float:
        return self.func()


class RadiationLink(LinkType):

    def __init__(self, options: dict):
        super().__init__(options)
        self._radiationArea1: float = options['radiationArea1']
        self._radiationArea2: float = options['radiationArea2']
        self._viewingFactor: float = options['viewingFactor']

    def computeHeatExchange(self) -> float:
        boltzman: float = 5.670374419e-8
        A1 = self._radiationArea1
        A2 = self._radiationArea2
        e1 = self.node1._emissivity
        e2 = self.node2._emissivity
        F = self._viewingFactor
        resistance = boltzman / (
            ( (1 - e1) / (e1 * A1) )
            + (1 / (A1 * F))
            + ( (1 - e2) / (e2 * A2) )
        )
        deltaT = self.node1.getTemperature()**4 - self.node2.getTemperature()**4
        heatTransferRate = - deltaT / resistance
        return heatTransferRate


class ContactLink(LinkType):

    def __init__(self, options: dict):
        super().__init__(options)
        self._contactArea: float = options['contactArea']
        self._resistance: float = options['resistance']

    def computeHeatExchange(self) -> float:
        deltaT = self.node1.getTemperature() - self.node2.getTemperature()
        heatTransferRate = - (deltaT * self._contactArea) / self._resistance
        return heatTransferRate


class ConductionLink(LinkType):

    def __init__(self, options: dict):
        super().__init__(options)
        self._conductionArea: float = options['conductionArea']
        self._conductivity: float = options['conductivity']
        self._length: float = options['length']

    def computeHeatExchange(self) -> float:
        resistance = self._length / (self._conductivity * self._conductionArea)
        deltaT = self.node1.getTemperature() - self.node2.getTemperature()
        heatTransferRate = - deltaT / resistance
        return heatTransferRate


class AmbientLink(LinkType):

    def __init__(self, options: dict):
        super().__init__(options)

    def computeHeatExchange(self) -> float:
        raise NotImplementedError()


class VacuumChamberLink(LinkType):

    def __init__(self, options: dict):
        super().__init__(options)

    def computeHeatExchange(self) -> float:
        raise NotImplementedError()


class Link():

    def __init__(self, node1: InterfaceNode, node2: InterfaceNode,
                 linkTypes: List[Type[LinkType]],
                 parameters: dict):
        self.node1: InterfaceNode = node1
        self.node2: InterfaceNode = node2

        parameters['node1'] = node1
        parameters['node2'] = node2
        self.linkTypes: List[LinkType] = [ L(parameters) for L in linkTypes ]
        self.parameters: dict = parameters

    def computeHeatExchange(self) -> float:
        return sum(( lt.computeHeatExchange() for lt in self.linkTypes ))
