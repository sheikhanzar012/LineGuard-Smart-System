# LineGuard Smart System — Test Cases & Sample Data

## 1. Purpose

This document defines the functional test cases, negative test cases, workflow validation, synchronization tests, API tests, event-log tests, sample data, end-to-end testing, and acceptance criteria for the LineGuard Smart System.

The purpose is to verify that the software prototype correctly enforces the intended maintenance workflow:

    REPAIRING ON
          ↓
    GRID AUTHORIZE ISOLATION
          ↓
    3/3 ISOLATORS OPEN
          ↓
    MAINTENANCE LOCK
          ↓
    REPAIRING TEST
          ↓
    GRID RESTORE POWER FOR TEST
          ↓
    SIMULATED TEST POWER ON
          ↓
    REPAIRING OFF / CLEAR
          ↓
    TEST POWER OFF + ISOLATORS OPEN
          ↓
    SAFETY CONFIRMATION
          ↓
    GRID AUTHORIZE RESTORATION
          ↓
    3/3 ISOLATORS CLOSED
          ↓
    SYSTEM RESTORED / IDLE

> **Safety Boundary:** LineGuard is currently a software-only prototype. The isolators and test power used in this document are simulations. The system does not control, isolate, energize, de-energize, or verify real electrical infrastructure.

---

## 2. Test Objectives

The testing process verifies that:

- Authentication works correctly.
- Work location is required.
- Maintenance requests are created correctly.
- Grid authorization is required for isolation.
- Three simulated isolation points are correctly controlled.
- 3/3 isolation is verified before maintenance lock.
- Restoration is blocked during maintenance.
- Repairing Test follows the correct workflow.
- Simulated test power follows the correct workflow.
- Clearance turns simulated test power OFF.
- Isolation is restored after clearance.
- Safety Confirmation is required.
- Final restoration requires Grid authorization.
- Lineman and Grid interfaces remain synchronized.
- Invalid workflow transitions are rejected.
- Events are recorded.
- Reset returns the system to its initial state.

---

# 3. Test Environment

| Component | Configuration |
|---|---|
| Backend | Python + Flask |
| Frontend | HTML5 + CSS3 + JavaScript |
| Grid Interface | `/grid` |
| Lineman Interface | `/lineman` |
| API | Flask REST-style API |
| Network | Local Wi-Fi |
| Browser | Modern desktop/mobile browser |
| Database | Not used in current prototype |
| Hardware | Not connected |
| Electrical Equipment | Not connected |
| Cloud | Not used in current prototype |

---

# 4. Sample User Accounts

| ID | Name | Password | Role |
|---|---|---|---|
| LIN001 | Aamir Khan | 1234 | Lineman |
| LIN002 | Rizwan Ahmad | 1234 | Lineman |
| LIN003 | Adil Ahmad | 1234 | Lineman |
| LIN004 | Sameer Hussain | 1234 | Lineman |
| LIN005 | Imran Dar | 1234 | Lineman |
| LIN006 | Danish Ahmad | 1234 | Lineman |
| LIN007 | Faisal Rashid | 1234 | Lineman |
| LIN008 | Suhail Ahmad | 1234 | Lineman |

These are demonstration credentials for the prototype.

---

# 5. Sample Work Location

Example test location:

    Transformer: Transformer-01
    Mohalla: Fatehgarh
    Landmark: Near Main Road

Sample JSON:

    {
      "transformer": "Transformer-01",
      "mohalla": "Fatehgarh",
      "landmark": "Near Main Road"
    }

---

# 6. Sample Maintenance Request

    {
      "request_id": "REQ-A1B2C3",
      "lineman_id": "LIN001",
      "transformer": "Transformer-01",
      "mohalla": "Fatehgarh",
      "landmark": "Near Main Road",
      "state": "REQUESTED"
    }

---

# 7. State Machine

The LineGuard workflow uses the following states:

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

---

# 8. State Definitions

| State | Meaning |
|---|---|
| `IDLE` | System ready for a new request |
| `REQUESTED` | Lineman submitted maintenance request |
| `ISOLATING` | Grid authorized simulated isolation |
| `MAINTENANCE_LOCKED` | Three simulated isolation points are open |
| `TEST_REQUESTED` | Lineman requested simulated test power |
| `TEST_POWER_ON` | Simulated test power is active |
| `CLEAR_PENDING` | Test power is OFF and clearance is pending |
| `SAFETY_CONFIRMED` | Lineman has confirmed safety |
| `RESTORING` | Grid has authorized final restoration |

