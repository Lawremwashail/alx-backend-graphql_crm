#!/bin/bash
# Script: clean_inactive_customers.sh
# Purpose: Delete customers with no orders in the past year
# Logs result to /tmp/customer_cleanup_log.txt

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_DIR"

# Run Django shell to delete inactive customers
deleted_count=$(python3 manage.py shell <<'EOF'
from crm.models import Customer, Order
from django.utils import timezone
from datetime import timedelta

one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.exclude(orders__order_date__gte=one_year_ago)
count = inactive_customers.count()
inactive_customers.delete()
print(count)
EOF
)

# Log results with timestamp
echo "$(date '+%Y-%m-%d %H:%M:%S') - Deleted $deleted_count inactive customers" >> /tmp/customer_cleanup_log.txt

