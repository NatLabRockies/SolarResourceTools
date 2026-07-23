"""State models and adapters for transitioning away from legacy dict state."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AirMassState:
    ktMax: Any = 0
    knMax: Any = 0
    kdMax: Any = 0
    shapeLeft: int = 0
    shapeRight: int = 0
    posLeft: int = 0
    posRight: int = 0
    lBound: list = field(default_factory=lambda: [0])
    rBound: list = field(default_factory=lambda: [0])
    In: Any = 0
    Out: Any = 0
    Active: int = 0
    Ignored: int = 0
    Total: int = 0
    Err_L: Any = 0
    Err_R: Any = 0
    activeLBound: list = field(default_factory=lambda: [0])
    activeRBound: list = field(default_factory=lambda: [0])
    xLB: list = field(default_factory=lambda: [0])
    yLB: list = field(default_factory=lambda: [0])
    xRB: list = field(default_factory=lambda: [0])
    yRB: list = field(default_factory=lambda: [0])


@dataclass
class AppState:
    month: str = ""
    year: str = "All"
    integration: int = 60
    plane: int = 1
    threshold: float = 1.0
    xAxis: str = "KT"
    yAxis: str = "KN"
    lowAM: AirMassState = field(default_factory=AirMassState)
    medAM: AirMassState = field(default_factory=AirMassState)
    highAM: AirMassState = field(default_factory=AirMassState)


def get_airmass(state: AppState, amass: str) -> AirMassState:
    if amass == "low":
        return state.lowAM
    if amass == "med":
        return state.medAM
    if amass == "high":
        return state.highAM
    raise ValueError("Unsupported airmass value: {}".format(amass))


def _build_airmass(legacy_am: dict) -> AirMassState:
    return AirMassState(
        ktMax=legacy_am.get("ktMax", 0),
        knMax=legacy_am.get("knMax", 0),
        kdMax=legacy_am.get("kdMax", 0),
        shapeLeft=legacy_am.get("shapeLeft", 0),
        shapeRight=legacy_am.get("shapeRight", 0),
        posLeft=legacy_am.get("posLeft", 0),
        posRight=legacy_am.get("posRight", 0),
        lBound=list(legacy_am.get("lBound", [0])),
        rBound=list(legacy_am.get("rBound", [0])),
        In=legacy_am.get("In", 0),
        Out=legacy_am.get("Out", 0),
        Active=legacy_am.get("Active", 0),
        Ignored=legacy_am.get("Ignored", 0),
        Total=legacy_am.get("Total", 0),
        Err_L=legacy_am.get("Err_L", 0),
        Err_R=legacy_am.get("Err_R", 0),
        activeLBound=list(legacy_am.get("activeLBound", [0])),
        activeRBound=list(legacy_am.get("activeRBound", [0])),
        xLB=list(legacy_am.get("xLB", [0])),
        yLB=list(legacy_am.get("yLB", [0])),
        xRB=list(legacy_am.get("xRB", [0])),
        yRB=list(legacy_am.get("yRB", [0])),
    )


def from_legacy_dict(data: dict) -> AppState:
    return AppState(
        month=data.get("month", ""),
        year=data.get("year", "All"),
        integration=data.get("integration", 60),
        plane=data.get("plane", 1),
        threshold=data.get("threshold", 1.0),
        xAxis=data.get("xAxis", "KT"),
        yAxis=data.get("yAxis", "KN"),
        lowAM=_build_airmass(data.get("lowAM", {})),
        medAM=_build_airmass(data.get("medAM", {})),
        highAM=_build_airmass(data.get("highAM", {})),
    )


def _write_airmass(legacy_am: dict, am_state: AirMassState):
    legacy_am["ktMax"] = am_state.ktMax
    legacy_am["knMax"] = am_state.knMax
    legacy_am["kdMax"] = am_state.kdMax
    legacy_am["shapeLeft"] = am_state.shapeLeft
    legacy_am["shapeRight"] = am_state.shapeRight
    legacy_am["posLeft"] = am_state.posLeft
    legacy_am["posRight"] = am_state.posRight
    legacy_am["lBound"] = list(am_state.lBound)
    legacy_am["rBound"] = list(am_state.rBound)
    legacy_am["In"] = am_state.In
    legacy_am["Out"] = am_state.Out
    legacy_am["Active"] = am_state.Active
    legacy_am["Ignored"] = am_state.Ignored
    legacy_am["Total"] = am_state.Total
    legacy_am["Err_L"] = am_state.Err_L
    legacy_am["Err_R"] = am_state.Err_R
    legacy_am["activeLBound"] = list(am_state.activeLBound)
    legacy_am["activeRBound"] = list(am_state.activeRBound)
    legacy_am["xLB"] = list(am_state.xLB)
    legacy_am["yLB"] = list(am_state.yLB)
    legacy_am["xRB"] = list(am_state.xRB)
    legacy_am["yRB"] = list(am_state.yRB)


def apply_to_legacy_dict(state: AppState, data: dict):
    data["month"] = state.month
    data["year"] = state.year
    data["integration"] = state.integration
    data["plane"] = state.plane
    data["threshold"] = state.threshold
    data["xAxis"] = state.xAxis
    data["yAxis"] = state.yAxis

    if "lowAM" not in data:
        data["lowAM"] = {}
    if "medAM" not in data:
        data["medAM"] = {}
    if "highAM" not in data:
        data["highAM"] = {}

    _write_airmass(data["lowAM"], state.lowAM)
    _write_airmass(data["medAM"], state.medAM)
    _write_airmass(data["highAM"], state.highAM)
