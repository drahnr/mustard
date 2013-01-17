# Copyright (C) 2012 Codethink Limited


import markdown

import mustard


class VerificationCriterion(mustard.elementfactory.Element):

    def __init__(self, data):
        mustard.elementfactory.Element.__init__(self, data)

        self.parents = {}
        for ref in data.get('parents', None) or []:
            if ref:
                self.parents[ref] = None
        
        self.mapped_here = {}
        for ref in data.get('mapped-here', []):
            self.mapped_here[ref] = None

    def get_children(self):
        children = []
        for path, item in self.work_items.iteritems():
            if item:
                children.append((path, item))
        return children