---

# 9. Three-Point Isolation Model

The prototype contains three simulated isolation points:

    P1 = Isolator 1
    P2 = Isolator 2
    P3 = Isolator 3

Backend representation:

    true  = OPEN / simulated isolated
    false = CLOSED / simulated connected

Maintenance-isolated condition:

    {
      "isolators": [true, true, true]
    }

Normal closed condition:

    {
      "isolators": [false, false, false]
    }

The system should report:

    3/3 ISOLATORS OPEN VERIFIED

only when all three simulated isolators are OPEN.

---

# 10. Functional Test Cases

## TC001 — Valid Lineman Login

**Objective:** Verify that a valid Lineman can authenticate.

**Precondition:**

- Backend running.
- User is not logged in.

**Input:**

    ID: LIN001
    Password: 1234

**Expected Result:**

- Login succeeds.
- Lineman interface is displayed.
- Lineman identity becomes available to the workflow.

**Expected Status:** PASS

---

## TC002 — Invalid Login

**Objective:** Verify invalid credentials are rejected.

**Input:**

    ID: LIN001
    Password: WRONG

**Expected Result:**

- Login is rejected.
- User remains unauthenticated.
- Protected actions cannot be performed.

**Expected Status:** PASS

---

## TC003 — REPAIRING ON Without Login

**Precondition:**

- No Lineman authenticated.

**Action:**

    REPAIRING ON

**Expected Result:**

- Request rejected.
- State remains `IDLE`.

**Expected Status:** PASS

---

## TC004 — REPAIRING ON Without Work Location

**Precondition:**

- Lineman authenticated.
- Work location not entered.

**Action:**

    REPAIRING ON

**Expected Result:**

- Request rejected.
- State does not become `REQUESTED`.

**Expected Status:** PASS

---

## TC005 — Valid REPAIRING ON

**Precondition:**

- Lineman authenticated.
- Work location entered.
- State = `IDLE`.

**Action:**

    REPAIRING ON

**Expected Result:**

    IDLE
      ↓
    REQUESTED

A request ID is generated.

Example:

    REQ-A1B2C3

**Expected Status:** PASS

---

## TC006 — Grid Authorizes Isolation

**Precondition:**

    State = REQUESTED

**Action:**

    GRID AUTHORIZE ISOLATION

**Expected Result:**

    REQUESTED
        ↓
    ISOLATING

**Expected Status:** PASS

---

## TC007 — Three-Point Isolation

**Precondition:**

    State = ISOLATING

**Action:**

Grid authorizes simulated isolation.

**Expected Result:**

    P1 = OPEN
    P2 = OPEN
    P3 = OPEN

Grid displays:

    3/3 ISOLATORS OPEN VERIFIED

**Expected Status:** PASS

---

## TC008 — Maintenance Lock

**Precondition:**

    P1 = OPEN
    P2 = OPEN
    P3 = OPEN

**Expected Result:**

    State = MAINTENANCE_LOCKED

Restoration is blocked.

**Expected Status:** PASS

---

## TC009 — Repairing Test Before Maintenance Lock

**Precondition:**

    State != MAINTENANCE_LOCKED

**Action:**

    REPAIRING TEST

**Expected Result:**

- Action rejected.
- State does not become `TEST_REQUESTED`.

**Expected Status:** PASS

---

## TC010 — Valid Repairing Test

**Precondition:**

    State = MAINTENANCE_LOCKED

**Action:**

    REPAIRING TEST

**Expected Result:**

    MAINTENANCE_LOCKED
          ↓
    TEST_REQUESTED

**Expected Status:** PASS

---

## TC011 — Test Power Without Test Request

**Precondition:**

    State != TEST_REQUESTED

**Action:**

    GRID RESTORE POWER FOR TEST

**Expected Result:**

- Action rejected.
- Test power remains OFF.
- State does not become `TEST_POWER_ON`.

**Expected Status:** PASS

---

## TC012 — Valid Test Power Restoration

**Precondition:**

    State = TEST_REQUESTED

**Action:**

    GRID RESTORE POWER FOR TEST

**Expected Result:**

Simulated isolators become:

    P1 = CLOSED
    P2 = CLOSED
    P3 = CLOSED

