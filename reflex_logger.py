import json, datetime

def log_capsule(event, commentary, tags):
    capsule = {
        "timestamp": datetime.datetime.now().isoformat(),
        "event": event,
        "commentary": commentary,
        "tags": tags
    }

    with open("reflex_capsules.json", "a") as f:
        f.write(json.dumps(capsule) + "\n")

# Example usage
log_capsule(
    event="Tunnel failed",
    commentary="Fallback to local preview successful",
    tags=["reflex", "resilience", "offline-mode"]
)
