import argparse
import os
from dotenv import load_dotenv

load_dotenv()  

from etl.extract import read_file_in_chunks
from etl.transform import count_frequencies_from_chunks
from etl.load import init_table, load_counts, get_top_words
from charts import save_chart

def parse_args():
    p = argparse.ArgumentParser(description="Simple ETL word-frequency -> Postgres -> chart")
    p.add_argument("file_path", help="Path to .txt file to analyze (can be anywhere)")
    p.add_argument("chart_name", help="Name for saved chart (e.g., my_chart.png)")
    p.add_argument("--top", type=int, default=10, help="Top-N words (default 10)")
    p.add_argument("--no-truncate", action="store_true", help="If set, do not clear previous rows for this source")
    return p.parse_args()

def main():
    args = parse_args()
    file_path = args.file_path
    chart_name = args.chart_name
    top_n = args.top
    clear_previous = not args.no_truncate

    if not os.path.isfile(file_path):
        print(f"❌ File not found: {file_path}")
        return

    source = os.path.splitext(os.path.basename(file_path))[0]
    chart_full_path = os.path.join(os.path.dirname(file_path), chart_name)

    print(f"📂 File: {file_path}")
    print(f"🏷 Source label: {source}")
    print("🔁 Starting ETL... (streaming read)")

    # Extract -> Transform
    chunks = read_file_in_chunks(file_path)
    counts = count_frequencies_from_chunks(chunks)

    # Load
    init_table()
    load_counts(counts, source=source, clear_previous=clear_previous)

    # Query top N and save chart
    rows = get_top_words(source=source, limit=top_n)

    print(f"\nTop {top_n} words for '{source}':")
    for w, c in rows:
        print(f"{w:>15}: {c}")

    save_chart(rows, chart_full_path, title=f"Top {top_n} Words — {source}")
    print(f"\n✅ Done. Chart saved to: {chart_full_path}")

if __name__ == "__main__":
    main()
