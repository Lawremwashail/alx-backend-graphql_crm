import datetime
import requests

def log_crm_heartbeat():
    """Logs a heartbeat message every 5 minutes and checks GraphQL health."""
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_message = f"{timestamp} CRM is alive\n"
    log_path = "/tmp/crm_heartbeat_log.txt"

    # Append the heartbeat message to the log file
    with open(log_path, "a") as log_file:
        log_file.write(log_message)

    # Optional: Check GraphQL hello field for responsiveness
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=5
        )
        if response.status_code == 200:
            print("GraphQL endpoint responded successfully.")
        else:
            print("GraphQL endpoint returned an error:", response.status_code)
    except Exception as e:
        print("Error checking GraphQL endpoint:", e)

