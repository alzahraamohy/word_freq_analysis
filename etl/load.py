import os
from typing import List, Tuple
import psycopg2
from psycopg2.extras import execute_values
from collections import Counter

#data base connection 
def _connect():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME", "word_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASS", "admin"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
    )

def init_table():
    """Create table if not exists."""
    conn = _connect()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS word_counts (
                    source TEXT NOT NULL,
                    word   TEXT NOT NULL,
                    count  INT  NOT NULL,
                    PRIMARY KEY (source, word)
                );
            """)
            cur.execute("CREATE INDEX IF NOT EXISTS idx_wc_source ON word_counts(source);")
        conn.commit()
    finally:
        conn.close()

def load_counts(counter: Counter, source: str, clear_previous: bool = True):
    """Bulk insert/upsert counts for the given source."""
    if not counter:
        return

    conn = _connect()
    try:
        with conn.cursor() as cur:
            if clear_previous:
                cur.execute("DELETE FROM word_counts WHERE source = %s;", (source,))

            data = [(source, w, c) for w, c in counter.items()]
            execute_values(
                cur,
                """
                INSERT INTO word_counts (source, word, count)
                VALUES %s
                ON CONFLICT (source, word) DO UPDATE SET count = EXCLUDED.count;
                """,
                data,
            )
        conn.commit()
    finally:
        conn.close()

def get_top_words(source: str, limit: int = 10) -> List[Tuple[str, int]]:
    conn = _connect()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT word, count FROM word_counts WHERE source = %s ORDER BY count DESC, word ASC LIMIT %s;",
                (source, limit),
            )
            return cur.fetchall()
    finally:
        conn.close()
