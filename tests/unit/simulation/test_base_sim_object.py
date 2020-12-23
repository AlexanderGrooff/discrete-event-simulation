from copy import deepcopy

from simulation.framework import BaseSimObject
from tests.helpers import TestCase


class TestBaseSimObject(TestCase):
    def test_name_defaults_to_class_name(self):
        bso = BaseSimObject()
        self.assertEqual(bso.name, "BaseSimObject")

    def test_inherited_class_takes_over_name(self):
        class TestSimClass(BaseSimObject):
            pass

        bso = TestSimClass()
        self.assertEqual(bso.name, "TestSimClass")

    def test_specified_class_name_overrides_class_name(self):
        class TestSimClass(BaseSimObject):
            name = "Specified base class name"

        bso = TestSimClass()
        self.assertEqual(bso.name, "Specified base class name")

    def test_specified_object_name_overrides_class_name(self):
        class TestSimClass(BaseSimObject):
            name = "Specified base class name"

        bso = TestSimClass(name="Object name")
        self.assertEqual(bso.name, "Object name")

    def test_deepcopied_objects_are_equal(self):
        o1 = BaseSimObject()
        o2 = deepcopy(o1)
        self.assertEqual(o1, o2)

    def test_new_objects_are_not_equal(self):
        o1 = BaseSimObject()
        o2 = BaseSimObject()
        self.assertNotEqual(o1, o2)

    def test_objects_with_same_name_and_id_are_equal(self):
        o1 = BaseSimObject(name="test")
        o2 = BaseSimObject(name="test")
        o2.id = o1.id
        self.assertEqual(o1, o2)

    def test_objects_with_same_name_and_id_but_different_classes_are_not_equal(self):
        class TestSimClass(BaseSimObject):
            pass

        o1 = TestSimClass(name="test")
        o2 = BaseSimObject(name="test")
        o2.id = o1.id
        self.assertNotEqual(o1, o2)