Test power becomes:

    ON

State becomes:

    TEST_POWER_ON

**Expected Status:** PASS

---

## TC013 — Clear Before Test Power

**Precondition:**

    State != TEST_POWER_ON

**Action:**

    REPAIRING OFF / CLEAR

**Expected Result:**

- Action rejected.
- No premature clearance.
- State remains unchanged.

**Expected Status:** PASS

---

## TC014 — Valid Clearance

**Precondition:**

    State = TEST_POWER_ON

**Action:**

    REPAIRING OFF / CLEAR

**Expected Result:**

    Test Power = OFF

    P1 = OPEN
    P2 = OPEN
    P3 = OPEN

    State = CLEAR_PENDING

**Expected Status:** PASS

---

## TC015 — Safety Confirmation Before Clearance

**Precondition:**

    State != CLEAR_PENDING

**Action:**

    SAFETY CONFIRMATION

**Expected Result:**

- Action rejected.
- `safety_confirmed` remains false.

**Expected Status:** PASS

---

## TC016 — Valid Safety Confirmation

**Precondition:**

- State = `CLEAR_PENDING`.
- Test power = OFF.
- Repair test completed.

**Action:**

    SAFETY CONFIRMATION

**Expected Result:**

    State = SAFETY_CONFIRMED

    safety_confirmed = true

**Expected Status:** PASS

---

## TC017 — Restoration Before Safety Confirmation

**Precondition:**

    State != SAFETY_CONFIRMED

**Action:**

    GRID AUTHORIZE RESTORATION

**Expected Result:**

- Restoration rejected.
- System does not return to `IDLE`.

**Expected Status:** PASS

---

## TC018 — Valid Final Restoration

**Precondition:**

    State = SAFETY_CONFIRMED
    Test Power = OFF

**Action:**

    GRID AUTHORIZE RESTORATION

**Expected Result:**

    SAFETY_CONFIRMED
          ↓
       RESTORING
          ↓
       P1 CLOSED
       P2 CLOSED
       P3 CLOSED
          ↓
         IDLE

**Expected Status:** PASS

---

# 11. Restoration Protection Tests

## TC019 — Restoration During Maintenance Lock

**Precondition:**

    State = MAINTENANCE_LOCKED

**Action:**

    GRID AUTHORIZE RESTORATION

**Expected Result:**

- Restoration blocked.
- State remains `MAINTENANCE_LOCKED`.

**Expected Status:** PASS

---

## TC020 — Restoration During Test Request

**Precondition:**

    State = TEST_REQUESTED

**Action:**

    GRID AUTHORIZE RESTORATION

**Expected Result:**

- Restoration blocked.
- Test workflow must continue.

**Expected Status:** PASS

---

## TC021 — Restoration During Test Power

**Precondition:**

    State = TEST_POWER_ON

**Action:**

    GRID AUTHORIZE RESTORATION

**Expected Result:**

- Restoration blocked.
- Test power workflow remains active.

**Expected Status:** PASS

---

## TC022 — Restoration During Clearance

**Precondition:**

    State = CLEAR_PENDING

**Action:**

    GRID AUTHORIZE RESTORATION

**Expected Result:**

- Restoration blocked.
- Safety confirmation remains required.

**Expected Status:** PASS

---

## TC023 — Restoration After Safety Confirmation

**Precondition:**

    State = SAFETY_CONFIRMED
    Test Power = OFF

**Action:**

    GRID AUTHORIZE RESTORATION

**Expected Result:**

- Restoration authorized.
- P1 closes.
- P2 closes.
- P3 closes.
- State becomes `IDLE`.

**Expected Status:** PASS

---

# 12. Synchronization Tests

## TC024 — Lineman Request Appears on Grid

**Action:**

Lineman selects:

    REPAIRING ON

**Expected Result:**

Grid displays:

    REQUESTED

**Expected Status:** PASS

---

## TC025 — Isolation Status Synchronization

**Action:**

Grid authorizes isolation.

**Expected Result:**

Lineman interface reflects the updated workflow.

Grid displays:

    ISOLATING

followed by:

    MAINTENANCE_LOCKED

**Expected Status:** PASS

---

## TC026 — Three-Point Isolation Synchronization

**Action:**

Grid authorizes simulated isolation.

**Expected Result:**

Both interfaces reflect:

    P1 OPEN
    P2 OPEN
    P3 OPEN

