from copy import deepcopy
from unittest.mock import Mock

from simulation.framework import Event
from tests.helpers import TestCase


class TestEvent(TestCase):
    def test_copied_events_are_equal(self):
        e = Event(name="testevent", hook=Mock())
        self.assertEqual(e, deepcopy(e))
