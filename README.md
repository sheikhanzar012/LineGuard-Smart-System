# LineGuard Smart System

## Digital Maintenance Safety Interlock Prototype

LineGuard Smart System is a software-only prototype designed to demonstrate a controlled digital workflow for electrical line maintenance coordination between field personnel and a grid control room.

The system focuses on a simple principle:

    REQUEST
       ↓
    AUTHORIZE
       ↓
    ISOLATE
       ↓
    MAINTENANCE LOCK
       ↓
    TEST
       ↓
    CLEAR
       ↓
    SAFETY CONFIRMATION
       ↓
    RESTORE

> **Important Safety Notice:** LineGuard is currently a software prototype. It does not control, disconnect, energize, de-energize, or verify real electrical infrastructure. All isolators and test-power operations shown in the application are software simulations.

---

## 1. Problem

Electrical line maintenance requires reliable coordination between field personnel and grid control operations.

A maintenance activity can involve multiple steps and multiple people. A digital system can help structure these actions by ensuring that important workflow transitions occur in the correct sequence.

LineGuard demonstrates this concept through a state-based digital maintenance workflow.

---

## 2. Solution

LineGuard provides two interfaces:

### Lineman Interface

The Lineman can:

- Login.
- Enter work location.
- Submit `REPAIRING ON`.
- Request `REPAIRING TEST`.
- Submit `REPAIRING OFF / CLEAR`.
- Provide `SAFETY CONFIRMATION`.
- View current workflow status.

### Grid Control Interface

Grid Control can:

- View active maintenance requests.
- View Lineman information.
- View work location.
- Authorize simulated isolation.
- Monitor three simulated isolation points.
- View maintenance-lock status.
- Authorize simulated test power.
- Monitor test status.
- View safety confirmation.
- Authorize final simulated restoration.
- View event history.
- Reset the demonstration.

---

## 3. Core Workflow

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
      | 3/3 ISOLATORS CLOSED
      v
    IDLE

---

## 4. Three-Point Isolation

The prototype represents three simulated isolation points:

    P1 = Isolator 1
    P2 = Isolator 2
    P3 = Isolator 3

During simulated maintenance isolation:

    P1 = OPEN
    P2 = OPEN
    P3 = OPEN

The system verifies:

    3/3 ISOLATORS OPEN

before entering the maintenance-locked state.

After final simulated restoration:

    P1 = CLOSED
    P2 = CLOSED
    P3 = CLOSED

These are visual/software simulations only.

---

## 5. Maintenance Lock

Once the system reaches:

    MAINTENANCE_LOCKED

unauthorized restoration is blocked.

The system protects the maintenance workflow during:

    MAINTENANCE_LOCKED
    TEST_REQUESTED
    TEST_POWER_ON
    CLEAR_PENDING
    SAFETY_CONFIRMED

Restoration is permitted only after the required workflow and authorization conditions are satisfied.

---

## 6. Simulated Test Power

The prototype includes a controlled test-power workflow.

Sequence:

    MAINTENANCE_LOCKED
          ↓
    REPAIRING TEST
          ↓
    TEST_REQUESTED
          ↓
    GRID RESTORE POWER FOR TEST
          ↓
    TEST_POWER_ON

The simulated test temporarily changes the three simulated isolator states to represent test power.

After:

    REPAIRING OFF / CLEAR

the system:

    TEST POWER = OFF
    P1 = OPEN
    P2 = OPEN
    P3 = OPEN

and moves to:

    CLEAR_PENDING

---

## 7. Safety Confirmation

Final restoration cannot proceed directly after the test.

The workflow requires:

    TEST POWER OFF
          +
    CLEARANCE
          +
    SAFETY CONFIRMATION
          +
    GRID AUTHORIZATION

Only then can final simulated restoration occur.

---

## 8. Final Restoration

The final restoration workflow is:

    CLEAR_PENDING
          ↓
    SAFETY CONFIRMATION
          ↓
    SAFETY_CONFIRMED
          ↓
    GRID AUTHORIZE RESTORATION
          ↓
    RESTORING
          ↓
    P1 CLOSED
    P2 CLOSED
    P3 CLOSED
          ↓
    IDLE

---

## 9. Architecture

