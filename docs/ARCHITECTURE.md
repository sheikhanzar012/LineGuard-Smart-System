# LineGuard Smart System — System Architecture

## 1. Architecture Overview

LineGuard Smart System is designed as a two-layer solution:

1. Current Software Prototype — a working software demonstration using a Flask backend, responsive web interfaces, a state machine, event logging, and three simulated isolation points.
2. Intended Future IoT Architecture — an extension in which the software platform communicates through a secure cloud layer with a field microcontroller and approved isolation-control hardware.

The current prototype does not control physical electrical equipment.

## 2. Complete System Component Architecture

                         LINEGUARD SMART SYSTEM
                                  |
             +--------------------+--------------------+
             |                                         |
             v                                         v
     LINEMAN MOBILE APP                       GRID CONTROL DASHBOARD
             |                                         |
             +--------------------+--------------------+
                                  |
                                  v
                         COMMUNICATION / API
                                  |
                                  v
                         FLASK BACKEND
                            app.py
                                  |
        +-------------------------+-------------------------+
        |                         |                         |
        v                         v                         v
 AUTHENTICATION             WORKFLOW ENGINE            EVENT LOG
        |                         |
        |                         v
        |                    STATE MACHINE
        |                         |
        |              +----------+----------+
        |              |                     |
        v              v                     v
 WORK LOCATION    MAINTENANCE LOCK       RESTORATION
                           |
                           v
                  THREE-POINT ISOLATION
                    /       |       \
                   v        v        v
                  P1       P2       P3
               Isolator Isolator Isolator
                   1        2        3

## 3. Current Software Architecture

                 CURRENT SOFTWARE PROTOTYPE

        LINEMAN CLIENT             GRID CLIENT
        Mobile Browser            Laptop Browser
              |                         |
              +-----------+-------------+
                          |
                          v
                   FLASK BACKEND
                       app.py
                          |
              +-----------+-----------+
              |           |           |
              v           v           v
        Authentication  State      Event Log
                          |
                          v
                  Workflow Engine
                          |
                          v
                Simulated Isolators
                  /      |      \
                 v       v       v
                P1      P2      P3

### Current Components

| Component | Technology | Purpose |
|---|---|---|
| Lineman Interface | HTML/CSS/JavaScript | Field-side maintenance workflow |
| Grid Interface | HTML/CSS/JavaScript | Control-room workflow |
| Backend | Python + Flask | REST API and system logic |
| State Machine | Python | Controls valid workflow transitions |
| Authentication | Flask/Python | Demonstration user authentication |
| Work Location | Flask/Python | Stores transformer, mohalla and landmark |
| Maintenance Request | Flask/Python | Creates and tracks active requests |
| Maintenance Lock | State Machine | Blocks unauthorized restoration |
| Isolation Simulation | HTML/SVG/JavaScript | Displays three simulated isolators |
| Test Power | Software State | Simulates controlled test power |
| Safety Confirmation | State Machine | Required before final restoration |
| Event Log | Python | Records major workflow events |
| Reset | Flask API | Resets the demonstration state |

## 4. Lineman Mobile Interface

The lineman interacts with the system through a mobile browser.

                    LINEMAN MOBILE
                         |
             +-----------+-----------+
             |                       |
             v                       v
           LOGIN              WORK LOCATION
             |                       |
             +-----------+-----------+
                         |
                         v
                   REPAIRING ON
                         |
                         v
                MAINTENANCE REQUEST
                         |
                         v
              WAIT FOR GRID AUTHORIZATION
                         |
                         v
                  REPAIRING TEST
                         |
                         v
                 REPAIRING OFF
                     / CLEAR
                         |
                         v
                SAFETY CONFIRMATION

Lineman functions include:

- Login
- Select lineman identity
- Enter transformer/work location
- Enter mohalla/area
- Enter nearby landmark
- Submit REPAIRING ON request
- Request REPAIRING TEST
- Submit REPAIRING OFF / CLEAR
- Submit SAFETY CONFIRMATION
- Logout

## 5. Grid Control Dashboard

                    GRID CONTROL ROOM
                            |
            +---------------+---------------+
            |               |               |
            v               v               v
       ACTIVE REQUEST   ISOLATION       TEST POWER
            |               |               |
            +---------------+---------------+
                            |
                            v
                    RESTORATION CONTROL

Grid functions include:

- Review active maintenance request
- View lineman information
- View work location
- Authorize isolation
- View three simulated isolation points
- Monitor isolation status
- Restore power for simulated testing
- View system health
- View event log
- Authorize final restoration
- Reset demonstration