and:

    3/3 ISOLATORS OPEN VERIFIED

**Expected Status:** PASS

---

## TC027 — Test Power Synchronization

**Action:**

Grid selects:

    GRID RESTORE POWER FOR TEST

**Expected Result:**

Both interfaces reflect:

    TEST_POWER_ON

**Expected Status:** PASS

---

## TC028 — Clearance Synchronization

**Action:**

Lineman selects:

    REPAIRING OFF / CLEAR

**Expected Result:**

Grid reflects:

    CLEAR_PENDING

and:

    TEST POWER OFF

and:

    P1 OPEN
    P2 OPEN
    P3 OPEN

**Expected Status:** PASS

---

## TC029 — Safety Confirmation Synchronization

**Action:**

Lineman selects:

    SAFETY CONFIRMATION

**Expected Result:**

Grid reflects:

    SAFETY_CONFIRMED

**Expected Status:** PASS

---

## TC030 — Final Restoration Synchronization

**Action:**

Grid selects:

    GRID AUTHORIZE RESTORATION

**Expected Result:**

Both interfaces reflect:

    RESTORING

and finally:

    IDLE

**Expected Status:** PASS

---

# 13. Event Log Tests

## TC031 — Login Event

**Action:**

Successful Lineman login.

**Expected Result:**

Login event is recorded.

**Expected Status:** PASS

---

## TC032 — Maintenance Request Event

**Action:**

    REPAIRING ON

**Expected Result:**

Maintenance request event is recorded.

**Expected Status:** PASS

---

## TC033 — Isolation Authorization Event

**Action:**

Grid authorizes isolation.

**Expected Result:**

Isolation authorization event is recorded.

**Expected Status:** PASS

---

## TC034 — Isolation Verification Event

**Action:**

All three simulated isolators become OPEN.

**Expected Result:**

Isolation verification event is recorded.

**Expected Status:** PASS

---

## TC035 — Maintenance Lock Event

**Action:**

System reaches:

    MAINTENANCE_LOCKED

**Expected Result:**

Maintenance-lock event is recorded.

**Expected Status:** PASS

---

## TC036 — Test Request Event

**Action:**

Lineman selects:

    REPAIRING TEST

**Expected Result:**

Test request event is recorded.

**Expected Status:** PASS

---

## TC037 — Test Power Event

**Action:**

Grid selects:

    GRID RESTORE POWER FOR TEST

**Expected Result:**

Test-power event is recorded.

**Expected Status:** PASS

---

## TC038 — Clearance Event

**Action:**

Lineman selects:

    REPAIRING OFF / CLEAR

**Expected Result:**

Events record:

- Test power OFF.
- Isolation reopened.
- Clearance submitted.

**Expected Status:** PASS

---

## TC039 — Safety Confirmation Event

**Action:**

Lineman selects:

    SAFETY CONFIRMATION

**Expected Result:**

Safety-confirmation event is recorded.

**Expected Status:** PASS

---

## TC040 — Restoration Event

**Action:**

Grid selects:

    GRID AUTHORIZE RESTORATION

**Expected Result:**

Restoration event is recorded.

**Expected Status:** PASS

---

# 14. Reset Test

## TC041 — Reset Demo

**Precondition:**

System may be in any workflow state.

**Action:**

    RESET DEMO

**Expected Result:**

    State = IDLE

    P1 = CLOSED
    P2 = CLOSED
    P3 = CLOSED

    Test Power = OFF

    Safety Confirmation = FALSE

    Repair Test = RESET

    Active Request = CLEARED

**Expected Status:** PASS

---

# 15. Three-Point Isolation Validation

The system should consider isolation verified only when:

    P1 = OPEN
    AND
    P2 = OPEN
    AND
    P3 = OPEN

Test matrix:

| P1 | P2 | P3 | Expected Result |
|---|---|---|---|
| OPEN | OPEN | OPEN | 3/3 VERIFIED |
| OPEN | OPEN | CLOSED | NOT VERIFIED |
| OPEN | CLOSED | OPEN | NOT VERIFIED |
| CLOSED | OPEN | OPEN | NOT VERIFIED |
| OPEN | CLOSED | CLOSED | NOT VERIFIED |
| CLOSED | OPEN | CLOSED | NOT VERIFIED |
| CLOSED | CLOSED | OPEN | NOT VERIFIED |
| CLOSED | CLOSED | CLOSED | NOT VERIFIED |

