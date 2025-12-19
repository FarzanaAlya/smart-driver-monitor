from dataclasses import dataclass

@dataclass(frozen=True)
class Thresholds:
    """
    Threshold values for rule-based detection.

    NOTE: These values are reasonable starting points for simulation.
    You can tune them as part of your documentation/testing deliverables.
    """
    # Longitudinal acceleration (m/s^2)
    harsh_braking_ax: float = -3.5
    rapid_accel_ax: float = 3.0

    # Lateral acceleration (m/s^2) and/or gyro (deg/s)
    sharp_turn_ay: float = 3.0
    sharp_turn_gz: float = 35.0

    # Speed (km/h)
    overspeed_kmh: float = 90.0


@dataclass(frozen=True)
class SimulationConfig:
    """
    Controls the data generation loop and probability of unsafe events.
    """
    sample_interval_s: float = 1.0
    base_lat: float = 3.1390
    base_lon: float = 101.6869
    base_speed_kmh: float = 55.0

    # Probability of injecting an unsafe event into a sample
    unsafe_injection_prob: float = 0.20