### Current Software Architecture

    LINEMAN MOBILE BROWSER
              |
              v
       FLASK REST BACKEND
              |
       +------+------+
       |             |
       v             v
    STATE MACHINE  EVENT LOG
       |
       v
    THREE-POINT
    SIMULATION
      / | \
     P1 P2 P3
              ^
              |
       GRID CONTROL
          BROWSER

The Flask backend acts as the shared source of truth for the workflow state.

---

## 10. Intended Future Architecture

The project is designed with a future cloud and IoT architecture in mind.

    LINEMAN MOBILE APP
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
         /    |    \
        P1    P2    P3
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

The cloud platform, field controller, physical isolation system, and physical feedback are future scope and are not part of the current implementation.

---

## 11. Technology Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5 |
| Styling | CSS3 |
| Client Logic | JavaScript |
| Backend | Python |
| Framework | Flask |
| API | REST-style HTTP API |
| Visualization | HTML/SVG/JavaScript |
| State Management | Python In-Memory State |
| Communication | Local HTTP |
| Version Control | Git/GitHub |
| License | MIT |

---

## 12. Project Structure

    LineGuard-Smart-System/
    │
    ├── backend/
    │   └── app.py
    │
    ├── frontend/
    │   └── index.html
    │
    ├── docs/
    │   ├── TECHNICAL_DESIGN.md
    │   └── TEST_CASES.md
    │
    ├── .gitignore
    ├── LICENSE
    └── README.md

---

## 13. Requirements

The current prototype requires:

- Python 3.x
- Flask
- A modern web browser
- Local Wi-Fi network for phone-to-laptop demonstration

Install the Python dependency using:

    pip install flask

---

## 14. Running the Backend

Open a terminal and navigate to:

    C:\line guard\LineGuard-Network-Demo\backend

Run:

    py app.py

The Flask server starts on:

    http://127.0.0.1:5000

For the local-network demonstration, the server can be accessed using the laptop's local IP address.

Example:

    http://192.168.1.8:5000

---

## 15. Opening the Interfaces

### Grid Control

On the laptop:

    http://127.0.0.1:5000/grid

### Lineman Interface

On a phone connected to the same Wi-Fi:

    http://192.168.1.8:5000/lineman

The IP address may be different on another network.

---

## 16. Demonstration Procedure

### Step 1 — Start Backend

Run:

    py app.py

Keep the terminal window running.

### Step 2 — Open Grid Control

Open:

    http://127.0.0.1:5000/grid

### Step 3 — Open Lineman Interface

From a phone connected to the same Wi-Fi, open:

    http://192.168.1.8:5000/lineman

### Step 4 — Login

Use a demonstration Lineman account.

Example:

    ID: LIN001
    Password: 1234

### Step 5 — Enter Work Location

Example:

    Transformer: Transformer-01
    Mohalla: Fatehgarh
    Landmark: Near Main Road

### Step 6 — Submit Maintenance Request

Select:

    REPAIRING ON

### Step 7 — Grid Authorization

From Grid Control select:

    GRID AUTHORIZE ISOLATION

### Step 8 — Verify Isolation

Confirm:

    P1 OPEN
    P2 OPEN
    P3 OPEN

and:

    3/3 ISOLATORS OPEN

### Step 9 — Maintenance Lock

The system should enter:

    MAINTENANCE_LOCKED

### Step 10 — Repairing Test

From the Lineman interface select:

    REPAIRING TEST

### Step 11 — Test Power

From Grid Control select:

    GRID RESTORE POWER FOR TEST

The system enters:

    TEST_POWER_ON

### Step 12 — Clear

After the simulated test, the Lineman selects:

    REPAIRING OFF / CLEAR

Expected:

    TEST POWER OFF
    P1 OPEN
    P2 OPEN
    P3 OPEN

### Step 13 — Safety Confirmation

The Lineman selects:

    SAFETY CONFIRMATION

Expected:

    SAFETY_CONFIRMED

### Step 14 — Final Restoration

Grid Control selects:

    GRID AUTHORIZE RESTORATION

Expected:

    P1 CLOSED
    P2 CLOSED
    P3 CLOSED

and finally:

    IDLE

---

## 17. Demonstration Login Accounts

