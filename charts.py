import matplotlib
matplotlib.use("Agg")  
import matplotlib.pyplot as plt
import os
from typing import List, Tuple

def save_chart(rows: List[Tuple[str, int]], output_path: str, title: str = "Top Words"):
    if not rows:
        print("⚠ No rows to plot.")
        return None

    words, counts = zip(*rows)
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.bar(words, counts)
    plt.title(title)
    plt.xlabel("Word")
    plt.ylabel("Count")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return output_path
