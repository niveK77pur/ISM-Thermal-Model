#!/usr/bin/env python3

from __future__ import annotations
from typing import TYPE_CHECKING, List, Type

if TYPE_CHECKING:
    from .nodes import InterfaceNode


class LinkType():

    def __init__(self, options: dict):
        self.options: dict = options
        self.node1: InterfaceNode = options.get('node1')
        self.node2: InterfaceNode = options.get('node2')
        self._resistance: float = options.get('resistance', None)
        self._length: float = options.get('length', None)
        self._conductivity: float = options.get('conductivity', None)
        self._viewingFactor: float = options.get('viewingFactor', None)
        print("TODO: check if node values get updated here (i.e. node is pass by reference)")  # TODO

    def computeViewingFator(self) -> float:
        raise NotImplementedError()

    def computeHeatExchange(self) -> float:
        raise NotImplementedError()


class Manual(LinkType):

    def __init__(self, options: dict):
        super().__init__(options)

    def computeViewingFator(self) -> float:
        return self.options['viewingFactor']


class RadiationLink(LinkType):

    def __init__(self, options: dict):
        super().__init__(options)
        self._radiationArea1: float = options.get('radiationArea1')
        self._radiationArea2: float = options.get('radiationArea2')

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
        self._contactArea: float = options.get('contactArea')

    def computeHeatExchange(self) -> float:
        assert type(self._contactArea) in (float, int)
        assert type(self._resistance) in (float, int)
        deltaT = self.node1.getTemperature() - self.node2.getTemperature()
        heatTransferRate = - (deltaT * self._contactArea) / self._resistance
        return heatTransferRate


class ConductionLink(LinkType):

    def __init__(self, options: dict):
        super().__init__(options)
        self._conductionArea: float = options.get('conductionArea')

    def computeHeatExchange(self) -> float:
        assert type(self._length) in (float, int)
        assert type(self._conductivity) in (float, int)
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
