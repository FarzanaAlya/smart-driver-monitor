import time
from typing import Optional

from .config import SimulationConfig, Thresholds
from .simulator import generate_sensor_stream
from .edge_rules import detect_event
from .summarizer import create_event_summary, create_normal_summary
from .models import DrivingState
from .thingsboard_client import ThingsBoardClient, ThingsBoardConfig


def run_pipeline(
    tb_cfg: ThingsBoardConfig,
    sim_cfg: SimulationConfig = SimulationConfig(),
    thresholds: Thresholds = Thresholds(),
    max_samples: Optional[int] = None
) -> None:
    """
    Runs the full pipeline:
    SensorDataService -> BehaviorDetectionService -> SeverityEvaluationService
    -> EventSummaryService -> TelemetryUploadService

    Policy: ONLY unsafe events are transmitted to ThingsBoard.
    """
    tb = ThingsBoardClient(tb_cfg)
    stream = generate_sensor_stream(sim_cfg, thresholds)

    count = 0
    while True:
        sample = next(stream)
        result = detect_event(sample, thresholds)

        # Logging (local) for testing
        print(
            f"[{sample.timestamp_iso}] "
            f"ax={sample.ax_ms2:.2f} ay={sample.ay_ms2:.2f} gz={sample.gz_dps:.1f} "
            f"speed={sample.speed_kmh:.1f} -> {result.driving_state.value} ({result.event_type.value})"
        )

        if result.driving_state == DrivingState.UNSAFE:
            summary = create_event_summary(sample, result)
            ok, status, msg = tb.send_telemetry(summary.to_telemetry())
            print(f"  -> Upload: {ok} (status={status}) {msg}")
        else:
            summary = create_normal_summary(sample)
            ok, status, msg = tb.send_telemetry(summary.to_telemetry())
            print(f"  -> Upload NORMAL: {ok} (status={status}) {msg}")

        # Wait until next sampling time
        time.sleep(sim_cfg.sample_interval_s)

        count += 1
        if max_samples is not None and count >= max_samples:
            break
