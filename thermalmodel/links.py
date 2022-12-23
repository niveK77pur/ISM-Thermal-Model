#!/usr/bin/env python3

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .nodes import InterfaceNode


class LinkType():

    def __init__(self, options: dict):
        self.options: dict = options

    def computeViewingFator(self) -> float:
        raise NotImplementedError()


class Manual(LinkType):

    def __init__(self, options: dict):
        super().__init__(options)

    def computeViewingFator(self) -> float:
        return self.options['viewingFactor']


class Link():

    def __init__(self, node1: InterfaceNode, node2: InterfaceNode,
                 parameters: dict):
        self.node1: InterfaceNode = node1
        self.node2: InterfaceNode = node2

        self.linkType: LinkType = parameters.get('linkType', None)
        # TODO: explicitly extract missing parameters which are necessary
        self._resistance: float = parameters.get('resistance', None)
        self._length: float = parameters.get('length', None)
        self._area: float = parameters.get('area', None)  # QUESTION: can this area be taken from interface node?
        self._conductivity: float = parameters.get('conductivity', None)
        self._viewingFactor: float = parameters.get('viewingFactor', None)
        self.parameters: dict = parameters

    def _computeRadiationHeatExchange(self) -> float:
        boltzman: float = 5.670374419e-8
        A1 = self.node1._interfaceArea  # TODO: rename _interfaceArea as _radiationArea
        A2 = self.node2._interfaceArea
        e1 = self.node1._emissivity
        e2 = self.node2._emissivity
        F = self.linkType.computeViewingFator() if self.linkType else self._viewingFactor
        resistance = boltzman / (
            ( (1 - e1) / (e1 * A1) )
            + (1 / (A1 * F))
            + ( (1 - e2) / (e2 * A2) )
        )
        deltaT = self.node1.getTemperature()**4 - self.node2.getTemperature()**4
        heatTransferRate = deltaT / resistance
        return heatTransferRate

    def _computeContactHeatExchange(self) -> float:
        assert type(self._area) in (float, int)
        assert type(self._resistance) in (float, int)
        deltaT = self.node1.getTemperature() - self.node2.getTemperature()
        heatTransferRate = (deltaT * self._area) / self._resistance
        return heatTransferRate

    def _computeConductionHeatExchange(self) -> float:
        assert type(self._area) in (float, int)
        assert type(self._length) in (float, int)
        assert type(self._conductivity) in (float, int)
        resistance = self._length / (self._conductivity * self._area)
        deltaT = self.node1.getTemperature() - self.node2.getTemperature()
        heatTransferRate = deltaT / resistance
        return heatTransferRate

    def _computeConvectionHeatExchange(self) -> float:
        raise NotImplementedError()

    def computeHeatExchange(self) -> float:
        elements = {}
        elements['radiation'] = self._computeRadiationHeatExchange()
        if self._length == 0:
            elements['contact'] = self._computeContactHeatExchange()
        elif self._length > 0:
            elements['conduction'] = self._computeConductionHeatExchange()
        # elements['convection'] = self._computeConvectionHeatExchange()
        return sum(elements.values())
