import os
from utils.db import DBConnInfo


def get_warehouse_creds() -> DBConnInfo:
    return DBConnInfo(
        user=os.getenv('WAREHOUSE_USER', ''),
        password=os.getenv('WAREHOUSE_PASSWORD', ''),
        db=os.getenv('WAREHOUSE_DB', ''),
        host=os.getenv('WAREHOUSE_HOST', ''),
        port=int(os.getenv('WAREHOUSE_PORT', 5432)),
    )
