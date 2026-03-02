-- 파일명: eda_결정금액_예시.sql
-- 목적: 결정금액(Integer>Currency) 컬럼 EDA 실습용 SQL
-- 테이블: stt_sign_pple_mm

-- 1) 전처리: 통화 문자열을 숫자로 변환한 뷰(CTE)
WITH base AS (
  SELECT
    CAST(
      NULLIF(
        REPLACE(REPLACE(REPLACE(COALESCE("결정금액(Integer>Currency)", ''), char(8361), ''), ',', ''), ' ', ''),
        ''
      ) AS REAL
    ) AS decided_amt
  FROM "stt_sign_pple_mm"
)
SELECT *
FROM base
LIMIT 5;

-- 2) 빈도분석: 자주 등장하는 결정금액 Top 10
WITH base AS (
  SELECT
    CAST(
      NULLIF(
        REPLACE(REPLACE(REPLACE(COALESCE("결정금액(Integer>Currency)", ''), char(8361), ''), ',', ''), ' ', ''),
        ''
      ) AS REAL
    ) AS decided_amt
  FROM "stt_sign_pple_mm"
)
SELECT
  decided_amt,
  COUNT(*) AS cnt
FROM base
WHERE decided_amt IS NOT NULL
GROUP BY decided_amt
ORDER BY cnt DESC, decided_amt ASC
LIMIT 10;

-- 3) 기술통계(핵심): count/min/max/avg
WITH base AS (
  SELECT
    CAST(
      NULLIF(
        REPLACE(REPLACE(REPLACE(COALESCE("결정금액(Integer>Currency)", ''), char(8361), ''), ',', ''), ' ', ''),
        ''
      ) AS REAL
    ) AS decided_amt
  FROM "stt_sign_pple_mm"
)
SELECT
  COUNT(*) AS n,
  MIN(decided_amt) AS min_amt,
  AVG(decided_amt) AS avg_amt,
  MAX(decided_amt) AS max_amt
FROM base
WHERE decided_amt IS NOT NULL;

-- 4) 이상치(IQR 기준 상한=690000) 건수
WITH base AS (
  SELECT
    CAST(
      NULLIF(
        REPLACE(REPLACE(REPLACE(COALESCE("결정금액(Integer>Currency)", ''), char(8361), ''), ',', ''), ' ', ''),
        ''
      ) AS REAL
    ) AS decided_amt
  FROM "stt_sign_pple_mm"
)
SELECT
  COUNT(*) AS outlier_cnt
FROM base
WHERE decided_amt > 690000;

-- 5) 이상치 담보 기여도 Top 10
WITH base AS (
  SELECT
    "담보코드명" AS coverage_name,
    CAST(
      NULLIF(
        REPLACE(REPLACE(REPLACE(COALESCE("결정금액(Integer>Currency)", ''), char(8361), ''), ',', ''), ' ', ''),
        ''
      ) AS REAL
    ) AS decided_amt
  FROM "stt_sign_pple_mm"
)
SELECT
  coverage_name,
  COUNT(*) AS outlier_lines,
  ROUND(SUM(decided_amt), 0) AS outlier_amt_sum
FROM base
WHERE decided_amt > 690000
GROUP BY coverage_name
ORDER BY outlier_amt_sum DESC
LIMIT 10;