---

# 16. API Test Cases

## TC042 — GET Status

**Endpoint:**

    GET /api/status

**Expected Result:**

Returns:

- Current state.
- Isolator status.
- Lineman information.
- Request ID.
- Work location.
- Safety status.
- Test status.
- Event information.

**Expected Status:** PASS

---

## TC043 — Login API

**Endpoint:**

    POST /api/login

**Expected Result:**

Valid credentials authenticate successfully.

**Expected Status:** PASS

---

## TC044 — Logout API

**Endpoint:**

    POST /api/logout

**Expected Result:**

Current Lineman session is cleared.

**Expected Status:** PASS

---

## TC045 — Location API

**Endpoint:**

    POST /api/location

**Expected Result:**

Valid transformer, Mohalla, and landmark information is accepted.

**Expected Status:** PASS

---

## TC046 — Repair On API

**Endpoint:**

    POST /api/action/repair_on

**Expected Result:**

    IDLE → REQUESTED

**Expected Status:** PASS

---

## TC047 — Isolation Authorization API

**Endpoint:**

    POST /api/action/authorize_isolation

**Expected Result:**

    REQUESTED → ISOLATING → MAINTENANCE_LOCKED

**Expected Status:** PASS

---

## TC048 — Repair Test API

**Endpoint:**

    POST /api/action/repair_test

**Expected Result:**

    MAINTENANCE_LOCKED → TEST_REQUESTED

**Expected Status:** PASS

---

## TC049 — Test Power API

**Endpoint:**

    POST /api/action/test_power_restore

**Expected Result:**

    TEST_REQUESTED → TEST_POWER_ON

**Expected Status:** PASS

---

## TC050 — Clear API

**Endpoint:**

    POST /api/action/clear

**Expected Result:**

    TEST_POWER_ON → CLEAR_PENDING

and:

    test_power_on = false

    P1 = OPEN
    P2 = OPEN
    P3 = OPEN

**Expected Status:** PASS

---

## TC051 — Safety Confirmation API

**Endpoint:**

    POST /api/action/safety_confirm

**Expected Result:**

    CLEAR_PENDING → SAFETY_CONFIRMED

**Expected Status:** PASS

---

## TC052 — Restoration Authorization API

**Endpoint:**

    POST /api/action/authorize_restoration

**Expected Result:**

    SAFETY_CONFIRMED → RESTORING → IDLE

**Expected Status:** PASS

---

## TC053 — Restore API Protection

**Endpoint:**

    POST /api/action/restore

**Expected Result:**

The API must reject restoration when workflow conditions are not satisfied.

**Expected Status:** PASS

---

## TC054 — Reset API

**Endpoint:**

    POST /api/reset

**Expected Result:**

System returns to initial state.

**Expected Status:** PASS

---

# 17. Negative Workflow Tests

| Test ID | Invalid Action | Expected Result |
|---|---|---|
| NT001 | REPAIRING ON without login | Reject |
| NT002 | REPAIRING ON without location | Reject |
| NT003 | Isolation without request | Reject |
| NT004 | Repairing Test before isolation | Reject |
| NT005 | Test Power before test request | Reject |
| NT006 | Clear before test power | Reject |
| NT007 | Safety Confirmation before Clear | Reject |
| NT008 | Restoration before Safety Confirmation | Reject |
| NT009 | Restoration during maintenance | Reject |
| NT010 | Restoration during test | Reject |
| NT011 | Restoration during clearance | Reject |
| NT012 | Invalid login | Reject |

---

# 18. Sample State Data

## Initial State

    {
      "state": "IDLE",
      "isolators": [false, false, false],
      "test_power_on": false,
      "safety_confirmed": false,
      "repair_test_requested": false,
      "repair_test_passed": false
    }

## Requested State

    {
      "state": "REQUESTED",
      "isolators": [false, false, false],
      "test_power_on": false,
      "safety_confirmed": false,
      "repair_test_requested": false,
      "repair_test_passed": false
    }

## Isolating State

    {
      "state": "ISOLATING",
      "isolators": [true, true, true],
      "test_power_on": false,
      "safety_confirmed": false,
      "repair_test_requested": false,
      "repair_test_passed": false
    }

