from datetime import datetime
from uuid import uuid4


def generate_report_no():
    return f"RP{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid4().hex[:6].upper()}"

