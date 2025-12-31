from .config import Thresholds
from .models import SensorSample, DetectionResult, DrivingState, EventType, SeverityLevel


def detect_event(sample: SensorSample, t: Thresholds) -> DetectionResult:
    """
    Rule-based threshold detection.
    Priority is deterministic to avoid ambiguous classification.
    """
    # Overspeeding has clear meaning and should be detected even if other signals are noisy
    if sample.speed_kmh > t.overspeed_kmh:
        return DetectionResult(
            driving_state=DrivingState.UNSAFE,
            event_type=EventType.OVERSPEEDING,
            severity=_severity_overspeed(sample.speed_kmh, t.overspeed_kmh)
        )

    # Harsh braking / rapid acceleration based on longitudinal acceleration
    if sample.ax_ms2 <= t.harsh_braking_ax:
        return DetectionResult(
            driving_state=DrivingState.UNSAFE,
            event_type=EventType.HARSH_BRAKING,
            severity=_severity_by_exceedance(
                value=abs(sample.ax_ms2), threshold=abs(t.harsh_braking_ax)
            )
        )

    if sample.ax_ms2 >= t.rapid_accel_ax:
        return DetectionResult(
            driving_state=DrivingState.UNSAFE,
            event_type=EventType.RAPID_ACCELERATION,
            severity=_severity_by_exceedance(
                value=sample.ax_ms2, threshold=t.rapid_accel_ax
            )
        )

    # Sharp turn based on lateral accel OR gyro magnitude
    if abs(sample.ay_ms2) >= t.sharp_turn_ay or abs(sample.gz_dps) >= t.sharp_turn_gz:
        # Use the stronger indicator to assess severity
        exceed_ratio_ay = abs(sample.ay_ms2) / t.sharp_turn_ay
        exceed_ratio_gz = abs(sample.gz_dps) / t.sharp_turn_gz
        severity = _severity_from_ratio(max(exceed_ratio_ay, exceed_ratio_gz))
        return DetectionResult(
            driving_state=DrivingState.UNSAFE,
            event_type=EventType.SHARP_TURN,
            severity=severity
        )

    return DetectionResult(
        driving_state=DrivingState.SAFE,
        event_type=EventType.NORMAL_DRIVING,
        severity=None
    )


def _severity_by_exceedance(value: float, threshold: float) -> SeverityLevel:
    """
    Maps how far a reading exceeds a threshold to Low/Medium/High.
    """
    ratio = value / threshold if threshold != 0 else 0.0
    return _severity_from_ratio(ratio)


def _severity_overspeed(speed: float, limit: float) -> SeverityLevel:
    ratio = speed / limit if limit != 0 else 0.0
    # Overspeed severity should be a bit stricter
    if ratio >= 1.30:
        return SeverityLevel.HIGH
    if ratio >= 1.15:
        return SeverityLevel.MEDIUM
    return SeverityLevel.LOW


def _severity_from_ratio(ratio: float) -> SeverityLevel:
    if ratio >= 2.0:
        return SeverityLevel.HIGH
    if ratio >= 1.5:
        return SeverityLevel.MEDIUM
    return SeverityLevel.LOW
