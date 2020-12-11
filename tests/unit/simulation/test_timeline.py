from random import randint

from simulation.framework import Timeline, Event
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
