import json
from datetime import datetime
import os

LOG_FILE = "logs/actions_log.json"

def log_action(tool, column=None, strategy=None, before=None, after=None):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tool": tool,
        "column": column,
        "strategy": strategy,
        "before": before,
        "after": after
    }

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    logs.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

    return entry
