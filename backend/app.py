from flask import Flask, jsonify, request, send_from_directory
from datetime import datetime
import uuid

app = Flask(__name__, static_folder="../frontend")


# ============================================================
# SYSTEM STATE
# ============================================================

STATE = {
    "state": "IDLE",
    "isolators": [False, False, False],
    "lineman": None,
    "events": [
        "System initialized in IDLE"
    ],
    "request_id": None,
    "work_location": None,
    "safety_confirmed": False,
    "repair_test_requested": False,
    "test_power_on": False,
    "repair_test_passed": False
}


# ============================================================
# REGISTERED LINEMEN
# ============================================================

USERS = {

    "LIN001": {
        "password": "1234",
        "name": "Aamir Khan",
        "location": "Fatehgarh, Baramulla",
        "contact": "+91 98765 43210"
    },

    "LIN002": {
        "password": "1234",
        "name": "Rizwan Ahmad",
        "location": "Jamia, Baramulla",
        "contact": "+91 98765 12345"
    },

    "LIN003": {
        "password": "1234",
        "name": "Adil Ahmad",
        "location": "Delina, Baramulla",
        "contact": "+91 97970 11223"
    },

    "LIN004": {
        "password": "1234",
        "name": "Sameer Hussain",
        "location": "Sopore, Baramulla",
        "contact": "+91 98580 44556"
    },

    "LIN005": {
        "password": "1234",
        "name": "Imran Dar",
        "location": "Kanispora, Baramulla",
        "contact": "+91 99060 77889"
    },

    "LIN006": {
        "password": "1234",
        "name": "Danish Ahmad",
        "location": "Pattan, Baramulla",
        "contact": "+91 98123 45678"
    },

    "LIN007": {
        "password": "1234",
        "name": "Faisal Rashid",
        "location": "Kunzer, Baramulla",
        "contact": "+91 97654 32109"
    },

    "LIN008": {
        "password": "1234",
        "name": "Suhail Ahmad",
        "location": "Tangmarg, Baramulla",
        "contact": "+91 98987 65432"
    }

}

# ============================================================
# EVENT LOG
# ============================================================

def log(message):

    timestamp = datetime.now().strftime("%H:%M:%S")

    STATE["events"].insert(
        0,
        f"{timestamp} — {message}"
    )

    STATE["events"] = STATE["events"][:25]


# ============================================================
# SNAPSHOT
# ============================================================

def snapshot():

    return {
        "state": STATE["state"],
        "isolators": STATE["isolators"],
        "lineman": STATE["lineman"],
        "events": STATE["events"],
        "request_id": STATE["request_id"],
        "work_location": STATE["work_location"],
        "safety_confirmed": STATE["safety_confirmed"],
        "repair_test_requested": STATE["repair_test_requested"],
        "test_power_on": STATE["test_power_on"],
        "repair_test_passed": STATE["repair_test_passed"]
    }


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return send_from_directory(
        app.static_folder,
        "index.html"
    )


# ============================================================
# LINEMAN PANEL
# ============================================================

@app.get("/lineman")
def lineman():

    return send_from_directory(
        app.static_folder,
        "index.html"
    )


# ============================================================
# GRID CONTROL ROOM
# ============================================================

@app.get("/grid")
def grid():

    return send_from_directory(
        app.static_folder,
        "index.html"
    )


# ============================================================
# SYSTEM STATUS
# ============================================================

@app.get("/api/status")
def status():

    return jsonify(
        snapshot()
    )


# ============================================================
# LINEMAN LOGIN
# ============================================================

