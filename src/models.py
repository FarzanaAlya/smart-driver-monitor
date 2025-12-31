from dataclasses import dataclass
from enum import Enum
from typing import Optional, Dict, Any


class DrivingState(str, Enum):
    SAFE = "Safe"
    UNSAFE = "Unsafe"


class EventType(str, Enum):
    NORMAL_DRIVING = "None"
    HARSH_BRAKING = "HarshBraking"
    RAPID_ACCELERATION = "RapidAcceleration"
    SHARP_TURN = "SharpTurn"
    OVERSPEEDING = "Overspeeding"


class SeverityLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


@dataclass(frozen=True)
class SensorSample:
    """
    Raw sensor attributes (simulated).
    """
    ax_ms2: float
    ay_ms2: float
    gz_dps: float
    speed_kmh: float
    latitude: float
    longitude: float
    timestamp_iso: str  # ISO 8601 string


@dataclass(frozen=True)
class DetectionResult:
    """
    Output from BehaviorDetectionService + SeverityEvaluationService.
    """
    driving_state: DrivingState
    event_type: EventType
    severity: Optional[SeverityLevel] = None


@dataclass(frozen=True)
class EventSummary:
    """
    Output from EventSummaryService (JSON-ready object).
    """
    event_type: str
    severity_level: str
    speed_kmh: float
    latitude: float
    longitude: float
    timestamp: str

    def to_telemetry(self) -> Dict[str, Any]:
        """
        ThingsBoard telemetry payload format (key-value JSON).
        """
        return {
            "event_type": self.event_type,
            "severity_level": self.severity_level,
            "speed_kmh": self.speed_kmh,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timestamp": self.timestamp,
        }
