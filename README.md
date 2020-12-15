# Discrete event simulation

This package can be used to create a discrete event simulation based on your parameters. Just install the library (pypi library is WIP) and use
the `DiscreteSimulation` class to run with your environment.

## How to apply it to your scenario

Check out the [examples](https://github.com/AlexanderGrooff/discrete-event-simulation/tree/master/examples) where scenarios are sketched out using this framework.
The idea is that you state one or more available actions that the simulation can pick from which have a starting condition and events to trigger.

The events that are triggered by actions will modify the state, which is tracked in the simulation's `Timeline`.

## Development

Make a virtualenv, install requirements and run `tox` to ensure everything works. It works from Python 3.8+.

```
mkvirtualenv -a . -p python3 $(basename $(pwd))
pip install -r requirements.txt
tox
```