## 6. Backend Architecture

                      HTTP REQUEST
                           |
                           v
                    FLASK REST API
                           |
                           v
                    ACTION VALIDATOR
                           |
                           v
                     STATE MACHINE
                           |
                +----------+----------+
                |                     |
                v                     v
          UPDATE STATE           EVENT LOG
                |
                v
             RESPONSE

The backend validates every workflow action against the current state before allowing the transition.

## 7. Authentication Component

Lineman
   |
   v
Login Interface
   |
   v
Credential Validation
   |
   +------ INVALID ------> ACCESS DENIED
   |
  VALID
   |
   v
Authenticated Session

The current credentials are demonstration credentials only.

A production system would require:

- Secure password hashing
- Multi-factor authentication
- Role-based access control
- Session security
- Device identity
- Audit logging

## 8. Work Location Component

The lineman provides:

Transformer
Mohalla / Area
Nearby Landmark

             LINEMAN
                |
                v
          WORK LOCATION
                |
       +--------+--------+
       |        |        |
       v        v        v
 Transformer  Mohalla  Landmark
       |        |        |
       +--------+--------+
                |
                v
        Maintenance Request

Future versions may extend this with GPS and GIS integration.

## 9. Maintenance Request

The maintenance request begins when the lineman selects:

REPAIRING ON

The state changes:

IDLE
  |
  v
REQUESTED

A unique request ID is generated and made available to Grid Control.

Example:

REQ-A1B2C3

## 10. Complete Workflow State Machine

IDLE
  |
  | REPAIRING ON
  v
REQUESTED
  |
  | GRID AUTHORIZE ISOLATION
  v
ISOLATING
  |
  | 3/3 ISOLATORS OPEN VERIFIED
  v
MAINTENANCE_LOCKED
  |
  | REPAIRING TEST
  v
TEST_REQUESTED
  |
  | GRID RESTORE POWER FOR TEST
  v
TEST_POWER_ON
  |
  | REPAIRING OFF / CLEAR
  v
CLEAR_PENDING
  |
  | SAFETY CONFIRMATION
  v
SAFETY_CONFIRMED
  |
  | GRID AUTHORIZE RESTORATION
  v
RESTORING
  |
  v
IDLE

| State | Description |
|---|---|
| `IDLE` | No active maintenance operation |
| `REQUESTED` | Lineman submitted maintenance request |
| `ISOLATING` | Grid authorized simulated isolation |
| `MAINTENANCE_LOCKED` | Three isolation points are open and restoration is blocked |
| `TEST_REQUESTED` | Lineman requested test |
| `TEST_POWER_ON` | Simulated test power is active |
| `CLEAR_PENDING` | Test complete and awaiting safety confirmation |
| `SAFETY_CONFIRMED` | Safety confirmed by lineman |
| `RESTORING` | Grid is executing simulated restoration |

## 11. Maintenance Lock

                 ACTIVE MAINTENANCE
                         |
                         v
                  MAINTENANCE LOCK
                         |
              +----------+----------+
              |                     |
              v                     v
        TEST WORKFLOW         RESTORATION
                                   |
                                   v
                                BLOCKED

During active maintenance, unauthorized restoration is blocked.

## 12. Three-Point Isolation System

The prototype contains three simulated isolation points:

                    DISTRIBUTION LINE
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
        ISOLATOR 1    ISOLATOR 2    ISOLATOR 3
             |             |             |
             v             v             v
           POLE 1        POLE 2        POLE 3

### Isolation Points

P1 = Isolation Point 1
P2 = Isolation Point 2
P3 = Isolation Point 3

Each point has two software states:

OPEN   = simulated isolated condition
CLOSED = simulated connected condition

Backend representation:

True  = OPEN / ISOLATED
False = CLOSED / CONNECTED

Example:

{
  "isolators": [true, true, true]
}

means:

3 / 3 OPEN

The three isolation points are software/visual simulations only.

## 13. Isolation Verification

REQUESTED
     |
     v
ISOLATING
     |
     v
OPEN ISOLATOR 1
     |
     v
OPEN ISOLATOR 2
     |
     v
OPEN ISOLATOR 3
     |
     v
VERIFY 3 / 3 OPEN
     |
     v
MAINTENANCE_LOCKED

The system requires all three simulated isolation points to be open before entering the maintenance-locked condition.

## 14. Visual Isolation Layer

Closed:

CONTACT ---- BLADE ---- CONTACT
             |
         CONNECTED

Open:

