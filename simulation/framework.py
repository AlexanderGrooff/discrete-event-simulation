from collections import OrderedDict
from copy import deepcopy
from typing import (
    OrderedDict as OrderedDictType,
    Optional,
    List,
    Tuple,
    Callable,
    Union,
)
from uuid import uuid4

import loguru

from simulation.types import Time, Timedelta, Weight

logger = loguru.logger


class SimulationError(RuntimeError):
    pass


class State:
    """
    State of the simulation at a given point in time
    """

    values: dict = None
    active_events: List["Action"] = None
    completed_events: List["Action"] = None

    def __init__(
        self,
        values: Optional[dict] = None,
        active_events: List["Action"] = None,
        completed_events: List["Action"] = None,
    ):
        self.values = values or {}
        self.active_events = active_events or []
        self.completed_events = completed_events or []

    def get(self, key, default=None):
        return self.values.get(key, default)

    def set(self, key, value) -> "State":
        self.values[key] = value
        return self

    def complete_event(self, event: "Action") -> "State":
        active_event = [ae for ae in self.active_events if ae.id == event.id][0]
        self.active_events.remove(active_event)
        self.completed_events.append(active_event)
        return self


class BaseSimObject:
    weight: Weight = 0
    started: bool = False

    def __init__(self, weight: Weight = None, *args, **kwargs):
        self.weight = weight or self.weight or 0


class Event(BaseSimObject):
    """
    Event is scheduled by an action
    """

    id = None
    name: str = None
    started: bool = False

    def __init__(self, name: str = None, hook: Callable = None, weight: Weight = None):
        super(Event, self).__init__(weight=weight)
        self.id = str(uuid4())
        self.name = name or self.name or self.id
        self.hook = hook or self.hook

    def __repr__(self):
        return "{} - {}".format(self.name, self.id)

    def __call__(self, state: State, *args, **kwargs) -> State:
        self.started = True
        return self.hook(state=state, *args, **kwargs)

    def __eq__(self, other: "Event"):
        return self.id == other.id and self.name == other.name


class Action(BaseSimObject):
    """
    Actions at a point in time that trigger a series of events
    """

    id = None
    name = None
    started = False
    is_complete = False
    events: List[Tuple[Timedelta, Event]] = None

    def __init__(
        self,
        name: str = None,
        duration: float = 0,
        events: List[Tuple[Timedelta, Event]] = None,
        weight: Weight = None,
    ):
        super(Action, self).__init__(weight=weight)
        self.duration = duration
        self.id = str(uuid4())
        self.name = name or self.name or self.id
        self.events = events or self.events or []
        self.weight = weight or self.weight or 0

    def ready_to_start(self, timeline: "Timeline", *args, **kwargs) -> bool:
        return not self.started  # TODO

    def __repr__(self):
        return "{} - {}".format(self.name, self.id)

    def __eq__(self, other: "Action"):
        return self.id == other.id and self.name == other.name


class Timeslot:
    items: OrderedDictType[Weight, List[BaseSimObject]] = None

    def __init__(
        self, items: Optional[Union[BaseSimObject, List[BaseSimObject]]] = None
    ):
        items = items or []
        if not isinstance(items, list):
            items = [items]
        self.items = OrderedDict()
        for item in items:
            if self.items.get(item.weight):
                self.items[item.weight].append(item)
            else:
                self.items[item.weight] = [item]
        self.sort()

    def sort(self) -> "Timeslot":
        self.items = OrderedDict(
            sorted(self.items.items(), reverse=True)
        )  # High weight has prio
        return self

    def add(self, item: BaseSimObject) -> "Timeslot":
        self.items[item.weight] = self.items.get(item.weight, [])
        self.items[item.weight].append(item)
        self.sort()
        return self

    def to_list(self) -> List[BaseSimObject]:
        flat_list = []
        for i in self.items.values():
            for j in i:
                flat_list.append(j)
        return flat_list

    def upcoming_events(self) -> List[BaseSimObject]:
        return [i for i in self.to_list() if not i.started]

    def next_event(self) -> Optional[BaseSimObject]:
        try:
            return self.upcoming_events()[0]  # TODO: Not as efficient as possible
        except IndexError:
            pass

    def __eq__(self, other: "Timeslot") -> bool:
        return self.to_list() == other.to_list()


