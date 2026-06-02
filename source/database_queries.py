import sqlite3

from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from source.config import DB_PATH


# ==========================================================
# Generic Query Executor
# ==========================================================

def query_db(
    sql: str,
    params: tuple = ()
) -> List[Dict[str, Any]]:

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    try:

        cursor = conn.cursor()

        cursor.execute(
            sql,
            params
        )

        rows = cursor.fetchall()

        return [
            dict(row)
            for row in rows
        ]

    finally:

        conn.close()


# ==========================================================
# Client Queries
# ==========================================================

def get_client(
    client_id: str
) -> Optional[Dict[str, Any]]:

    results = query_db(
        """
        SELECT *
        FROM clients
        WHERE client_id = ?
        """,
        (client_id,)
    )

    return results[0] if results else None


def get_all_clients():

    return query_db(
        """
        SELECT *
        FROM clients
        """
    )


# ==========================================================
# Holdings Queries
# ==========================================================

def get_client_holdings(
    client_id: str
):

    return query_db(
        """
        SELECT *
        FROM holdings
        WHERE client_id = ?
        """,
        (client_id,)
    )


# ==========================================================
# Portfolio Query
# ==========================================================

def get_client_portfolio(
    client_id: str
):

    client = get_client(
        client_id
    )

    if not client:

        return None

    holdings = get_client_holdings(
        client_id
    )

    return {
        "client": client,
        "holdings": holdings
    }


# ==========================================================
# Market Search
# ==========================================================

def search_market_data(
    query: str
):

    q = query.upper()

    return query_db(
        """
        SELECT *
        FROM market_data
        WHERE UPPER(ticker) LIKE ?
        OR UPPER(company_name) LIKE ?
        OR UPPER(sector) LIKE ?
        """,
        (
            f"%{q}%",
            f"%{q}%",
            f"%{q}%"
        )
    )


# ==========================================================
# Startup Validation
# ==========================================================

def validate_database_connection():

    try:

        query_db(
            "SELECT 1"
        )

        return True

    except Exception:

        return False