CONTACT       GAP       CONTACT
       \               /
        \             /
          BLADE

        ISOLATED

The red warning indicator provides a visual indication during simulated isolation.

## 15. Repairing Test

MAINTENANCE_LOCKED
        |
        | REPAIRING TEST
        v
TEST_REQUESTED

The request becomes available to Grid Control.

## 16. Simulated Test Power

Grid Control selects:

RESTORE POWER FOR TEST

The simulated isolators transition:

[OPEN] [OPEN] [OPEN]
        |
        v
TEST AUTHORIZATION
        |
        v
[CLOSED] [CLOSED] [CLOSED]
        |
        v
SIMULATED TEST POWER ON

The backend sets:

test_power_on = True
state = TEST_POWER_ON

This is simulated test power only.

## 17. Clearance

The lineman selects:

REPAIRING OFF / CLEAR

The system performs:

SIMULATED TEST POWER
          |
          v
        OFF
          |
          v
ISOLATOR 1 → OPEN
ISOLATOR 2 → OPEN
ISOLATOR 3 → OPEN
          |
          v
   CLEAR_PENDING

This ensures that the simulated system returns to the isolated condition before final restoration.

## 18. Safety Confirmation

CLEAR_PENDING
      |
      v
SAFETY CONFIRMATION
      |
      v
SAFETY_CONFIRMED

The backend verifies that:

- The test is complete.
- Simulated test power is OFF.
- The system is in the correct workflow state.

Only then can Grid Control authorize final restoration.

## 19. Final Restoration

SAFETY_CONFIRMED
       |
       v
AUTHORIZE RESTORATION
       |
       v
RESTORING
       |
       v
[CLOSED] [CLOSED] [CLOSED]
       |
       v
SYSTEM RESTORED
       |
       v
IDLE

The restoration requires both:

LINEMAN
Safety Confirmation

+

GRID
Restoration Authorization

## 20. Event Logging

Major operations are recorded in the event log.

Examples:

System initialized
Lineman logged in
Work location saved
REPAIRING ON request received
Grid authorized isolation
Isolator 1 opened
Isolator 2 opened
Isolator 3 opened
3/3 isolation verified
Maintenance lock active
Repairing test requested
Simulated test power ON
Repairing OFF / CLEAR received
Simulated test power OFF
Three isolators reopened
Safety confirmation received
Grid authorized restoration
Three isolators closed
System restored

The current prototype uses in-memory logging. Future versions can use persistent audit storage.

## 21. API Architecture

                  FRONTEND
                     |
                     v
                REST API
                     |
                     v
                  FLASK
                     |
                     v
              STATE MACHINE

### Main Endpoints

GET  /api/status

POST /api/login
POST /api/logout
POST /api/location

POST /api/action/repair_on
POST /api/action/authorize_isolation
POST /api/action/repair_test
POST /api/action/test_power_restore
POST /api/action/clear
POST /api/action/safety_confirm
POST /api/action/authorize_restoration
POST /api/action/restore

POST /api/reset

## 22. Current Network Architecture

                 SAME WI-FI NETWORK
                         |
             +-----------+-----------+
             |                       |
             v                       v
          LAPTOP                   PHONE
             |                       |
       Flask Server            Lineman Browser
             |
             v
       Grid Browser

Example:

Grid:
http://127.0.0.1:5000/grid

Lineman:
http://192.168.1.8:5000/lineman

The current implementation is designed for demonstration over a local network.

## 23. Intended Cloud and IoT Architecture

The future LineGuard system extends the current software prototype with a secure cloud communication layer and field microcontroller.

                    LINEMAN MOBILE APP
                             |
                             | Maintenance Request
                             v
                       SECURE CLOUD
                             |
                    Secure API / Messaging
                             |
                             v
                     GRID CONTROL ROOM
                             |
                             | Authorized Command
                             v
                       SECURE CLOUD
                             |
                    Secure Internet / Cellular
                             |
                             v
                    FIELD MICROCONTROLLER
                             |
                    Command + Status Feedback
                             |
                             v
                APPROVED ISOLATION CONTROL SYSTEM
                       /       |       \
                      v        v        v
                 POINT 1   POINT 2   POINT 3

## 24. Future Cloud Communication Flow

LINEMAN
   |
   | Maintenance Request
   v
CLOUD PLATFORM
   |
   | Request / Status
   v
GRID CONTROL
   |
   | Authorized Command
   v
CLOUD PLATFORM
   |
   | Secure Device Command
   v
FIELD MICROCONTROLLER
   |
   | Isolation Control
   v
