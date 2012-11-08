# Copyright (C) 2012 Codethink Limited


import cliapp

import mustard


class Project(mustard.elementfactory.Element):

    def __init__(self):
        mustard.elementfactory.Element.__init__(self, {})
        self.kind = 'project'
        self.copyright = None
        self.elements = {}
        self.predefined_filters = []

    def _propagate_requirement(self, path, requirement):
        self.elements[path] = requirement

        self._resolve_tags(path, requirement)
        self._resolve_mapped_to(path, requirement)
        self._resolve_parent_requirement(path, requirement)
        self._resolve_work_items(path, requirement)
        self._resolve_tests(path, requirement)

    def _propagate_tag(self, path, tag):
        self.elements[path] = tag

        self._resolve_tagged(path, tag)

    def _propagate_architecture(self, path, architecture):
        self.elements[path] = architecture

        self._resolve_tags(path, architecture)
        self._resolve_mapped_here(path, architecture)
        self._resolve_parent_component(path, architecture)
        self._resolve_components(path, architecture)
        self._resolve_integration_strategy(path, architecture)
        self._resolve_work_items(path, architecture)

    def _propagate_component(self, path, component):
        self.elements[path] = component

        self._resolve_tags(path, component)
        self._resolve_parent_architecture(path, component)
        self._resolve_architecture(path, component)
        self._resolve_interfaces(path, component)
        self._resolve_mapped_here(path, component)
        self._resolve_work_items(path, component)
        self._resolve_tests(path, component)

    def _propagate_work_item(self, path, item):
        self.elements[path] = item

        self._resolve_tags(path, item)
        self._resolve_parents(path, item)

    def _propagate_interface(self, path, interface):
        self.elements[path] = interface

        self._resolve_tags(path, interface)
        self._resolve_interface_component(path, interface)
        self._resolve_mapped_here(path, interface)
        self._resolve_work_items(path, interface)
        self._resolve_tests(path, interface)

    def _propagate_integration_strategy(self, path, strategy):
        self.elements[path] = strategy

        self._resolve_tags(path, strategy)
        self._resolve_strategy_architecture(path, strategy)
        self._resolve_mapped_here(path, strategy)
        self._resolve_work_items(path, strategy)
        self._resolve_tests(path, strategy)

    def _propagate_test(self, path, test):
        self.elements[path] = test

        self._resolve_tags(path, test)
        self._resolve_mapped_here(path, test)
        self._resolve_work_items(path, test)
        self._resolve_test_parents(path, test)

    def _resolve_tags(self, path, element):
        for ref in element.tags.iterkeys():
            if ref in self.elements:
                element.tags[ref] = self.elements[ref]
                self.elements[ref].tagged[path] = element

    def _resolve_tagged(self, path, tag):
        for ref, element in self.elements.iteritems():
            if path in element.tags:
                element.tags[path] = tag
                tag.tagged[ref] = element

    def _resolve_parent_component(self, path, element):
        ref = element.parent[0]
        if ref in self.elements:
            self.elements[ref].architecture = (path, element)
            element.parent = (ref, self.elements[ref])

    def _resolve_interface_component(self, path, element):
        ref = element.parent[0]
        if ref in self.elements:
            self.elements[ref].interfaces[path] = element
            element.parent = (ref, self.elements[ref])

    def _resolve_components(self, path, architecture):
        for ref, element in self.elements.iteritems():
            if element.kind == 'component':
                if element.parent[0] == path:
                    element.parent = (path, architecture)
                    architecture.components[ref] = element

    def _resolve_parent_architecture(self, path, element):
        ref = element.parent[0]
        if ref in self.elements:
            self.elements[ref].components[path] = element
            element.parent = (ref, self.elements[ref])

    def _resolve_architecture(self, path, component):
        for ref, element in self.elements.iteritems():
            if element.kind == 'architecture':
                if element.parent[0] == path:
                    element.parent = (path, component)
                    component.architecture = (ref, element)

    def _resolve_interfaces(self, path, component):
        for ref, element in self.elements.iteritems():
            if element.kind == 'interface':
                if element.parent[0] == path:
                    element.parent = (path, component)
                    component.interfaces[ref] = element

    def _resolve_mapped_to(self, path, requirement):
        for ref, element in self.elements.iteritems():
            if hasattr(element, 'mapped_here'):
                if path in element.mapped_here:
                    element.mapped_here[path] = requirement
                    requirement.mapped_to[ref] = element
            if path == element.parent[0]:
                element.parent = (path, requirement)
                requirement.subrequirements[ref] = element

    def _resolve_mapped_here(self, path, element):
        for ref in element.mapped_here:
            if ref in self.elements:
                element.mapped_here[ref] = self.elements[ref]
                self.elements[ref].mapped_to[path] = element

    def _resolve_parent_requirement(self, path, requirement):
        ref = requirement.parent[0]
        if ref in self.elements:
            requirement.parent = (ref, self.elements[ref])
            self.elements[ref].subrequirements[path] = requirement

    def _resolve_work_items(self, path, element):
        for ref, other in self.elements.iteritems():
            if other.kind == 'work-item':
                if path in other.parents:
                    other.parents[path] = element
                    element.work_items[ref] = other

    def _resolve_parents(self, path, element):
        for ref in element.parents.iterkeys():
            if ref in self.elements:
                self.elements[ref].work_items[path] = element
                element.parents[ref] = self.elements[ref]

    def _resolve_integration_strategy(self, path, arch):
        for ref, element in self.elements.iteritems():
            if element.kind == 'integration-strategy':
                if path == element.parent[0]:
                    element.parent = (path, arch)
                    self.integration_strategy = (ref, element)

    def _resolve_strategy_architecture(self, path, strategy):
        ref = strategy.parent[0]
        if ref in self.elements:
            strategy.parent = (ref, self.elements[ref])
            self.elements[ref].integration_strategy = (path, strategy)

    def _resolve_test_parents(self, path, test):
        for ref in test.parents.iterkeys():
            if ref in self.elements:
                self.elements[ref].tests[path] = test
                test.parents[ref] = self.elements[ref]

    def _resolve_tests(self, path, element):
        for ref, other in self.elements.iteritems():
            if other.kind == 'test':
                if path in other.parents:
                    other.parents[path] = element
                    element.tests[ref] = other

    def find(self, kind):
        for path, element in self.elements.iteritems():
            if element.kind == kind:
                yield path, element
