#!/usr/bin/env python3

from nodes import InterfaceNode


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

    def computeRadiationHeatExchange(self) -> float:
        raise NotImplementedError()

    def computeConductionHeatExchange(self) -> float:
        raise NotImplementedError()

    def computeConvectionHeatExchange(self) -> float:
        raise NotImplementedError()

    def computeHeatExchange() -> float:
        radiation = computeRadiationHeatExchange()
        conduction = computeConductionHeatExchange()
        convection = computeConvectionHeatExchange()
        return radiation + conduction + convection