## Maintenance-Locked State

    {
      "state": "MAINTENANCE_LOCKED",
      "isolators": [true, true, true],
      "test_power_on": false,
      "safety_confirmed": false,
      "repair_test_requested": false,
      "repair_test_passed": false
    }

## Test-Requested State

    {
      "state": "TEST_REQUESTED",
      "isolators": [true, true, true],
      "test_power_on": false,
      "safety_confirmed": false,
      "repair_test_requested": true,
      "repair_test_passed": false
    }

## Test-Power State

    {
      "state": "TEST_POWER_ON",
      "isolators": [false, false, false],
      "test_power_on": true,
      "safety_confirmed": false,
      "repair_test_requested": true,
      "repair_test_passed": false
    }

## Clearance State

    {
      "state": "CLEAR_PENDING",
      "isolators": [true, true, true],
      "test_power_on": false,
      "safety_confirmed": false,
      "repair_test_requested": false,
      "repair_test_passed": true
    }

## Safety-Confirmed State

    {
      "state": "SAFETY_CONFIRMED",
      "isolators": [true, true, true],
      "test_power_on": false,
      "safety_confirmed": true,
      "repair_test_requested": false,
      "repair_test_passed": true
    }

## Final State

    {
      "state": "IDLE",
      "isolators": [false, false, false],
      "test_power_on": false,
      "safety_confirmed": false,
      "repair_test_requested": false,
      "repair_test_passed": false
    }

---

# 19. Sample Event Log

Example event sequence:

    1. System initialized
    2. Lineman LIN001 logged in
    3. Work location saved
    4. REPAIRING ON request received
    5. Request REQ-A1B2C3 created
    6. Grid authorized isolation
    7. Isolator 1 OPEN
    8. Isolator 2 OPEN
    9. Isolator 3 OPEN
    10. 3/3 isolation verified
    11. Maintenance lock activated
    12. Repairing test requested
    13. Grid authorized simulated test power
    14. Isolator 1 CLOSED for test
    15. Isolator 2 CLOSED for test
    16. Isolator 3 CLOSED for test
    17. Simulated test power ON
    18. REPAIRING OFF / CLEAR received
    19. Simulated test power OFF
    20. Isolator 1 OPEN
    21. Isolator 2 OPEN
    22. Isolator 3 OPEN
    23. Clearance pending
    24. Safety confirmation received
    25. Grid authorized final restoration
    26. Isolator 1 CLOSED
    27. Isolator 2 CLOSED
    28. Isolator 3 CLOSED
    29. System restored
    30. State returned to IDLE

---

# 20. Complete End-to-End Test

## Step 1 — Login

Lineman logs in:

    LIN001
    1234

Expected:

    LOGIN SUCCESS

---

## Step 2 — Work Location

Enter:

    Transformer: Transformer-01
    Mohalla: Fatehgarh
    Landmark: Near Main Road

Expected:

    LOCATION SAVED

---

## Step 3 — REPAIRING ON

Lineman selects:

    REPAIRING ON

Expected:

    IDLE → REQUESTED

---

## Step 4 — Grid Receives Request

Grid Control displays:

    ACTIVE REQUEST
    REQ-A1B2C3

Expected:

    REQUESTED

---

## Step 5 — Grid Authorizes Isolation

Grid selects:

    GRID AUTHORIZE ISOLATION

Expected:

    REQUESTED → ISOLATING

---

## Step 6 — Three-Point Isolation

System opens:

    P1
    P2
    P3

Expected:

    P1 = OPEN
    P2 = OPEN
    P3 = OPEN

---

## Step 7 — Isolation Verification

Expected:

    3/3 ISOLATORS OPEN VERIFIED

---

## Step 8 — Maintenance Lock

Expected:

    MAINTENANCE_LOCKED

Restoration must now be blocked.

---

## Step 9 — Repairing Test Request

Lineman selects:

    REPAIRING TEST

Expected:

    MAINTENANCE_LOCKED → TEST_REQUESTED

---

## Step 10 — Grid Authorizes Test Power

Grid selects:

    GRID RESTORE POWER FOR TEST

Expected:

    P1 = CLOSED
    P2 = CLOSED
    P3 = CLOSED

and:

    TEST POWER = ON

State:

    TEST_POWER_ON

---

## Step 11 — Simulated Test

The system remains in:

    TEST_POWER_ON

The test represents a controlled software demonstration only.

---

## Step 12 — Repairing OFF / CLEAR