@app.post("/api/login")
def login():

    data = request.get_json(silent=True) or {}

    user_id = str(
        data.get("user_id", "")
    ).strip().upper()

    password = str(
        data.get("password", "")
    ).strip()

    # Explicit credentials for every registered lineman
    credentials = {
        "LIN001": "1234",
        "LIN002": "1234",
        "LIN003": "1234",
        "LIN004": "1234",
        "LIN005": "1234",
        "LIN006": "1234",
        "LIN007": "1234",
        "LIN008": "1234"
    }

    if user_id not in credentials:
        return jsonify({
            "ok": False,
            "message": "Invalid User ID.",
            **snapshot()
        }), 401

    if password != credentials[user_id]:
        return jsonify({
            "ok": False,
            "message": "Invalid password.",
            **snapshot()
        }), 401

    # Prevent another login during an active maintenance cycle
    if STATE["state"] != "IDLE":
        return jsonify({
            "ok": False,
            "message": "A maintenance session is already active.",
            **snapshot()
        }), 409

    user = USERS[user_id]

    STATE["lineman"] = {
        "user_id": user_id,
        "name": user["name"],
        "location": user["location"],
        "contact": user["contact"]
    }

    log(
        f"Lineman login: "
        f"{user['name']} ({user_id})"
    )

    return jsonify({
        "ok": True,
        "message": f"Welcome {user['name']}. Login successful.",
        **snapshot()
    })






# ============================================================
# LINEMAN LOGOUT
# ============================================================

@app.post("/api/logout")
def logout():

    if STATE["lineman"]:

        log(
            f"Lineman logout: "
            f"{STATE['lineman']['name']}"
        )


    STATE["lineman"] = None

    STATE["work_location"] = None
    STATE["safety_confirmed"] = False
    STATE["repair_test_requested"] = False
    STATE["test_power_on"] = False
    STATE["repair_test_passed"] = False


    return jsonify({

        "ok": True,

        "message": "Lineman logged out.",

        **snapshot()

    })


# ============================================================
# WORK LOCATION
# ============================================================

@app.post("/api/location")
def set_location():

    if not STATE["lineman"]:

        return jsonify({

            "ok": False,

            "message":
                "Lineman login required.",

            **snapshot()

        }), 401


    data = request.get_json() or {}


    transformer = str(
        data.get(
            "transformer",
            ""
        )
    ).strip()


    mohalla = str(
        data.get(
            "mohalla",
            ""
        )
    ).strip()


    landmark = str(
        data.get(
            "landmark",
            ""
        )
    ).strip()


    if not transformer:

        return jsonify({

            "ok": False,

            "message":
                "Transformer ID is required.",

            **snapshot()

        }), 400


    if not mohalla:

        return jsonify({

            "ok": False,

            "message":
                "Mohalla / area is required.",

            **snapshot()

        }), 400


    if not landmark:

        return jsonify({

            "ok": False,

            "message":
                "Nearby landmark is required.",

            **snapshot()

        }), 400


    STATE["work_location"] = {

        "transformer": transformer,

        "mohalla": mohalla,

        "landmark": landmark

    }


    log(
        f"Work location selected: "
        f"{transformer} — {mohalla}"
    )


    return jsonify({

        "ok": True,

        "message":
            "Work location saved successfully.",

        **snapshot()

    })


# ============================================================
# MAIN ACTIONS
# ============================================================

