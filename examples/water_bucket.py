from random import randint

import loguru

from simulation.framework import Action, DiscreteSimulation, Event, State, Timeline

logger = loguru.logger


class WaterDropEvent(Event):
    name = "WaterDropEvent"

    def hook(self, state: State):
        return state.set("drops", state.get("drops") + randint(1, 10))


class WaterDropAction(Action):
    name = "WaterdropAction"
    events = [(3, WaterDropEvent())]

    def ready_to_start(self, timeline: Timeline, *args, **kwargs) -> bool:
        return not timeline.action_already_planned(action=self)


class WaterBucketOverflowEvent(Event):
    name = "WaterBucketOverflowEvent"
    weight = 2  # Overflow happens before waterdrop

    def hook(self, state: State):
        logger.info("Overflowing bucket")
        state = state.set("drops", 0)
        return state.set("overflows", state.get("overflows") + 1)


class WaterBucketOverflowAction(Action):
    name = "WaterBucketOverflowAction"
    events = [(1, WaterBucketOverflowEvent())]

    def ready_to_start(self, timeline: Timeline, *args, **kwargs) -> bool:
        return timeline.current_state.get(
            "drops"
        ) > 100 and not timeline.action_already_planned(action=self)


sim = DiscreteSimulation(
    initial_values={"drops": 0, "overflows": 0},
    available_actions=[WaterDropAction(), WaterBucketOverflowAction()],
    max_duration=600,
)
sim.run()

logger.info(
    "Bucket is filled with {drops} drops and overflowed {overflows} time(s)".format(
        **sim.timeline.current_state.values
    )
)