ISOLATION SYSTEM
   |
   | Position Feedback
   v
FIELD MICROCONTROLLER
   |
   | Status
   v
CLOUD PLATFORM
   |
   v
GRID CONTROL

The communication flow represents a bidirectional command and feedback loop.

Command Path:

LINEMAN
   |
   v
CLOUD PLATFORM
   |
   v
GRID CONTROL
   |
   v
CLOUD PLATFORM
   |
   v
FIELD MICROCONTROLLER
   |
   v
ISOLATION SYSTEM

Feedback Path:

ISOLATION SYSTEM
   |
   v
FIELD MICROCONTROLLER
   |
   v
CLOUD PLATFORM
   |
   v
GRID CONTROL

The current repository implements the software workflow locally. The cloud, field controller, and physical isolation components are intended future architecture.

## 25. Intended Microcontroller

A future implementation may use an appropriately selected ESP32-class microcontroller, subject to utility engineering and certification requirements.

Potential functions:

- Secure command reception
- Device authentication
- Isolation actuator interface
- Isolation-position feedback
- Local status indication
- Communication monitoring
- Fail-safe local behavior
- Status reporting

The microcontroller would operate as part of an approved protection and control architecture.

## 26. Future Physical Isolation Architecture

                     FIELD CONTROLLER
                            |
                            v
                     CONTROL INTERFACE
                            |
              +-------------+-------------+
              |             |             |
              v             v             v
         ISOLATION 1   ISOLATION 2   ISOLATION 3
              |             |             |
              +-------------+-------------+
                            |
                            v
                  APPROVED POWER SYSTEM

The exact actuator, protection device, sensing mechanism, communication hardware, and electrical interface would be determined by qualified engineers and the relevant utility.

## 27. Command and Feedback Architecture

### Command Path

GRID CONTROL
     |
     | Authorized Command
     v
CLOUD PLATFORM
     |
     | Secure Device Command
     v
FIELD MICROCONTROLLER
     |
     | Isolation Control
     v
ISOLATION SYSTEM

### Feedback Path

ISOLATION SYSTEM
     |
     | Position Feedback
     v
FIELD MICROCONTROLLER
     |
     | Status
     v
CLOUD PLATFORM
     |
     v
GRID CONTROL

## 28. Security Architecture

LINEMAN
   |
   | Authentication
   v
CLOUD
   |
   | Authorization
   v
GRID CONTROL
   |
   | Authenticated Command
   v
FIELD CONTROLLER
   |
   | Device Authentication
   v
ISOLATION SYSTEM

Potential controls:

- HTTPS/TLS
- Multi-factor authentication
- Role-based access control
- Device identity
- Certificates
- Secure API authentication
- Signed/authenticated commands
- Replay protection
- Persistent audit logging
- Network segmentation
- Secure firmware
- Secure device provisioning

## 29. Safety Architecture

             DIGITAL AUTHORIZATION
                      |
                      v
               CLOUD CONTROL
                      |
                      v
             FIELD CONTROLLER
                      |
                      v
              HARDWARE INTERLOCK
                      |
                      v
              PHYSICAL ISOLATION
                      |
                      v
             EARTHING / GROUNDING
                      |
                      v
             QUALIFIED PERSONNEL

LineGuard software is intended as a coordination and authorization layer, not as a replacement for physical electrical protection or qualified safety procedures.

## 30. Failure-Safe Architecture

COMMUNICATION FAILURE
        |
        v
SAFE LOCAL STATE
        |
        v
NO UNAUTHORIZED RESTORATION

The exact fail-safe behavior would be determined through electrical engineering, protection requirements, and utility standards.

## 31. Data Flow Architecture

LINEMAN
   |
   | Login / Location / Repair Request
   v
LINEMAN INTERFACE
   |
   v
FLASK API
   |
   +-------------------+
   |                   |
   v                   v
STATE MACHINE      EVENT LOG
   |
   +-------------------+
   |
   v
GRID CONTROL
   |
   | Authorization
   v
STATE MACHINE
   |
   v
ISOLATION STATUS
   |
   +---------+---------+
   |         |         |
   v         v         v
  P1        P2        P3
   |         |         |
   +---------+---------+
             |
             v
        SYSTEM STATUS
             |
             v
       LINEMAN / GRID

## 32. Complete Operational Sequence

