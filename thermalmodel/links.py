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

    def __init__(self, node1: InterfaceNode, node2: InterfaceNode, parameters: dict):
        self.node1: InterfaceNode = node1
        self.node2: InterfaceNode = node2

        self.linkType: LinkType = parameters.get('linkType', None)
        # TODO: explicitly extract missing parameters which are necessary
        self.parameters: dict = parameters

    def _computeRadiationHeatExchange(self) -> float:
        raise NotImplementedError()

    def _computeConductionHeatExchange(self) -> float:
        raise NotImplementedError()

    def _computeConvectionHeatExchange(self) -> float:
        raise NotImplementedError()

    def computeHeatExchange(self) -> float:
        radiation = self._computeRadiationHeatExchange()
        conduction = self._computeConductionHeatExchange()
        convection = self._computeConvectionHeatExchange()
        return radiation + conduction + convection
