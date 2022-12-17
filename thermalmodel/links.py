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
        self._R: float = parameters.get('R', None)  # TODO: change name
        self._length: float = parameters.get('length', None)
        self._area: float = parameters.get('area', None)  # QUESTION: can this area be taken from interface node?
        self._conductivity: float = parameters.get('conductivity', None)
        self.parameters: dict = parameters

    def _computeRadiationHeatExchange(self) -> float:
        raise NotImplementedError()

    def _computeContactHeatExchange(self) -> float:
        assert type(self._area) in (float, int)
        assert type(self._R) in (float, int)
        deltaT = self.node1.getTemperature() - self.node2.getTemperature()
        Q = deltaT * self._area / self._R
        return Q

    def _computeConductionHeatExchange(self) -> float:
        assert type(self._area) in (float, int)
        assert type(self._length) in (float, int)
        assert type(self._conductivity) in (float, int)
        R = self._length / self._conductivity * self._area
        deltaT = self.node1.getTemperature() - self.node2.getTemperature()
        Q = deltaT / R
        return Q

    def _computeConvectionHeatExchange(self) -> float:
        raise NotImplementedError()

    def computeHeatExchange(self) -> float:
        radiation = self._computeRadiationHeatExchange()
        if self._length == 0:
            contact = self._computeContactHeatExchange()
            conduction = 0
        elif self._length > 0:
            contact = 0
            conduction = self._computeConductionHeatExchange()
        convection = self._computeConvectionHeatExchange()
        return radiation + contact + conduction + convection