class Timeline:
    """
    Tracks the state and events over time
    """

    states: OrderedDictType[Time, State] = None
    events: OrderedDictType[Time, Timeslot] = None
    actions: OrderedDictType[Time, Timeslot] = None

    def __init__(self, initial_values: Optional[dict] = None):
        initial_state = State(
            active_events=[], completed_events=[], values=initial_values
        )
        self.states = OrderedDict({0: initial_state})
        self.events = OrderedDict()
        self.actions = OrderedDict()

    @property
    def last_time(self) -> Optional[Time]:
        try:
            return next(reversed(self.states.keys()))
        except StopIteration:
            pass

    @property
    def current_time(self) -> Time:
        return self.last_time or 0

    @property
    def current_state(self) -> State:
        return self.states[self.current_time]

    @property
    def events_to_come(self) -> List[Event]:
        upcoming_events = []
        for t, timeslot in self.events.items():
            if t >= self.current_time:
                upcoming_events.extend(timeslot.upcoming_events())
        return upcoming_events

    @property
    def actions_to_come(self) -> List[Action]:
        upcoming_actions = []
        for t, timeslot in self.actions.items():
            if t >= self.current_time:
                upcoming_actions.extend(timeslot.upcoming_events())
        return upcoming_actions

    def schedule_action(self, action: Action):
        curr_time = self.current_time
        logger.debug("Scheduling action {} at time {}".format(action, curr_time))
        self.actions[curr_time] = self.actions.get(curr_time, Timeslot())
        self.actions[curr_time].add(item=action)
        for td, e in action.events:
            self.schedule_event(event=e, time=curr_time + td)

    def schedule_event(self, event: Event, time: Time = None):
        logger.debug("Scheduling event {} at time {}".format(event, time))
        time = time or self.current_time
        self.events[time] = self.events.get(time, Timeslot())
        self.events[time].add(item=event)
        # Sort by time
        self.events = OrderedDict(sorted(self.events.items()))

    def set_state(self, state: State, time: Time):
        self.states[time] = state

    def get_first_upcoming_event(
        self, time: Time = None
    ) -> Optional[Tuple[Time, Event]]:
        time = time or self.current_time
        for t, timeslot in self.events.items():
            if t >= time and (e := timeslot.next_event()):
                return t, e
        logger.debug("There are no upcoming events")

    def last_event_occurrence(self, event_type) -> Optional[Tuple[Time, Event]]:
        for t, timeslot in sorted(self.events.items(), reverse=True):
            for e in timeslot.to_list():
                if isinstance(e, event_type):
                    return t, e

    def action_already_planned(self, action) -> bool:
        return any([e for e in self.actions_to_come if isinstance(e, action.__class__)])


class DiscreteSimulation:
    available_actions = None
    timeline: Timeline = None
    max_duration: Time = None

    def __init__(
        self,
        max_duration: Time,
        available_actions: List[Action],
        initial_values: Optional[dict] = None,
    ):
        self.max_duration = max_duration
        self.available_actions = available_actions
        self.reset(initial_values)

    def reset(self, initial_values: Optional[dict] = None):
        logger.debug("Prepping simulation to run")
        self.timeline = Timeline(initial_values=initial_values)

    def run(self) -> State:
        logger.info("Starting simulation with duration {}".format(self.max_duration))
        while self.timeline.current_time < self.max_duration:
            # Schedule actions until no more available
            for action in self.get_available_actions():
                self.timeline.schedule_action(action=action)

            # Run next event
            if not (event_occurrence := self.timeline.get_first_upcoming_event()):
                # TODO: What to do if there is no action or event? Find next time available action?
                logger.warning(
                    "No events or actions available. Stopping simulation at {} time".format(
                        self.timeline.current_time
                    )
                )
                break
            new_time = event_occurrence[0]
            event = event_occurrence[1]
            if new_time > self.max_duration:
                logger.info(
                    "Next event {} starts after max duration. Stopping simulation".format(
                        event
                    )
                )
                break
            logger.debug("Executing event {} at time {}".format(event, new_time))
            new_state = event(state=self.timeline.current_state)

            # Apply new state
            self.timeline.set_state(state=new_state, time=new_time)
            logger.info(
                "Time: {}   -   State: {}".format(
                    self.timeline.current_time, new_state.values
                )
            )

        return self.timeline.current_state

    def get_available_actions(self) -> List[Action]:
        return deepcopy(
            [
                aa
                for aa in sorted(
                    self.available_actions, reverse=True, key=lambda a: a.weight
                )
                if aa.ready_to_start(timeline=self.timeline)
            ]
        )
