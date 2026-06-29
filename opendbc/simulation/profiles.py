"""Real OpenDBC vehicle profiles for simulation telemetry."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SignalRef:
  message: str
  signal: str


@dataclass(frozen=True)
class VehicleProfile:
  id: str
  label: str
  dbc: str
  speed: SignalRef
  rpm: SignalRef | None = None
  steer: SignalRef | None = None
  brake: SignalRef | None = None
  gas: SignalRef | None = None
  gear: SignalRef | None = None


PROFILES: dict[str, VehicleProfile] = {
  "toyota_corolla_2020": VehicleProfile(
    id="toyota_corolla_2020",
    label="Toyota Corolla 2020",
    dbc="toyota_2017_ref_pt",
    speed=SignalRef("VSC1S03", "SP1"),
    rpm=SignalRef("BDB1S18_99", "ENGINE"),
    steer=SignalRef("STR1S01", "ASLP"),
  ),
  "mazda_3_2019": VehicleProfile(
    id="mazda_3_2019",
    label="Mazda 3 2019",
    dbc="mazda_3_2019",
    speed=SignalRef("WHEEL", "SPEED"),
    steer=SignalRef("STEER_RATE", "STEER_ANGLE"),
    rpm=SignalRef("ENGINE_DATA", "RPM"),
  ),
  "hyundai_kona_ev": VehicleProfile(
    id="hyundai_kona_ev",
    label="Hyundai Kona EV",
    dbc="hyundai_kia_generic",
    speed=SignalRef("CLU11", "CF_Clu_Vanz"),
    rpm=SignalRef("EMS_INFO", "RPM"),
  ),
  "tesla_model3": VehicleProfile(
    id="tesla_model3",
    label="Tesla Model 3",
    dbc="tesla_model3_vehicle",
    speed=SignalRef("DI_speed", "DI_vehicleSpeed"),
    steer=SignalRef("STW_ACTN_RQ", "SteeringAngle"),
  ),
  "ford_fusion": VehicleProfile(
    id="ford_fusion",
    label="Ford Fusion 2018",
    dbc="ford_fusion_2018_pt",
    speed=SignalRef("EngVehicleSpd_No2", "VehicleSpd"),
    steer=SignalRef("Steering_Wheel_Data1_FD1", "SteWhlAng_No2"),
  ),
}

DEFAULT_PROFILE_ID = "toyota_corolla_2020"
