#!/usr/bin/env python3
import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

LOG_FILE = "/tmp/order_reminders_log.txt"
GRAPHQL_URL = "http://localhost:8000/graphql"

def log_message(message):
    """Append messages with timestamps to the log file."""
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} {message}\n")

def main():
    """Query orders from the last 7 days and log reminders."""
    try:
        transport = RequestsHTTPTransport(url=GRAPHQL_URL, verify=False)
        client = Client(transport=transport, fetch_schema_from_transport=True)

        # Calculate date 7 days ago
        week_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")

        # GraphQL query — adjust field names to match your schema
        query = gql(f"""
        {{
            allOrders(orderDate_Gte: "{week_ago}") {{
                id
                customer {{
                    email
                }}
                orderDate
            }}
        }}
        """)

        response = client.execute(query)
        orders = response.get("allOrders", [])

        for order in orders:
            customer_email = order["customer"]["email"]
            order_id = order["id"]
            log_message(f"Reminder: Order #{order_id} for {customer_email}")
        
        print("Order reminders processed!")

    except Exception as e:
        log_message(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
