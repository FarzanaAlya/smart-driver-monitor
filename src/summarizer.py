from .models import SensorSample, DetectionResult, EventSummary, DrivingState


def create_event_summary(sample: SensorSample, result: DetectionResult) -> EventSummary:
    """
    Creates a compact JSON-ready summary ONLY for unsafe events.
    """
    if result.driving_state != DrivingState.UNSAFE or result.severity is None:
        raise ValueError("Event summary can only be created for unsafe events with severity.")

    return EventSummary(
        event_type=result.event_type.value,
        severity_level=result.severity.value,
        speed_kmh=round(sample.speed_kmh, 2),
        latitude=round(sample.latitude, 6),
        longitude=round(sample.longitude, 6),
        timestamp=sample.timestamp_iso
    )


def create_normal_summary(sample: SensorSample) -> EventSummary:
    """
    Creates a summary for NORMAL (safe) driving.
    """
    return EventSummary(
        event_type="Normal",
        severity_level="Safe",
        speed_kmh=round(sample.speed_kmh, 2),
        latitude=round(sample.latitude, 6),
        longitude=round(sample.longitude, 6),
        timestamp=sample.timestamp_iso
    )
