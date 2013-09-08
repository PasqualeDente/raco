
import collections
import raco.algebra
import raco.scheme as scheme

class FakeDatabase:
    def __init__(self):
        # Map from relation names (strings) to tuples of (Bag, scheme.Scheme)
        self.tables = {}

    def evaluate(self, op):
        '''Evaluate a relational algebra operation.

        For "query-type" operators, return a tuple iterator.
        For store queries, the return value is None.
        '''
        print str(op)
        method = getattr(self, op.opname().lower())
        return method(op)

    def evaluate_to_bag(self, op):
        '''Return a bag (collections.Counter instance) for the operation'''
        return collections.Counter(self.evaluate(op))

    def ingest(self, relation_key, contents, scheme):
        '''Directly load raw data into the database'''
        self.tables[relation_key] = (contents, scheme)

    def get_scheme(self, relation_key):
        bag, scheme = self.tables[relation_key]
        return scheme

    def scan(self, op):
        bag, scheme = self.tables[op.relation.name]
        return bag.elements()
