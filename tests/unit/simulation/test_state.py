from copy import deepcopy

from simulation.framework import State, Action
from tests.helpers import TestCase


class TestState(TestCase):
    def test_state_starts_with_no_active_events(self):
        s = State()
        self.assertEqual(s.active_events, [])

    def test_state_starts_with_no_completed_events(self):
        s = State()
        self.assertEqual(s.completed_events, [])

    def test_state_starts_with_no_values(self):
        s = State()
        self.assertEqual(s.values, {})

    def test_state_completes_the_specified_event(self):
        e = Action()
        s = State(active_events=[e])
        s.complete_event(e)
        self.assertEqual(s.completed_events, [e])
        self.assertEqual(s.active_events, [])

    def test_state_completes_the_copied_event(self):
        e = Action()
        s = State(active_events=[e])
        s.complete_event(deepcopy(e))
        self.assertEqual(s.completed_events, [e])
        self.assertEqual(s.active_events, [])

    def test_complete_raises_error_if_event_id_isnt_found(self):
        s = State(active_events=[Action()])
        with self.assertRaises(IndexError):
            s.complete_event(Action())
