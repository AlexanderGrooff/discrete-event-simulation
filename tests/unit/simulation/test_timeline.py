from collections import OrderedDict
from random import randint

from simulation.framework import Timeline, Event, Timeslot, Action
from tests.helpers import TestCase


class TestTimeline(TestCase):
    def test_last_event_can_be_retrieved(self):
        es = [
            Event(hook=lambda *args, **kwargs: 123, weight=randint(0, 5))
            for _ in range(100)
        ]
        tl = Timeline()
        for i, e in enumerate(es):
            tl.schedule_event(event=e, time=i)
        t, last_event = tl.last_event_occurrence(Event)
        self.assertEqual(last_event, es[-1])
        self.assertEqual(t, 99)

    def test_next_event_occurrence_can_be_retrieved(self):
        es = [
            Event(hook=lambda *args, **kwargs: 123, weight=randint(0, 5))
            for _ in range(100)
        ]
        tl = Timeline()
        for i, e in enumerate(es):
            tl.schedule_event(event=e, time=i)
        t, next_event = tl.get_first_upcoming_event()
        self.assertEqual(next_event, es[0])
        self.assertEqual(t, 0)

    def test_events_are_ordered_by_time(self):
        e1 = Event(hook=lambda *args, **kwargs: 123)
        e2 = Event(hook=lambda *args, **kwargs: 123)
        tl = Timeline()
        tl.schedule_event(e1, time=2)
        tl.schedule_event(e2, time=1)
        self.assertOrderedDictEqual(
            OrderedDict(
                {
                    1: Timeslot(items=[e2]),
                    2: Timeslot(items=[e1]),
                }
            ),
            tl.events,
        )

    def test_actions_are_added_sequentially(self):
        a1 = Action()
        a2 = Action()
        tl = Timeline()
        tl.schedule_action(a1)
        tl.schedule_action(a2)
        self.assertOrderedDictEqual(
            OrderedDict(
                {
                    0: Timeslot(items=[a1, a2]),
                }
            ),
            tl.actions,
        )
