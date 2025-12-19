import random
from datetime import datetime, timezone
from typing import Iterator

from .config import SimulationConfig, Thresholds
from .models import SensorSample, EventType


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def generate_sensor_stream(
    sim_cfg: SimulationConfig,
    thresholds: Thresholds
) -> Iterator[SensorSample]:
    """
    Generates an infinite stream of simulated sensor samples.

    This simulates accelerometer/gyroscope + GPS + speed.
    Occasionally injects unsafe behaviors for testing.
    """
    lat = sim_cfg.base_lat
    lon = sim_cfg.base_lon
    speed = sim_cfg.base_speed_kmh

    while True:
        # Baseline "normal driving" noise
        ax = random.uniform(-0.8, 0.8)
        ay = random.uniform(-0.8, 0.8)
        gz = random.uniform(-10.0, 10.0)

        # Slight random walk for speed/location
        speed = max(0.0, speed + random.uniform(-2.0, 2.0))
        lat += random.uniform(-0.0003, 0.0003)
        lon += random.uniform(-0.0003, 0.0003)

        # Randomly inject an unsafe event
        if random.random() < sim_cfg.unsafe_injection_prob:
            event_choice = random.choice([
                EventType.HARSH_BRAKING,
                EventType.RAPID_ACCELERATION,
                EventType.SHARP_TURN,
                EventType.OVERSPEEDING
            ])

            if event_choice == EventType.HARSH_BRAKING:
                ax = thresholds.harsh_braking_ax - random.uniform(0.5, 4.0)  # more negative
            elif event_choice == EventType.RAPID_ACCELERATION:
                ax = thresholds.rapid_accel_ax + random.uniform(0.5, 4.0)
            elif event_choice == EventType.SHARP_TURN:
                # Turn can show up in lateral accel and/or gyro
                ay = random.choice([-1, 1]) * (thresholds.sharp_turn_ay + random.uniform(0.5, 4.0))
                gz = random.choice([-1, 1]) * (thresholds.sharp_turn_gz + random.uniform(5.0, 60.0))
            elif event_choice == EventType.OVERSPEEDING:
                speed = thresholds.overspeed_kmh + random.uniform(5.0, 40.0)

        yield SensorSample(
            ax_ms2=ax,
            ay_ms2=ay,
            gz_dps=gz,
            speed_kmh=speed,
            latitude=lat,
            longitude=lon,
            timestamp_iso=_now_iso()
        )