| ID | Name | Password |
|---|---|---|
| LIN001 | Aamir Khan | 1234 |
| LIN002 | Rizwan Ahmad | 1234 |
| LIN003 | Adil Ahmad | 1234 |
| LIN004 | Sameer Hussain | 1234 |
| LIN005 | Imran Dar | 1234 |
| LIN006 | Danish Ahmad | 1234 |
| LIN007 | Faisal Rashid | 1234 |
| LIN008 | Suhail Ahmad | 1234 |

These accounts are for demonstration purposes.

---

## 18. API Endpoints

The prototype provides the following API routes:

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

---

## 19. Testing

Detailed test cases are available in:

    docs/TEST_CASES.md

The test suite covers:

- Authentication.
- Work location.
- Maintenance request.
- Isolation.
- Maintenance lock.
- Repairing test.
- Simulated test power.
- Clearance.
- Safety confirmation.
- Restoration.
- Invalid workflow transitions.
- API behavior.
- Event logging.
- Synchronization.
- Reset.
- End-to-end workflow.

The complete technical architecture is documented in:

    docs/TECHNICAL_DESIGN.md

---

## 20. Example End-to-End Test

The expected successful workflow is:

    LOGIN
      ↓
    WORK LOCATION
      ↓
    REPAIRING ON
      ↓
    REQUESTED
      ↓
    GRID AUTHORIZE ISOLATION
      ↓
    ISOLATING
      ↓
    P1 + P2 + P3 OPEN
      ↓
    MAINTENANCE_LOCKED
      ↓
    REPAIRING TEST
      ↓
    TEST_REQUESTED
      ↓
    GRID RESTORE POWER FOR TEST
      ↓
    TEST_POWER_ON
      ↓
    REPAIRING OFF / CLEAR
      ↓
    TEST POWER OFF
      ↓
    P1 + P2 + P3 OPEN
      ↓
    CLEAR_PENDING
      ↓
    SAFETY CONFIRMATION
      ↓
    SAFETY_CONFIRMED
      ↓
    GRID AUTHORIZE RESTORATION
      ↓
    RESTORING
      ↓
    P1 + P2 + P3 CLOSED
      ↓
    IDLE

---

## 21. Key Safety Concept

The core software concept is a two-party digital workflow:

    FIELD PERSONNEL
          |
          | Maintenance Request
          v
    GRID CONTROL
          |
          | Isolation Authorization
          v
    MAINTENANCE LOCK
          |
          | Repair / Test
          v
    FIELD CLEARANCE
          |
          | Safety Confirmation
          v
    GRID CONTROL
          |
          | Restoration Authorization
          v
    SYSTEM RESTORED

The prototype demonstrates how software can enforce the sequence of actions rather than allowing unrestricted state changes.

---

## 22. Innovation

LineGuard combines:

- Digital maintenance requests.
- Lineman-to-grid coordination.
- State-based workflow control.
- Three-point isolation simulation.
- Maintenance lock.
- Controlled test-power simulation.
- Clearance workflow.
- Safety confirmation.
- Authorized restoration.
- Event logging.
- Mobile and desktop interfaces.
- Future IoT/cloud extensibility.

The project is designed around a simple principle:

    NO DIRECT RESTORATION
    DURING ACTIVE MAINTENANCE

---

## 23. Social Impact

The intended social impact is to explore how digital technology can improve coordination and workflow discipline in electrical maintenance operations.

Potential future benefits include:

- Better field-control-room coordination.
- More structured maintenance workflows.
- Reduced dependence on informal communication.
- Improved visibility of maintenance status.
- Better auditability.
- Reduced possibility of incorrect software workflow transitions.
- Foundation for future IoT-enabled safety systems.

These are intended benefits of the proposed concept and should not be interpreted as proof of real-world electrical safety.

---

## 24. Future Scope

### Cloud Integration

- Secure cloud backend.
- Persistent database.
- Real-time communication.
- Centralized monitoring.
- Audit storage.

### Mobile Application

- Native Android/iOS application.
- Secure authentication.
- GPS.
- Offline workflow support.
- Push notifications.

### IoT

- ESP32-class field controller.
- Device authentication.
- Secure command channel.
- Isolation-position feedback.
- Device health monitoring.

### GIS

- Live field location.
- Transformer mapping.
- Pole mapping.
- Feeder information.
- Maintenance history.

### Security

- MFA.
- RBAC.
- HTTPS/TLS.
- Device certificates.
- Signed commands.
- Replay protection.
- Secure firmware.
- Network segmentation.

