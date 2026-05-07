"""
Purpose:    Merge per-worker transform output shards into combined files.
            Concatenates *.nq shards, merges werk_staging DuckDB tables, sums *-stats.json.
            Shard files are deleted only after all merges complete without error.
Usage:      python -m transform merge <out_base>
                [--nq PATH] [--db PATH] [--stats PATH]
Inputs:     <out_base>/**/*.nq                   N-Quads shards (one per worker)
            <out_base>/**/*-werk-staging.duckdb  DuckDB werk_staging shards
            <out_base>/**/*-stats.json           per-worker stats JSON files
Outputs:    <out_base>/combined.nq               merged N-Quads (or --nq)
            <out_base>/werk-staging-merged.duckdb merged werk_staging (or --db)
            <out_base>/combined-stats.json        merged stats (or --stats)
Deps:       stdlib only + duckdb (pip install duckdb) for .duckdb merge
Assumes:    All shards produced by `python -m transform` with compatible --stats level.
            Output files are overwritten if they already exist.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path


def _merge_nq(paths: list[Path], out: Path) -> None:
    with open(out, "w", encoding="utf-8") as fout:
        for p in paths:
            with open(p, encoding="utf-8") as fin:
                for line in fin:
                    fout.write(line)


def _merge_duckdb(paths: list[Path], out: Path) -> int:
    import duckdb
    conn = duckdb.connect(str(out))
    for i, p in enumerate(paths):
        alias = f"shard_{i}"
        conn.execute(f"ATTACH '{p}' AS {alias} (READ_ONLY)")
        if i == 0:
            conn.execute(f"CREATE OR REPLACE TABLE werk_staging AS SELECT * FROM {alias}.werk_staging")
        else:
            conn.execute(f"INSERT INTO werk_staging SELECT * FROM {alias}.werk_staging")
        conn.execute(f"DETACH {alias}")
    rows = conn.execute("SELECT COUNT(*) FROM werk_staging").fetchone()[0]
    conn.close()
    return rows


def _merge_stats(paths: list[Path]) -> dict:
    records     = defaultdict(int)
    by_mt       = defaultdict(int)
    by_ht       = defaultdict(int)
    errors      = defaultdict(int)
    triples     = defaultdict(int)
    by_graph    = defaultdict(int)
    werk        = defaultdict(int)
    by_class    = defaultdict(int)
    dispatch    = defaultdict(int)
    dclass: dict = {}
    elapsed     = 0.0
    stats_level = "none"
    interrupted = False

    for p in paths:
        with open(p) as f:
            s = json.load(f)

        elapsed     += s.get("run", {}).get("elapsed_s", 0)
        stats_level  = s.get("run", {}).get("stats_level", stats_level)
        if s.get("run", {}).get("interrupted"):
            interrupted = True

        r = s.get("records", {})
        records["processed"]          += r.get("processed", 0)
        records["skipped_not_in_ids"] += r.get("skipped_not_in_ids", 0)
        records["uri_sanitized"]      += r.get("uri_sanitized", 0)
        records["uri_split"]          += r.get("uri_split", 0)
        records["uri_about_split"]    += r.get("uri_about_split", 0)
        for k, v in r.get("by_mediatype", {}).items():
            by_mt[k] += v
        for k, v in r.get("by_htype", {}).items():
            by_ht[k] += v
        e = r.get("errors", {})
        errors["json_parse"] += e.get("json_parse", 0)
        errors["transform"]  += e.get("transform", 0)

        t = s.get("triples", {})
        triples["total"] += t.get("total", 0)
        for k, v in t.get("by_graph", {}).items():
            by_graph[k] += v

        w = s.get("werk_staging", {})
        werk["rows"] += w.get("rows", 0)
        for k, v in w.get("by_class", {}).items():
            by_class[k] += v

        d = s.get("dispatch", {})
        for k, v in d.items():
            if isinstance(v, int):
                dispatch[k] += v
            elif isinstance(v, dict):
                if k not in dclass:
                    dclass[k] = defaultdict(int)
                for ck, cv in v.items():
                    dclass[k][ck] += cv

    result: dict = {
        "run": {
            "shards":      len(paths),
            "elapsed_s":   round(elapsed, 1),
            "stats_level": stats_level,
            "interrupted": interrupted,
        },
        "records": {
            "processed":          records["processed"],
            "skipped_not_in_ids": records["skipped_not_in_ids"],
            "by_mediatype": dict(sorted(by_mt.items(), key=lambda x: -x[1])),
            "by_htype":     dict(sorted(by_ht.items(), key=lambda x: -x[1])),
            "uri_sanitized":   records["uri_sanitized"],
            "uri_split":       records["uri_split"],
            "uri_about_split": records["uri_about_split"],
            "errors": dict(errors),
        },
        "triples": {
            "total":    triples["total"],
            "by_graph": dict(by_graph),
        },
        "werk_staging": {
            "rows":     werk["rows"],
            "by_class": dict(sorted(by_class.items(), key=lambda x: -x[1])),
        },
    }
    if dclass or dispatch:
        result["dispatch"] = {**dict(dispatch), **{k: dict(v) for k, v in dclass.items()}}
    return result


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(
        description="Merge per-worker transform shards: .nq, werk_staging, stats"
    )
    parser.add_argument("out_base", type=Path,
                        help="Run directory containing shard subdirectories")
    parser.add_argument("--nq",    type=Path, default=None,
                        help="Output .nq path (default: <out_base>/combined.nq)")
    parser.add_argument("--db",    type=Path, default=None,
                        help="Output DuckDB path (default: <out_base>/werk-staging-merged.duckdb)")
    parser.add_argument("--stats", type=Path, default=None,
                        help="Output stats path (default: <out_base>/combined-stats.json)")
    args = parser.parse_args(argv)

    out_base  = args.out_base
    nq_out    = args.nq    or out_base / "combined.nq"
    db_out    = args.db    or out_base / "werk-staging-merged.duckdb"
    stats_out = args.stats or out_base / "combined-stats.json"

    nq_paths    = sorted(p for p in out_base.rglob("*.nq")                  if p != nq_out)
    db_paths    = sorted(p for p in out_base.rglob("*-werk-staging.duckdb") if p != db_out)
    stats_paths = sorted(p for p in out_base.rglob("*-stats.json")          if p != stats_out)

    if not nq_paths:
        print(f"No *.nq shard files found under {out_base}", file=sys.stderr)
        sys.exit(1)

    to_delete: list[Path] = []
    try:
        _merge_nq(nq_paths, nq_out)
        to_delete.extend(nq_paths)
        sz = nq_out.stat().st_size
        print(f"  .nq:    {len(nq_paths)} shards → {nq_out} ({sz / 1_000_000:.1f} MB)")

        if db_paths:
            try:
                rows = _merge_duckdb(db_paths, db_out)
                to_delete.extend(db_paths)
                print(f"  .duckdb: {len(db_paths)} shards → {db_out} ({rows:,} rows)")
            except ImportError:
                print("  .duckdb: duckdb not installed — skipping (shards retained)")
        else:
            print("  .duckdb: no shards found — skipping")

        if stats_paths:
            merged = _merge_stats(stats_paths)
            with open(stats_out, "w") as f:
                json.dump(merged, f, indent=2)
            to_delete.extend(stats_paths)
            r = merged["records"]
            t = merged["triples"]
            print(f"  stats:  {len(stats_paths)} shards → {stats_out} "
                  f"({r['processed']:,} records, {t['total']:,} triples)")
        else:
            print("  stats:  no shards found — skipping")

    except Exception as exc:
        print(f"Merge error: {exc} — shard files retained", file=sys.stderr)
        sys.exit(1)

    for p in to_delete:
        p.unlink()
    print(f"Merged and deleted {len(to_delete)} shard files.")
