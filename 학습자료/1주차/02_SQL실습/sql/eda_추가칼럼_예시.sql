-- 파일명: eda_추가칼럼_예시.sql
-- 목적: 신입 실습용 추가 컬럼 EDA 예시
-- 테이블: stt_sign_pple_mm

-- [칼럼 A] 청구보험금액(Integer>Currency): 빈도분석 Top 10
WITH base AS (
  SELECT
    CAST(
      NULLIF(
        REPLACE(REPLACE(REPLACE(COALESCE("청구보험금액(Integer>Currency)", ''), char(8361), ''), ',', ''), ' ', ''),
        ''
      ) AS REAL
    ) AS claim_amt
  FROM "stt_sign_pple_mm"
)
SELECT
  claim_amt,
  COUNT(*) AS cnt
FROM base
WHERE claim_amt IS NOT NULL
GROUP BY claim_amt
ORDER BY cnt DESC, claim_amt ASC
LIMIT 10;

-- [칼럼 A] 청구보험금액(Integer>Currency): 이상치(IQR 상한=690000) 건수
WITH base AS (
  SELECT
    CAST(
      NULLIF(
        REPLACE(REPLACE(REPLACE(COALESCE("청구보험금액(Integer>Currency)", ''), char(8361), ''), ',', ''), ' ', ''),
        ''
      ) AS REAL
    ) AS claim_amt
  FROM "stt_sign_pple_mm"
)
SELECT
  COUNT(*) AS outlier_cnt
FROM base
WHERE claim_amt > 690000;

-- [칼럼 B] 질병코드/질병명: 빈도 Top 10
SELECT
  "질병코드" AS disease_code,
  "질병명" AS disease_name,
  COUNT(*) AS claim_lines
FROM "stt_sign_pple_mm"
WHERE COALESCE("질병코드", '') <> ''
GROUP BY "질병코드", "질병명"
ORDER BY claim_lines DESC
LIMIT 10;

-- [칼럼 C] 병원종별구분코드: 분포 확인
SELECT
  COALESCE("병원종별구분코드", '(blank)') AS hospital_type_code,
  COUNT(*) AS claim_lines
FROM "stt_sign_pple_mm"
GROUP BY COALESCE("병원종별구분코드", '(blank)')
ORDER BY claim_lines DESC
LIMIT 10;

-- [칼럼 D] 청구일->지급일 지연일수: 운영 지표 분포
SELECT
  CAST(julianday("지급년월일") - julianday("사고청구년월일") AS INTEGER) AS lag_days,
  COUNT(*) AS cnt
FROM "stt_sign_pple_mm"
WHERE length("사고청구년월일") = 10
  AND length("지급년월일") = 10
  AND julianday("지급년월일") >= julianday("사고청구년월일")
GROUP BY lag_days
ORDER BY cnt DESC
LIMIT 10;

-- [칼럼 D] 지연일수와 결정금액 동시 확인 (상위 100건 평균)
WITH base AS (
  SELECT
    CAST(julianday("지급년월일") - julianday("사고청구년월일") AS INTEGER) AS lag_days,
    CAST(
      NULLIF(
        REPLACE(REPLACE(REPLACE(COALESCE("결정금액(Integer>Currency)", ''), char(8361), ''), ',', ''), ' ', ''),
        ''
      ) AS REAL
    ) AS decided_amt
  FROM "stt_sign_pple_mm"
  WHERE length("사고청구년월일") = 10
    AND length("지급년월일") = 10
    AND julianday("지급년월일") >= julianday("사고청구년월일")
)
SELECT
  lag_days,
  COUNT(*) AS lines,
  ROUND(AVG(decided_amt), 0) AS avg_decided_amt
FROM base
GROUP BY lag_days
ORDER BY lines DESC
LIMIT 10;
