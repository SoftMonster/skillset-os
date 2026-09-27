---
name: performance-tuning
description: "Speeds up code and systems by measuring first: establishes a benchmark, profiles to find the real hotspot, applies the fix with the best payoff (algorithm, I/O batching, caching, concurrency), and proves the gain with before and after numbers. Use when the user says something is slow, times out, uses too much memory or CPU, wants to optimise or profile code, reduce latency, or improve load time or throughput. Do not use for a single slow SQL query; use database-design."
trigger: "make code, a query or an app faster or use less memory"
command: "tune performance"
metadata:
  version: "1.0.1"
---

# Performance tuning

🧬 **Core meme:** Measure first, fix the real hotspot, and prove the gain.

Make it measurably faster or leaner where it matters, without making it wrong or unreadable. Every claim of improvement comes with numbers from the same benchmark before and after.

## Workflow

```
- [ ] 1. Define the target
- [ ] 2. Build a repeatable benchmark
- [ ] 3. Profile to find the hotspot
- [ ] 4. Fix the biggest cost first
- [ ] 5. Re-measure and check correctness
- [ ] 6. Report
```

1. **Target.** Which operation, how slow now, how fast it needs to be ("p95 of /search under 300 ms at 50 rps"). Without a target, optimisation never ends.
2. **Benchmark.** A script or test that runs the slow path on realistic data sizes and prints timing. Warm up, repeat, and report the median (and p95 for latency). Use `hyperfine` for commands, `pytest-benchmark` or `timeit` for Python, `go test -bench`, `criterion` for Rust, and `vitest bench` or `tinybench` for JavaScript.
3. **Profile.** Do not guess; the hotspot is usually not where people expect. Python: `py-spy record -o profile.svg -- python app.py` or `python -m cProfile -s cumtime`, plus `memray` for memory. Node: `node --cpu-prof` or `clinic flame`. Go: `pprof`. Browser: the Performance panel and Lighthouse. For services, check query counts and timings per request first.
4. **Fix, in the order of typical payoff:**
   1. Do less work: a better algorithm or data structure (a dict or set lookup instead of a list scan, avoiding O(n²) loops).
   2. Batch I/O: fix N+1 queries, bulk inserts, fewer round trips, streaming instead of loading everything.
   3. Avoid repeated work: memoise pure functions, cache with an explicit invalidation plan.
   4. Parallelise I/O-bound work (async, thread pools); use processes or native code for CPU-bound work.
   5. Micro-optimisations last, and only in measured hot loops.
5. **Re-measure** with the same benchmark and run the full test suite. Performance changes are a common source of subtle bugs, especially caching and concurrency.
6. **Report** before and after numbers, what changed, and any trade-off (memory, staleness, complexity).

## Example report

Numbers first and prominent, one point per item:

- 📊 **Result:** `/search` p95 1,840 ms → 210 ms (50 rps, 1M-row dataset, median of 5 runs).
- 🐛 **Cause:** 1 + N queries (one per result) to load tags.
- 🛠️ **Fix:** `prefetch_related('tags')` → 2 queries; index on `items(tenant_id, created_at DESC)` for the ORDER BY, so the plan now uses an Index Scan.
- ⚖️ **Trade-off:** none significant; memory per request +0.4 MB.

## Frontend specifics

Measure with Lighthouse or WebPageTest and work on Core Web Vitals (LCP, INP, CLS). Common wins are smaller JavaScript bundles through code splitting and removing heavy dependencies, correctly sized modern image formats, avoiding layout shift with explicit dimensions, and moving work off the main thread.

## Gotchas

- Benchmarks on tiny inputs mislead; use production-like sizes and data distributions.
- Caches without invalidation plans become correctness bugs. Write down when each entry becomes stale.
- Timing in a noisy sandbox varies. Repeat runs and compare medians, and treat differences under about 10% as noise.
- For a single slow SQL query, use `database-design`, which covers reading query plans.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents software-dev/performance-tuning` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review software-dev/performance-tuning` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
