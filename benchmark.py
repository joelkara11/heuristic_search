# benchmark.py
# --- Run A* 100× for both heuristics and measure time + nodes ---

import time, random, statistics, csv
from puzzle import random_walk, GOAL
from heuristics import hamming, manhattan
from astar import astar

def run_experiment(n_runs=100, seed=42):
    rng = random.Random(seed)
    results = []

    for i in range(n_runs):
        start = random_walk(GOAL, steps=rng.randint(8,24))
        for name, h in [("hamming", hamming), ("manhattan", manhattan)]:
            t0 = time.perf_counter()
            path, expanded = astar(start, h)
            t1 = time.perf_counter()
            results.append({
                "run": i,
                "heuristic": name,
                "expanded": expanded,
                "time_ms": (t1 - t0) * 1000,
                "solution_len": len(path) - 1
            })

    # Summary
    summary = {}
    for h in ["hamming","manhattan"]:
        subset = [r for r in results if r["heuristic"]==h]
        mean_exp = statistics.mean(r["expanded"] for r in subset)
        std_exp = statistics.pstdev(r["expanded"] for r in subset)
        mean_t = statistics.mean(r["time_ms"] for r in subset)
        std_t = statistics.pstdev(r["time_ms"] for r in subset)
        summary[h] = {
            "expanded_mean": mean_exp,
            "expanded_std": std_exp,
            "time_mean_ms": mean_t,
            "time_std_ms": std_t
        }

    # Print summary
    print("\\n=== SUMMARY (100 runs) ===")
    for h,v in summary.items():
        print(f"{h.upper():10s} | Expanded: {v['expanded_mean']:.1f} ± {v['expanded_std']:.1f}"
              f" | Time: {v['time_mean_ms']:.1f} ± {v['time_std_ms']:.1f} ms")

    # Save CSV
    with open("results.csv","w",newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    run_experiment()
