## Code Overview (What each file does)

This project is organized to reflect the IoT pipeline:
**Simulated Perception → Edge Processing → Network (HTTP/JSON) → ThingsBoard Cloud → Dashboard**.

### notebooks/
- **notebooks/edge_processing.ipynb**
  - Main demo notebook executed using Jupyter Notebook.
  - Loads ThingsBoard credentials from a local `.env` file.
  - Runs the full pipeline (sensor simulation → edge-based event detection → event summarization → telemetry upload).
  - Used for testing, demonstration and dashboard data generation.

### src/
- **src/thingsboard_client.py**
  - Handles all communication with ThingsBoard Cloud.
  - Builds the authenticated telemetry endpoint using the device access token.
  - Sends telemetry data using HTTP POST with JSON payloads.
  - Includes retry and timeout handling for reliable transmission.
  - Keeps cloud communication logic separate so the system is not tied to a specific IoT platform.

- **src/runner.py**
  - Manages the end-to-end pipeline flow.
  - Connects all system components in sequence:
    > Sensor simulation
    > Edge-based behavior detection
    > Severity evaluation
    > Event summarization
    > Telemetry upload
  - Implements event-driven transmission:
    > Only unsafe events are uploaded to the cloud.
  - Controls sampling rate and total execution length for testing and demonstration.

- **src/simulator.py**
  - Generates a continuous stream of simulated sensor data.
  - Simulates:
    > Longitudinal and lateral acceleration
    > Gyroscope rotation
    > Vehicle speed
    > GPS latitude and longitude
  - Introduces unsafe driving events randomly based on a configurable probability.
  - Allows testing of detection logic without physical hardware.

- **src/models.py** 
  - Defines all core data models and enumerations used in the pipeline.
  - Includes:
      > SensorSample: represents one simulated sensor reading (motion, speed, GPS, timestamp).
      > DetectionResult: represents the output of edge-based behavior detection.
      > EventSummary: a compact, JSON-ready representation of an unsafe driving event.
  - Enumerations (DrivingState, EventType, SeverityLevel) ensure consistent labeling across the system.
  - Provides a to_telemetry() method to convert event summaries into ThingsBoard-compatible JSON format.

- **src/config.py** 
  - Defines configuration and threshold values used throughout the system.
  - Thresholds: stores rule-based detection thresholds for unsafe driving behaviors (overspeeding, harsh braking).
  - SimulationConfig: controls simulation behavior such as sampling interval, base GPS location, base speed and probability of unsafe event injection.
  - Centralizes all tunable parameters so they can be adjusted without changing core logic.
 
- **src/edge_rules.py**
  - Implements rule-based unsafe driving detection logic.
  - Compares simulated sensor readings against predefined thresholds.
  - Detects unsafe behaviors such as:
    > Overspeeding
    > Harsh braking
    > Rapid acceleration
    > Sharp turns
  - Assigns severity levels (Low, Medium, High) based on how much a threshold is exceeded.
  - Returns a structured DetectionResult for downstream processing.

- **src/summarizer.py**
  - Creates a compact event summary for unsafe driving events only.
  - Converts raw sensor readings and detection results into a concise EventSummary.
  - Filters out safe driving data to reduce unnecessary cloud transmission.
  - Ensures that only meaningful, high-level event information is sent to ThingsBoard.

### Root files
- **requirements.txt**
  - Python dependencies required to run the notebook and pipeline.

- **.env.example**
  - Template for environment variables (host + token). Users copy this into `.env` locally.
  - Example:
    - `TB_HOST=https://thingsboard.cloud`
    - `TB_TOKEN=<your device access token>`

- **.gitignore**
  - Ensures sensitive/local files are not committed (e.g., `.env`, venv folders, notebook checkpoints).

> Note: The `.env` file is intentionally not committed for security. Each team member creates their own ThingsBoard device and token.
> The Jupyter Notebook is used for demonstration and testing, while the core logic is implemented in reusable Python modules under `src/`.

