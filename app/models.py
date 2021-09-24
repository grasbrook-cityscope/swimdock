from dataclasses import dataclass
from typing import Dict, TypedDict
from os import path, getcwd

default_data_dir = (path.dirname(getcwd()) + "/data/").replace("//", "/")
default_baseline_input = path.join(default_data_dir, "scenario.inp")


@dataclass(frozen=True)
class ScenarioPaths:
    id: str
    baseline_input: str = default_baseline_input
    base: str = default_data_dir

    @property
    def input(self):
        return path.join(self.base, self.id + "_scenario.inp")

    @property
    def output(self):
        return path.join(self.base, self.id + "_scenario.out")

    @property
    def report(self):
        return path.join(self.base, self.id + "_scenario.rpt")


@dataclass(frozen=True)
class SwimdockUser:
    user_id: str
    scenarios: dict[str, ScenarioPaths]


class LayerRainEvent(TypedDict):
    return_period: int
    duration: int


class LayerModelUpdate(TypedDict):
    subcatchment_id: str
    outlet_id: str


class CityPyoLayer(TypedDict):
    hash: str
    model_updates: list[LayerModelUpdate]
    rain_event: LayerRainEvent
    calculation_method: str


class CityPyoUser(TypedDict):
    username: str
    password: str


class CityPyoUsers(TypedDict):
    users: list[CityPyoUser]


CityPyoLayers = Dict[str, CityPyoLayer]
