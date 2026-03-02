# SQL Workbook Execution Report

- Run at: 2026-03-01T21:06:19
- Database: `data/db/stt_sign_pple_mm.sqlite`
- SQL files: 1
- Max rows per result: 1000

## File: `1주차/sql/eda_결정금액_예시.sql`

- Statements: 5

### Q1

- Type: SELECT
- Export rows: 5
- CSV: `csv/eda_결정금액_예시_q01.csv`

| decided_amt |
| --- |
| 20000.0 |
| 300000.0 |
| 10000.0 |
| 490000.0 |
| 20000.0 |

### Q2

- Type: SELECT
- Export rows: 10
- CSV: `csv/eda_결정금액_예시_q02.csv`

| decided_amt | cnt |
| --- | --- |
| 10000.0 | 54288 |
| 300000.0 | 48335 |
| 60000.0 | 43727 |
| 20000.0 | 42560 |
| 30000.0 | 40504 |

### Q3

- Type: SELECT
- Export rows: 1
- CSV: `csv/eda_결정금액_예시_q03.csv`

| n | min_amt | avg_amt | max_amt |
| --- | --- | --- | --- |
| 822337 | 0.0 | 407992.38716365676 | 150000000.0 |

### Q4

- Type: SELECT
- Export rows: 1
- CSV: `csv/eda_결정금액_예시_q04.csv`

| outlier_cnt |
| --- |
| 55669 |

### Q5

- Type: SELECT
- Export rows: 10
- CSV: `csv/eda_결정금액_예시_q05.csv`

| coverage_name | outlier_lines | outlier_amt_sum |
| --- | --- | --- |
| 암 | 10207 | 84113941728.0 |
| 일반사망 | 2405 | 28858186818.0 |
| 입원 | 8140 | 10279790540.0 |
| 재해사망 | 388 | 10259326988.0 |
| 재해 | 7603 | 8092661000.0 |

## Summary

- SQL files executed: 1
- SELECT results exported: 5
- Output directory: `1주차/results/run_20260301_210619`
