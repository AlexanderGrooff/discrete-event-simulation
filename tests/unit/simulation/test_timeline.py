from collections import OrderedDict

from simulation.framework import Timeline, Action
from tests.helpers import TestCase


class TestTimeline(TestCase):
    def test_multiple_actions_can_be_scheduled_on_the_same_time_with_same_weight(self):
        a1 = Action()
        a2 = Action()
        tl = Timeline()
        tl.schedule_action(a1)
        tl.schedule_action(a2)

        self.assertOrderedDictEqual(
            tl.actions, OrderedDict({0: OrderedDict({0: [a1, a2]})})
        )

    def test_multiple_actions_can_be_scheduled_on_the_same_time_with_different_weight(self):
        a1 = Action(weight=0)
        a2 = Action(weight=1)
        tl = Timeline()
        tl.schedule_action(a1)
        tl.schedule_action(a2)

        self.assertOrderedDictEqual(
            tl.actions, OrderedDict({0: OrderedDict({0: [a1, a2]})})
        )
