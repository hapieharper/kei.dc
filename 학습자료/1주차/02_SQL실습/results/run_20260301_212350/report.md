# SQL Workbook Execution Report

- Run at: 2026-03-01T21:23:50
- Database: `data/db/stt_sign_pple_mm.sqlite`
- SQL files: 2
- Max rows per result: 100

## File: `1주차/02_SQL실습/sql/eda_결정금액_예시.sql`

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

## File: `1주차/02_SQL실습/sql/eda_추가칼럼_예시.sql`

- Statements: 6

### Q1

- Type: SELECT
- Export rows: 10
- CSV: `csv/eda_추가칼럼_예시_q01.csv`

| claim_amt | cnt |
| --- | --- |
| 10000.0 | 54318 |
| 300000.0 | 48396 |
| 60000.0 | 43765 |
| 20000.0 | 42589 |
| 30000.0 | 40514 |

### Q2

- Type: SELECT
- Export rows: 1
- CSV: `csv/eda_추가칼럼_예시_q02.csv`

| outlier_cnt |
| --- |
| 58191 |

### Q3

- Type: SELECT
- Export rows: 10
- CSV: `csv/eda_추가칼럼_예시_q03.csv`

| disease_code | disease_name | claim_lines |
| --- | --- | --- |
| J209 | 급성 기관지염 | 107966 |
| J304 | 혈관운동성 및 알레르기성 비염 | 32253 |
| J219 | 급성 세기관지염 | 26453 |
| J189 | 상세불명 병원체의 폐렴 | 25858 |
| S134 | 목 부위에서의 관절 및 인대의 탈구, 염좌 및 긴장 | 17163 |

### Q4

- Type: SELECT
- Export rows: 10
- CSV: `csv/eda_추가칼럼_예시_q04.csv`

| hospital_type_code | claim_lines |
| --- | --- |
| C | 360707 |
| B | 191554 |
| A | 151989 |
| M | 82029 |
| E | 12654 |

### Q5

- Type: SELECT
- Export rows: 10
- CSV: `csv/eda_추가칼럼_예시_q05.csv`

| lag_days | cnt |
| --- | --- |
| 0 | 399964 |
| 1 | 202740 |
| 3 | 65824 |
| 2 | 34116 |
| 4 | 22928 |

### Q6

- Type: SELECT
- Export rows: 10
- CSV: `csv/eda_추가칼럼_예시_q06.csv`

| lag_days | lines | avg_decided_amt |
| --- | --- | --- |
| 0 | 399964 | 168847.0 |
| 1 | 202740 | 224773.0 |
| 3 | 65824 | 293726.0 |
| 2 | 34116 | 354874.0 |
| 4 | 22928 | 506354.0 |

## Summary

- SQL files executed: 2
- SELECT results exported: 11
- Output directory: `1주차/02_SQL실습/results/run_20260301_212350`