### Physical Safety Engineering

Any physical deployment would require:

- Utility approval.
- Qualified electrical engineering.
- Approved isolation equipment.
- Hardware interlocking.
- Protection systems.
- Earthing/grounding.
- Electrical testing.
- Fail-safe design.
- Cybersecurity validation.
- Regulatory and standards compliance.

---

## 25. Limitations

The current prototype:

- Does not control real electrical infrastructure.
- Does not disconnect real power lines.
- Does not energize real power lines.
- Does not measure voltage.
- Does not verify de-energization.
- Does not perform physical earthing.
- Does not operate physical isolators.
- Does not provide utility-grade SCADA.
- Does not use production cloud infrastructure.
- Does not use a production database.
- Does not implement production-grade authentication.
- Does not provide certified electrical protection.
- Does not provide physical interlocking.
- Does not provide real GPS/GIS tracking.
- Does not receive physical isolation feedback.

---

## 26. Repository Documentation

| File | Purpose |
|---|---|
| `README.md` | Project overview and setup |
| `backend/app.py` | Flask backend and workflow logic |
| `frontend/index.html` | Lineman and Grid interfaces |
| `docs/TECHNICAL_DESIGN.md` | Architecture and technical design |
| `docs/TEST_CASES.md` | Test cases and sample data |
| `.gitignore` | Git ignored files |
| `LICENSE` | MIT License |

---

## 27. Safety Disclaimer

> **LineGuard is a software prototype intended to demonstrate a digital maintenance authorization and workflow concept.**
>
> The current system must not be used to control, isolate, energize, de-energize, or verify real electrical infrastructure.
>
> The software does not guarantee that an electrical line is dead or safe to touch.
>
> The three isolation points and test power are software simulations.
>
> Real electrical work requires utility-approved procedures, physical isolation, appropriate testing, protection and interlocking systems, earthing/grounding, qualified personnel, and applicable electrical safety standards.

---

## 28. AI Assistance Disclosure

AI-based tools were used during the development process for activities including:

- Brainstorming and refinement of the project concept.
- Software development assistance.
- Debugging assistance.
- Documentation drafting.
- Technical design refinement.
- Test-case generation.
- README and repository documentation preparation.

The project implementation, integration, testing, workflow decisions, and final submission remain under the control and review of the project team.

**Estimated proportion of final work involving AI assistance:** `[ENTER HONEST PERCENTAGE]`

> The percentage should be completed by the project team based on the actual extent of AI assistance used during development.

---

## 29. Project Status

**Current Version:** Software Prototype

**Current Deployment:** Local Network Demonstration

**Backend:** Flask/Python

**Frontend:** HTML/CSS/JavaScript

**Physical Hardware:** Not connected

**Electrical Infrastructure:** Not connected

**Future Direction:** Cloud + IoT + Secure Field-Control Architecture

---

## 30. License

This project is released under the MIT License.

See:

    LICENSE

for the complete license text.

---

## 31. Final Project Statement

LineGuard Smart System demonstrates how a structured digital workflow can coordinate field maintenance requests, simulated isolation, maintenance locking, testing, clearance, safety confirmation, and restoration authorization.

The current implementation is intentionally software-only and serves as a proof-of-concept for a future architecture that could combine secure cloud services, field controllers, position feedback, GIS, and utility-approved physical safety systems.

The central concept is:

    REQUEST
       ↓
    VERIFY
       ↓
    ISOLATE
       ↓
    LOCK
       ↓
    TEST
       ↓
    CLEAR
       ↓
    CONFIRM
       ↓
    AUTHORIZE
       ↓
    RESTORE

---

## 32. Project Repository

**Repository:**

    https://github.com/sheikhanzar012/LineGuard-Smart-System

**Main Branch:**

    main

**Project Structure:**

    LineGuard-Smart-System/
    ├── backend/
    │   └── app.py
    ├── frontend/
    │   └── index.html
    ├── docs/
    │   ├── TECHNICAL_DESIGN.md
    │   └── TEST_CASES.md
    ├── .gitignore
    ├── LICENSE
    └── README.md

---

## 33. Document Status

**Project:** LineGuard Smart System

**Document:** README.md

**Version:** 1.0

**Status:** Submission-Ready Draft
