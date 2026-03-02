#!/usr/bin/env python3
"""
Run SQL workbook files against SQLite and save results to files.

Usage examples:
  python 1주차/02_SQL실습/scripts/run_sql_workbook.py
  python 1주차/02_SQL실습/scripts/run_sql_workbook.py --sql 1주차/02_SQL실습/sql/eda_결정금액_예시.sql
  python 1주차/02_SQL실습/scripts/run_sql_workbook.py --max-rows 5000 --preview-rows 10
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import sqlite3
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run SQL workbook files and export results.")
    p.add_argument(
        "--db",
        default="data/db/stt_sign_pple_mm.sqlite",
        help="SQLite database path",
    )
    p.add_argument(
        "--sql",
        action="append",
        default=[],
        help="SQL file path (repeatable). If omitted, files from --sql-dir are used.",
    )
    p.add_argument(
        "--sql-dir",
        default="1주차/02_SQL실습/sql",
        help="Directory containing .sql files",
    )
    p.add_argument(
        "--out",
        default="1주차/02_SQL실습/results",
        help="Output root directory",
    )
    p.add_argument(
        "--max-rows",
        type=int,
        default=2000,
        help="Max rows exported per SELECT result",
    )
    p.add_argument(
        "--preview-rows",
        type=int,
        default=5,
        help="Rows shown in markdown preview per SELECT result",
    )
    p.add_argument(
        "--encoding",
        default="utf-8",
        help="Encoding for .sql files",
    )
    return p.parse_args()


def resolve_sql_files(explicit: Sequence[str], sql_dir: str) -> List[Path]:
    if explicit:
        files = [Path(x) for x in explicit]
    else:
        files = sorted(Path(sql_dir).glob("*.sql"))
    return [f for f in files if f.exists() and f.is_file()]


def split_sql_statements(sql_text: str) -> List[str]:
    """
    Split SQL text into executable statements while respecting semicolons in strings.
    Uses sqlite3.complete_statement for robust chunking.
    """
    statements: List[str] = []
    buf = ""
    for line in sql_text.splitlines():
        stripped = line.strip()
        # Skip full-line comments to avoid buffering comment+statement as one chunk.
        if stripped.startswith("--"):
            continue
        buf += line + "\n"
        if sqlite3.complete_statement(buf):
            candidate = buf.strip()
            buf = ""
            if not candidate:
                continue
            if candidate.rstrip(";").strip():
                statements.append(candidate)
    trailing = buf.strip()
    if trailing and trailing.rstrip(";").strip():
        statements.append(trailing)
    return statements


def write_csv(path: Path, headers: Sequence[str], rows: Sequence[Sequence[object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(rows)


def md_escape(value: object) -> str:
    if value is None:
        return "NULL"
    s = str(value).replace("\n", " ")
    return s.replace("|", "\\|")


def md_table(headers: Sequence[str], rows: Sequence[Sequence[object]]) -> str:
    if not headers:
        return "_No columns_"
    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        lines.append("| " + " | ".join(md_escape(v) for v in row) + " |")
    return "\n".join(lines)


def execute_sql_file(
    conn: sqlite3.Connection,
    sql_file: Path,
    run_dir: Path,
    max_rows: int,
    preview_rows: int,
    encoding: str,
) -> Tuple[List[str], int]:
    sql_text = sql_file.read_text(encoding=encoding)
    statements = split_sql_statements(sql_text)
    report_lines: List[str] = []
    report_lines.append(f"## File: `{sql_file.as_posix()}`")
    report_lines.append("")
    report_lines.append(f"- Statements: {len(statements)}")
    report_lines.append("")

    select_count = 0
    for idx, stmt in enumerate(statements, start=1):
        cur = conn.cursor()
        cur.execute(stmt)
        title = f"### Q{idx}"

        if cur.description:
            select_count += 1
            headers = [d[0] for d in cur.description]
            rows = cur.fetchmany(max_rows + 1)
            truncated = len(rows) > max_rows
            export_rows = rows[:max_rows]
            csv_name = f"{sql_file.stem}_q{idx:02d}.csv"
            csv_path = run_dir / "csv" / csv_name
            write_csv(csv_path, headers, export_rows)

            preview = export_rows[:preview_rows]
            report_lines.append(title)
            report_lines.append("")
            report_lines.append(f"- Type: SELECT")
            report_lines.append(f"- Export rows: {len(export_rows)}")
            report_lines.append(f"- CSV: `csv/{csv_name}`")
            if truncated:
                report_lines.append(
                    f"- Note: result truncated at {max_rows} rows (increase `--max-rows` if needed)"
                )
            report_lines.append("")
            report_lines.append(md_table(headers, preview))
            report_lines.append("")
        else:
            conn.commit()
            affected = cur.rowcount
            report_lines.append(title)
            report_lines.append("")
            report_lines.append("- Type: NON-SELECT")
            report_lines.append(f"- Affected rows: {affected}")
            report_lines.append("")

    return report_lines, select_count


def main() -> int:
    args = parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {db_path}")

    sql_files = resolve_sql_files(args.sql, args.sql_dir)
    if not sql_files:
        raise FileNotFoundError("No SQL files found. Check --sql or --sql-dir.")

    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = Path(args.out) / f"run_{timestamp}"
    run_dir.mkdir(parents=True, exist_ok=True)

    report: List[str] = []
    report.append("# SQL Workbook Execution Report")
    report.append("")
    report.append(f"- Run at: {dt.datetime.now().isoformat(timespec='seconds')}")
    report.append(f"- Database: `{db_path.as_posix()}`")
    report.append(f"- SQL files: {len(sql_files)}")
    report.append(f"- Max rows per result: {args.max_rows}")
    report.append("")

    total_select = 0
    with sqlite3.connect(db_path) as conn:
        for sql_file in sql_files:
            section, select_count = execute_sql_file(
                conn=conn,
                sql_file=sql_file,
                run_dir=run_dir,
                max_rows=args.max_rows,
                preview_rows=args.preview_rows,
                encoding=args.encoding,
            )
            report.extend(section)
            total_select += select_count

    report.append("## Summary")
    report.append("")
    report.append(f"- SQL files executed: {len(sql_files)}")
    report.append(f"- SELECT results exported: {total_select}")
    report.append(f"- Output directory: `{run_dir.as_posix()}`")
    report.append("")

    report_path = run_dir / "report.md"
    report_path.write_text("\n".join(report), encoding="utf-8")

    print(f"Done. Report: {report_path.as_posix()}")
    print(f"CSV dir: {(run_dir / 'csv').as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
