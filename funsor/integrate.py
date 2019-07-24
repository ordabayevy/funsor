from __future__ import absolute_import, division, print_function

import functools
from collections import OrderedDict

import funsor.interpreter as interpreter
import funsor.ops as ops
from funsor.contract import Contract
from funsor.terms import Funsor, Reduce, eager


class Integrate(Funsor):
    """
    Funsor representing an integral wrt a log density funsor.
    """
    def __init__(self, log_measure, integrand, reduced_vars):
        assert isinstance(log_measure, Funsor)
        assert isinstance(integrand, Funsor)
        assert isinstance(reduced_vars, frozenset)
        inputs = OrderedDict((k, d) for term in (log_measure, integrand)
                             for (k, d) in term.inputs.items()
                             if k not in reduced_vars)
        output = integrand.output
        fresh = frozenset()
        bound = reduced_vars
        super(Integrate, self).__init__(inputs, output, fresh, bound)
        self.log_measure = log_measure
        self.integrand = integrand
        self.reduced_vars = reduced_vars


@eager.register(Integrate, Funsor, Funsor, frozenset)
def eager_integrate(log_measure, integrand, reduced_vars):
    return (log_measure.exp() * integrand).reduce(ops.add, reduced_vars)


__all__ = [
    'Integrate',
]