@app.post("/api/action/<action>")
def action(action):


    # ========================================================
    # REPAIRING ON
    # ========================================================

    if action == "repair_on":

        if not STATE["lineman"]:

            return jsonify({

                "ok": False,

                "message":
                    "Lineman must login first.",

                **snapshot()

            }), 400


        if not STATE["work_location"]:

            return jsonify({

                "ok": False,

                "message":
                    "Select transformer, Mohalla and nearby "
                    "landmark first.",

                **snapshot()

            }), 400


        if STATE["state"] != "IDLE":

            return jsonify({

                "ok": False,

                "message":
                    "System is not ready for a new request.",

                **snapshot()

            }), 400


        STATE["state"] = "REQUESTED"


        STATE["request_id"] = (

            "REQ-"

            + uuid.uuid4().hex[:6].upper()

        )


        log(
            f"REPAIRING ON request "
            f"{STATE['request_id']} "
            f"from {STATE['lineman']['name']}"
        )


        return jsonify({

            "ok": True,

            "message":
                "Repair request sent to Grid Control Room.",

            **snapshot()

        })


    # ========================================================
    # AUTHORIZE ISOLATION
    # ========================================================

    if action == "authorize_isolation":

        if STATE["state"] != "REQUESTED":

            return jsonify({

                "ok": False,

                "message":
                    "No pending repair request.",

                **snapshot()

            }), 400


        STATE["state"] = "ISOLATING"


        log(
            "Grid authorized isolation."
        )


        # Simulated three-point isolation

        STATE["isolators"] = [

            True,
            True,
            True

        ]


        log(
            "Isolator 1 OPEN"
        )

        log(
            "Isolator 2 OPEN"
        )

        log(
            "Isolator 3 OPEN"
        )


        # Verify all three

        if all(
            STATE["isolators"]
        ):

            STATE["state"] = (
                "MAINTENANCE_LOCKED"
            )


            log(
                "All three isolation points verified OPEN."
            )


            log(
                "MAINTENANCE LOCK ACTIVE."
            )


            return jsonify({

                "ok": True,

                "message":
                    "Isolation verified. "
                    "Maintenance lock active.",

                **snapshot()

            })


    # ========================================================
    # TRY RESTORE
    # ========================================================

    if action == "restore":

        if STATE["state"] in [
            "REQUESTED",
            "ISOLATING",
            "MAINTENANCE_LOCKED",
            "TEST_REQUESTED",
            "TEST_POWER_ON",
            "CLEAR_PENDING",
            "SAFETY_CONFIRMED"
        ]:

            log(
                "RESTORE attempt BLOCKED: "
                "maintenance session active."
            )


            return jsonify({

                "ok": False,

                "message":
                    "RESTORATION BLOCKED — "
                    "maintenance active.",

                **snapshot()

            })


        return jsonify({

            "ok": False,

            "message":
                "Restoration is not available.",

            **snapshot()

        })


    # ========================================================
    # REPAIRING TEST REQUEST
    # ========================================================

    if action == "repair_test":

        if not STATE["lineman"]:
            return jsonify({
                "ok": False,
                "message": "Lineman must login first.",
                **snapshot()
            }), 400

        if STATE["state"] != "MAINTENANCE_LOCKED":
            return jsonify({
                "ok": False,
                "message": "Repairing Test is available only while the maintenance lock is active.",
                **snapshot()
            }), 400

        STATE["repair_test_requested"] = True
        STATE["test_power_on"] = False
        STATE["repair_test_passed"] = False
        STATE["state"] = "TEST_REQUESTED"

        log(
            f"REPAIRING TEST requested by {STATE['lineman']['name']}. Awaiting Grid test-power authorization."
        )

        return jsonify({
            "ok": True,
            "message": "Repairing Test request sent to Grid Control Room.",
            **snapshot()
        })


    # ========================================================
    # GRID RESTORE POWER FOR TEST
    # ========================================================

    if action == "test_power_restore":

        if STATE["state"] != "TEST_REQUESTED" or not STATE["repair_test_requested"]:
            return jsonify({
                "ok": False,
                "message": "No pending Repairing Test request.",
                **snapshot()
            }), 400

        # During the temporary test, close all three simulated isolators.
        STATE["isolators"] = [False, False, False]
        log("Grid authorized temporary simulated test power.")
        log("Isolator 1 CLOSED for test.")
        log("Isolator 2 CLOSED for test.")
        log("Isolator 3 CLOSED for test.")

        STATE["test_power_on"] = True
        STATE["state"] = "TEST_POWER_ON"
        log("SIMULATED TEST POWER ON.")

        return jsonify({
            "ok": True,
            "message": "Temporary simulated test power is ON.",
            **snapshot()
        })


    # ========================================================
    # LINEMAN CLEAR
    # ========================================================

    if action == "clear":

        if STATE["state"] != "TEST_POWER_ON":

            return jsonify({

                "ok": False,

                "message":
                    "Maintenance lock is not active.",

                **snapshot()

            }), 400


        # REPAIRING OFF automatically switches temporary test power OFF.
        STATE["test_power_on"] = False

        # After Repairing OFF, immediately re-isolate the line for clearance.
        STATE["isolators"] = [True, True, True]
        log("SIMULATED TEST POWER AUTOMATICALLY OFF.")
        log("Isolator 1 OPEN — post-test isolation.")
        log("Isolator 2 OPEN — post-test isolation.")
        log("Isolator 3 OPEN — post-test isolation.")

        STATE["repair_test_passed"] = True
        STATE["state"] = "CLEAR_PENDING"
        STATE["safety_confirmed"] = False

        log("REPAIRING OFF received. Temporary test power automatically switched OFF.")
        log(
            f"CLEARANCE received from {STATE['lineman']['name']}. Awaiting safety confirmation."
        )


        return jsonify({

            "ok": True,

            "message":
                "Clear received. "
                "Awaiting Grid authorization.",

            **snapshot()

        })


    # ========================================================
    # SAFETY CONFIRMATION
    # ========================================================

    if action == "safety_confirm":

        if STATE["state"] != "CLEAR_PENDING" or not STATE["repair_test_passed"] or STATE["test_power_on"]:

            return jsonify({
                "ok": False,
                "message":
                    "Safety confirmation requires completed test, CLEAR, and test power OFF.",
                **snapshot()
            }), 400

        STATE["safety_confirmed"] = True
        STATE["state"] = "SAFETY_CONFIRMED"

        log(
            f"SAFETY CONFIRMATION received from {STATE['lineman']['name']}"
        )

        return jsonify({
            "ok": True,
            "message":
                "Safety confirmation received. Awaiting Grid restoration authorization.",
            **snapshot()
        })


    # ========================================================
    # AUTHORIZE RESTORATION
    # ========================================================

    if action == "authorize_restoration":

        if STATE["state"] != "SAFETY_CONFIRMED" or STATE["test_power_on"]:


            return jsonify({

                "ok": False,

                "message":
                    "Restoration requires lineman CLEAR and safety confirmation first.",

                **snapshot()

            }), 400


        STATE["state"] = (
            "RESTORING"
        )


        log(
            "Grid authorized restoration."
        )


        STATE["isolators"] = [

            False,
            False,
            False

        ]


        log(
            "Isolator 1 CLOSED"
        )

        log(
            "Isolator 2 CLOSED"
        )

        log(
            "Isolator 3 CLOSED"
        )


        STATE["state"] = "IDLE"
        STATE["repair_test_requested"] = False
        STATE["test_power_on"] = False
        STATE["repair_test_passed"] = False
        STATE["safety_confirmed"] = False


        log(
            "System restored successfully."
        )


        log(
            "System returned to IDLE."
        )


        return jsonify({

            "ok": True,

            "message":
                "System restored successfully.",

            **snapshot()

        })


    # ========================================================
    # UNKNOWN ACTION
    # ========================================================

    return jsonify({

        "ok": False,

        "message":
            "Unknown action.",

        **snapshot()

    }), 404


# ============================================================
# RESET DEMO
# ============================================================

@app.post("/api/reset")
def reset():

    STATE["state"] = "IDLE"

    STATE["isolators"] = [

        False,
        False,
        False

    ]

    STATE["lineman"] = None

    STATE["events"] = [

        "System reset to IDLE"

    ]

    STATE["request_id"] = None

    STATE["work_location"] = None
    STATE["safety_confirmed"] = False
    STATE["repair_test_requested"] = False
    STATE["test_power_on"] = False
    STATE["repair_test_passed"] = False


    return jsonify({

        "ok": True,

        "message":
            "Demo reset successfully.",

        **snapshot()

    })


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=False

    )
