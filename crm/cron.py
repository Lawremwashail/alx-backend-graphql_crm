from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    # Log timestamp
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_message = f"{timestamp} CRM is alive\n"

    with open("/tmp/crm_heartbeat_log.txt", "a") as log_file:
        log_file.write(log_message)

    # Optional: Query GraphQL hello field
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=False,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=False)

    query = gql("""
        query {
            hello
        }
    """)

    try:
        result = client.execute(query)
        print("GraphQL hello:", result.get("hello"))
    except Exception as e:
        print("GraphQL check failed:", e)

def update_low_stock():
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=False,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=False)

    mutation = gql("""
        mutation {
            updateLowStockProducts {
                success
                message
                updatedProducts {
                    name
                    stock
                }
            }
        }
    """)

    try:
        result = client.execute(mutation)
        updates = result["updateLowStockProducts"]["updatedProducts"]
        timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

        with open("/tmp/low_stock_updates_log.txt", "a") as log_file:
            log_file.write(f"\n{timestamp} - Low stock update:\n")
            for p in updates:
                log_file.write(f"  {p['name']} → {p['stock']}\n")

        print("Low-stock update completed!")

    except Exception as e:
        print("Error updating low-stock products:", e)
