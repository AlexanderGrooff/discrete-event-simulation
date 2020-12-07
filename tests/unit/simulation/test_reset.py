from simulation.framework import DiscreteSimulation
from tests.helpers import TestCase


class TestSimulationFramework(TestCase):
    def setUp(self):
        self.sim = DiscreteSimulation(max_duration=8, available_actions=[])

    def test_reset_creates_new_timeline(self):
        original_timeline = self.sim.timeline
        self.sim.reset()
        self.assertNotEqual(self.sim.timeline, original_timeline)

    def test_reset_applies_initial_values(self):
        self.sim.reset(initial_values={"water": 5000})
        self.assertDictEqual(self.sim.timeline.current_state.values, {"water": 5000})
