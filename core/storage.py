import json
import os
from datetime import datetime

TEST_FILE = "data/testcases.json"
HISTORY_FILE = "data/history.json"


def save_testcases(testcases):
    if not os.path.exists("data"):
        os.makedirs("data")

    with open(TEST_FILE, "w") as f:
        json.dump(testcases, f, indent=4)


def load_testcases():
    if not os.path.exists(TEST_FILE):
        return []

    with open(TEST_FILE, "r") as f:
        return json.load(f)


# -------- HISTORY --------
def save_test_run(results):
    if not os.path.exists("data"):
        os.makedirs("data")

    history = []

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)

    run = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "results": results
    }

    history.append(run)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r") as f:
        return json.load(f)