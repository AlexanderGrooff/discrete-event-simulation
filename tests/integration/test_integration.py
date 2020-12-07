from collections import OrderedDict

from simulation.framework import Action, DiscreteSimulation, Timeline, Event, State
from tests.helpers import TestCase


class WaterDropEvent(Event):
    name = "WaterDropEvent"

    def hook(self, state, *args, **kwargs):
        state.set("water", state.get("water", 0) + 1)
        return state


class WaterDropAction(Action):
    name = "WaterDropAction"
    events = [(3, WaterDropEvent())]

    def ready_to_start(self, timeline: Timeline, *args, **kwargs) -> bool:
        return not timeline.action_already_planned(action=self)


class TestSimulationFramework(TestCase):
    def setUp(self):
        self.action = WaterDropAction()
        self.event = self.action.events[0][1]
        self.sim = DiscreteSimulation(max_duration=8, available_actions=[self.action])

    def test_simulation_starts_with_timeline(self):
        self.sim.run()
        self.assertIsNotNone(self.sim.timeline)

    def test_time_stays_at_zero_if_there_are_no_actions(self):
        self.sim.available_actions = []
        self.sim.run()
        self.assertEqual(self.sim.timeline.current_time, 0)

    def test_no_events_are_ran_if_there_are_no_actions(self):
        self.sim.available_actions = []
        self.sim.run()
        self.assertOrderedDictEqual(self.sim.timeline.events, OrderedDict({}))

    def test_events_are_tracked_on_timeline(self):
        self.sim.run()
        self.assertOrderedDictEqual(
            self.sim.timeline.events,
            OrderedDict(
                {
                    3: self.event,
                    6: self.event,
                    9: self.event,  # Even though it's not started, it is planned
                }
            ),
        )

    def test_events_outside_of_max_duration_are_not_started(self):
        self.sim.run()
        _, last_event = self.sim.timeline.last_event_occurrence(WaterDropEvent)
        self.assertFalse(last_event.started)

    def test_actions_are_added_to_timeline(self):
        self.sim.run()
        self.assertOrderedDictEqual(
            self.sim.timeline.actions,
            OrderedDict({0: self.action, 3: self.action, 6: self.action}),
        )

    def test_values_are_updated_in_state(self):
        self.sim.run()
        self.assertDictEqual(self.sim.timeline.current_state.values, {"water": 2})

    def test_initial_state_is_properly_passed_through_in_sim(self):
        self.sim.reset(initial_values={"water": 5000})
        self.sim.run()
        self.assertDictEqual(self.sim.timeline.current_state.values, {"water": 5002})
