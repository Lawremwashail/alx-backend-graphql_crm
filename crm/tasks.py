from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime
import os
import requests

@shared_task
def generate_crm_report():
    transport = RequestsHTTPTransport(
        url='http://localhost:8000/graphql/',
        verify=False,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    query = gql("""
    query {
        allCustomers { id }
        allOrders { totalAmount }
    }
    """)

    result = client.execute(query)

    customers = result.get("allCustomers", [])
    orders = result.get("allOrders", [])

    total_customers = len(customers)
    total_orders = len(orders)
    total_revenue = sum(o.get("totalAmount", 0) for o in orders)

    log_entry = (
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - "
        f"Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n"
    )

    os.makedirs("/tmp", exist_ok=True)
    with open("/tmp/crm_report_log.txt", "a") as f:
        f.write(log_entry)

    return log_entry