Lineman selects:

    REPAIRING OFF / CLEAR

Expected:

    TEST POWER = OFF

and:

    P1 = OPEN
    P2 = OPEN
    P3 = OPEN

State:

    CLEAR_PENDING

---

## Step 13 — Safety Confirmation

Lineman selects:

    SAFETY CONFIRMATION

Expected:

    SAFETY_CONFIRMED

---

## Step 14 — Grid Authorizes Final Restoration

Grid selects:

    GRID AUTHORIZE RESTORATION

Expected:

    RESTORING

---

## Step 15 — Final Simulated Restoration

System closes:

    P1
    P2
    P3

Expected:

    P1 = CLOSED
    P2 = CLOSED
    P3 = CLOSED

---

## Step 16 — System Returns to Idle

Expected:

    STATE = IDLE

All workflow flags reset.

---

# 21. End-to-End Expected Result

    LOGIN
      ↓
    LOCATION
      ↓
    REPAIRING ON
      ↓
    REQUESTED
      ↓
    GRID AUTHORIZE ISOLATION
      ↓
    ISOLATING
      ↓
    3/3 OPEN
      ↓
    MAINTENANCE LOCK
      ↓
    REPAIRING TEST
      ↓
    TEST REQUESTED
      ↓
    GRID TEST POWER
      ↓
    TEST POWER ON
      ↓
    REPAIRING OFF / CLEAR
      ↓
    TEST POWER OFF
      ↓
    3/3 OPEN
      ↓
    CLEAR PENDING
      ↓
    SAFETY CONFIRMATION
      ↓
    SAFETY CONFIRMED
      ↓
    GRID AUTHORIZE RESTORATION
      ↓
    RESTORING
      ↓
    3/3 CLOSED
      ↓
    IDLE

Expected Overall Result:

    PASS

---

# 22. Acceptance Criteria

The LineGuard prototype passes functional acceptance when:

- Valid authentication works.
- Invalid authentication is rejected.
- Work location is required.
- REPAIRING ON creates a maintenance request.
- Grid authorization is required for isolation.
- Three simulated isolators open during isolation.
- 3/3 isolation is verified.
- Maintenance lock becomes active.
- Restoration is blocked during maintenance.
- REPAIRING TEST is available only in the correct state.
- Simulated test power is available only after the correct request.
- Test power becomes OFF during CLEAR.
- Three simulated isolators reopen after CLEAR.
- Safety confirmation is required before final restoration.
- Final restoration requires Grid authorization.
- Three simulated isolators close during final restoration.
- The system returns to IDLE.
- Events are recorded.
- Lineman and Grid interfaces synchronize.
- Reset returns the system to the initial state.

---

# 23. Final Test Summary

| Test Area | Result |
|---|---|
| Authentication | PASS |
| Work Location | PASS |
| Maintenance Request | PASS |
| Grid Authorization | PASS |
| Three-Point Isolation | PASS |
| Isolation Verification | PASS |
| Maintenance Lock | PASS |
| Repairing Test | PASS |
| Simulated Test Power | PASS |
| Clearance | PASS |
| Safety Confirmation | PASS |
| Restoration Protection | PASS |
| Final Restoration | PASS |
| Event Logging | PASS |
| Frontend Synchronization | PASS |
| API Workflow | PASS |
| Reset | PASS |

## Overall Prototype Test Result

    PASS

---

# 24. Safety Boundary

This document validates software behavior only.

The current LineGuard prototype does not:

- Control real electrical equipment.
- Disconnect real electrical lines.
- Energize real electrical lines.
- De-energize real electrical lines.
- Measure electrical voltage.
- Verify that a line is electrically dead.
- Perform physical earthing or grounding.
- Operate physical isolators.
- Replace utility protection systems.
- Replace qualified electrical personnel.
- Provide certified electrical safety.

All isolation points, switching operations, and test power described in this document are software simulations.

Any future physical deployment would require utility approval, qualified electrical engineering, appropriate protection systems, physical interlocking, isolation, testing, earthing/grounding, cybersecurity, fail-safe design, and compliance with applicable standards and regulations.

---

# 25. Document Information

**Project:** LineGuard Smart System

**File:** `docs/TEST_CASES.md`

**Document Type:** Test Cases, Test Data & Acceptance Criteria

**Purpose:** Software Prototype Validation

**Status:** Final

**Version:** 1.0
