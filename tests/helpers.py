from typing import OrderedDict
from unittest import TestCase as UnitTestCase


class TestCase(UnitTestCase):
    @staticmethod
    def assertOrderedDictEqual(od1: OrderedDict, od2: OrderedDict):
        errors = []
        if len(od1.keys()) != len(od2.keys()):
            raise AssertionError("Number of items don't match: {} {}".format(od1, od2))
        for i, j in zip(od1.items(), od2.items()):
            if i[0] != j[0]:
                errors.append("Keys in {} and {} don't match".format(i, j))
            if i[1] != j[1]:
                errors.append("Values in {} and {} don't match".format(i, j))
        if errors:
            raise AssertionError(", ".join(errors))
        return True
