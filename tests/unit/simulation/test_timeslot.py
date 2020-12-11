from collections import OrderedDict

from simulation.framework import Timeslot, Event
from tests.helpers import TestCase


class TestTimeslot(TestCase):
    def test_timeslot_starts_empty(self):
        ts = Timeslot()
        self.assertOrderedDictEqual(ts.items, OrderedDict())

    def test_timeslot_orders_items_automatically(self):
        highweightevent = Event(weight=100, hook=lambda *args, **kwargs: 123)
        lowweightevent = Event(weight=0, hook=lambda *args, **kwargs: 123)
        ts = Timeslot(items=lowweightevent)
        ts.add(highweightevent)
        self.assertOrderedDictEqual(
            ts.items, OrderedDict({100: [highweightevent], 0: [lowweightevent]})
        )
        self.assertListEqual(ts.to_list(), [highweightevent, lowweightevent])

    def test_items_with_same_weight_are_placed_after_each_other(self):
        highweightevent1 = Event(weight=100, hook=lambda *args, **kwargs: 123)
        highweightevent2 = Event(weight=100, hook=lambda *args, **kwargs: 123)
        lowweightevent1 = Event(weight=0, hook=lambda *args, **kwargs: 123)
        lowweightevent2 = Event(weight=0, hook=lambda *args, **kwargs: 123)
        ts = Timeslot(items=[lowweightevent1, highweightevent1])
        ts.add(highweightevent2)
        ts.add(lowweightevent2)
        self.assertOrderedDictEqual(
            ts.items,
            OrderedDict(
                {
                    100: [highweightevent1, highweightevent2],
                    0: [lowweightevent1, lowweightevent2],
                }
            ),
        )
        self.assertListEqual(
            ts.to_list(),
            [highweightevent1, highweightevent2, lowweightevent1, lowweightevent2],
        )