1. Lineman logs into the system.
2. Lineman enters transformer, mohalla and nearby landmark.
3. Lineman selects REPAIRING ON.
4. System creates a maintenance request.
5. Grid Control receives the request.
6. Grid Control authorizes simulated isolation.
7. Isolator 1 opens.
8. Isolator 2 opens.
9. Isolator 3 opens.
10. System verifies 3/3 simulated isolation points.
11. Maintenance lock becomes active.
12. Lineman performs the required repair workflow.
13. Lineman selects REPAIRING TEST.
14. Grid Control receives the test request.
15. Grid Control selects RESTORE POWER FOR TEST.
16. All three simulated isolators close for the test simulation.
17. Simulated test power becomes ON.
18. Lineman completes the simulated test.
19. Lineman selects REPAIRING OFF / CLEAR.
20. Simulated test power turns OFF.
21. All three simulated isolators reopen.
22. System enters CLEAR_PENDING.
23. Lineman provides SAFETY CONFIRMATION.
24. System enters SAFETY_CONFIRMED.
25. Grid Control authorizes final restoration.
26. System enters RESTORING.
27. All three simulated isolators close.
28. System returns to IDLE.
29. The event log records the completed workflow.

## 33. Current Prototype vs Future System

| Component | Current Prototype | Intended Future System |
|---|---|---|
| Lineman Interface | Web/mobile browser | Secure mobile application |
| Grid Interface | Web dashboard | Secure control platform |
| Backend | Local Flask server | Cloud platform |
| Authentication | Demo authentication | Production identity/RBAC |
| Work Location | Transformer/Mohalla/Landmark | GPS/GIS-enabled |
| State Machine | Python | Cloud workflow service |
| Maintenance Lock | Software | Software + hardware interlock |
| Isolator 1 | Visual simulation | Approved physical isolation point |
| Isolator 2 | Visual simulation | Approved physical isolation point |
| Isolator 3 | Visual simulation | Approved physical isolation point |
| Test Power | Software simulation | Utility-approved controlled system |
| Microcontroller | Not implemented | ESP32-class/approved field controller |
| Cloud | Not implemented | Secure cloud platform |
| Feedback | Software state | Device/position feedback |
| Event Log | In-memory | Persistent audit log |
| Communication | Local HTTP | Secure cloud/API |
| Security | Prototype-level | Production-grade security |
| Physical Safety | Not implemented | Utility-approved protection/interlocking |
| GPS/GIS | Not implemented | Future GPS/GIS integration |
| Device Identity | Not implemented | Secure device identity |
| Hardware Feedback | Not implemented | Isolation-position feedback |

## 34. Deployment Evolution

### Phase 1 — Current Software Prototype

Web Browser
     |
     v
Flask Backend
     |
     v
State Machine
     |
     v
Simulated Three-Point Isolation

### Phase 2 — IoT Prototype

Mobile App
     |
     v
Cloud
     |
     v
Microcontroller
     |
     v
Low-Voltage Test Hardware

### Phase 3 — Utility-Engineered System

Mobile / Field Interface
          |
          v
Secure Cloud / Control Platform
          |
          v
Authenticated Field Controller
          |
          v
Approved Protection & Interlocking
          |
          v
Physical Isolation Equipment

Any real deployment would require utility approval, engineering validation, cybersecurity assessment, physical safety systems, and regulatory compliance.

## 35. Architectural Principle

Digital Authorization + Controlled State Transition + Verified Status + Physical Safety Controls

The current prototype demonstrates the digital workflow and state-management concepts.

The intended future architecture extends these concepts to a secure cloud-connected field controller and approved physical isolation system.

## 36. Limitations

The current LineGuard implementation is a software prototype.

It does not physically:

- Switch live electrical equipment.
- Isolate electrical lines.
- Measure electrical voltage.
- Verify de-energization.
- Perform physical earthing.
- Operate physical isolators.
- Replace SCADA systems.
- Replace protection systems.
- Replace utility control systems.
- Replace qualified electrical personnel.

The three isolation points and test power are simulated within the software interface.

The cloud platform, microcontroller, physical isolation hardware, GPS/GIS integration, hardware feedback and utility-grade protection systems are future development areas.

## 37. Safety Disclaimer

LineGuard is a software prototype intended to demonstrate a digital maintenance authorization and workflow concept.

The current system must not be used to control, isolate, energize, or de-energize real electrical infrastructure.

The software does not guarantee that an electrical line is dead or safe to touch.

Real electrical work requires utility-approved procedures, physical isolation, protection and interlocking systems, appropriate testing, earthing/grounding, qualified personnel, and applicable electrical safety standards.

The cloud, microcontroller, and physical isolation architecture described in this document represents the intended future architecture, not the physical capabilities of the current repository implementation.
