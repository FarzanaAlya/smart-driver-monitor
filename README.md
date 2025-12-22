## Code Overview (What each file does)

This project is organized to reflect the IoT pipeline:
**Simulated Perception → Edge Processing (Local) → Network (HTTP/JSON) → ThingsBoard Cloud → Dashboard**

---

### src/ (Core Edge Processing Logic)

* **src/main.py**

  * Primary entry point of the system.
  * Loads ThingsBoard configuration from a local `.env` file.
  * Starts the edge-processing pipeline by invoking the runner module.
  * When executed, performs continuous local sensor simulation, behavior detection, event summarization, and telemetry upload.

* **src/runner.py**

  * Manages the end-to-end edge-processing pipeline.
  * Connects all system components in sequence:

    > Sensor simulation
    > Edge-based behavior detection
    > Severity evaluation
    > Event summarization
    > Telemetry upload
  * Implements event-driven transmission:

    > Only unsafe driving events are uploaded to the cloud.
  * Controls sampling rate and execution flow for testing and demonstration.

* **src/simulator.py**

  * Generates a continuous stream of simulated sensor data.
  * Simulates:

    > Longitudinal and lateral acceleration
    > Gyroscope rotation
    > Vehicle speed
    > GPS latitude and longitude
  * Introduces unsafe driving events randomly based on a configurable probability.
  * Enables testing of detection logic without physical hardware.

* **src/edge_rules.py**

  * Implements rule-based unsafe driving detection logic at the edge.
  * Compares simulated sensor readings against predefined thresholds.
  * Detects unsafe behaviors such as:

    > Overspeeding
    > Harsh braking
    > Rapid acceleration
    > Sharp turns
  * Assigns severity levels (Low, Medium, High) based on threshold exceedance.
  * Outputs structured detection results for downstream processing.

* **src/summarizer.py**

  * Creates compact summaries for unsafe driving events only.
  * Converts raw sensor readings and detection results into a concise, JSON-ready EventSummary.
  * Filters out safe driving data to reduce unnecessary cloud transmission.

* **src/models.py**

  * Defines all core data models and enumerations used throughout the pipeline.
  * Includes:

    > SensorSample: represents one simulated sensor reading (motion, speed, GPS, timestamp).
    > DetectionResult: represents the output of edge-based behavior detection.
    > EventSummary: compact representation of an unsafe driving event.
  * Enumerations (DrivingState, EventType, SeverityLevel) ensure consistent labeling.
  * Provides a `to_telemetry()` method for ThingsBoard-compatible JSON output.

* **src/config.py**

  * Centralizes configuration and threshold parameters.
  * Thresholds define rule-based limits for unsafe driving behaviors (e.g., overspeeding, harsh braking).
  * SimulationConfig controls sampling interval, base GPS location, base speed, and unsafe event probability.
  * Allows easy tuning without modifying core logic.

* **src/thingsboard_client.py**

  * Handles all communication with ThingsBoard Cloud.
  * Constructs authenticated telemetry endpoints using device access tokens.
  * Sends telemetry data via HTTP POST with JSON payloads.
  * Includes retry and timeout handling for reliable transmission.
  * Keeps cloud communication logic separate from edge processing.

---

### Root files

* **requirements.txt**

  * Lists Python dependencies required to run the edge-processing pipeline.

* **.env.example**

  * Template for environment variables (ThingsBoard host and device token).
  * Users copy this file to `.env` locally.
  * Example:

    * `TB_HOST=https://thingsboard.cloud`
    * `TB_TOKEN=<your device access token>`

* **.gitignore**

  * Prevents sensitive and local files from being committed (e.g., `.env`, virtual environments).

---

> **Note:**
> The `.env` file is intentionally excluded from version control for security reasons.
> Each team member creates their own ThingsBoard device and access token.
> Edge processing is performed locally when `main.py` is executed, while ThingsBoard is used solely for cloud storage and visualization.






