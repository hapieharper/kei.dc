# 주요 질문과 SQL 쿼리

- 데이터베이스: `data/db/stt_sign_pple_mm.sqlite`
- 테이블: `stt_sign_pple_mm`

## Q1. 어떤 계약(증권번호)에서 청구가 많이 발생하는가?

```sql
SELECT
  "증권번호(Integer>String)" AS policy_no,
  COUNT(*) AS claim_lines,
  COUNT(DISTINCT "사고번호(Real>String)") AS claim_cases
FROM "stt_sign_pple_mm"
GROUP BY "증권번호(Integer>String)"
ORDER BY claim_lines DESC
LIMIT 5;
```

검증 포인트:
- `claim_lines`가 큰 순서로 상위 5개 증권번호가 조회되면 정상

## Q2. 보장 대상(피보험자) 기준으로 청구가 많이 발생한 사람은 누구인가?

```sql
SELECT
  "피보험자고객번호(LongInteger>String)" AS insured_id,
  "피보험자고객명" AS insured_name,
  COUNT(*) AS claim_lines,
  COUNT(DISTINCT "사고번호(Real>String)") AS claim_cases
FROM "stt_sign_pple_mm"
GROUP BY "피보험자고객번호(LongInteger>String)", "피보험자고객명"
ORDER BY claim_lines DESC
LIMIT 5;
```

검증 포인트:
- 상위 행의 `claim_lines`가 2자리 이상(수십 건 이상)으로 조회되면 정상

## Q3. 사고일과 청구일 간 시차(청구지연일수)는 얼마나 되는가?

```sql
SELECT
  "사고번호(Real>String)" AS accident_no,
  "사고년월일" AS accident_date,
  "사고청구년월일" AS claim_date,
  CAST(julianday("사고청구년월일") - julianday("사고년월일") AS INTEGER) AS delay_days
FROM "stt_sign_pple_mm"
WHERE length("사고년월일") = 10
  AND length("사고청구년월일") = 10
  AND julianday("사고청구년월일") >= julianday("사고년월일")
ORDER BY delay_days DESC
LIMIT 5;
```

검증 포인트:
- `delay_days`가 큰 순으로 조회되고, 음수 값이 나오지 않으면 정상

## Q4. 청구가 많은 질병코드/질병명은 무엇인가?

```sql
SELECT
  "질병코드" AS disease_code,
  "질병명" AS disease_name,
  COUNT(*) AS claim_lines,
  COUNT(DISTINCT "사고번호(Real>String)") AS claim_cases
FROM "stt_sign_pple_mm"
WHERE COALESCE("질병코드", '') <> ''
GROUP BY "질병코드", "질병명"
ORDER BY claim_lines DESC
LIMIT 5;
```

검증 포인트:
- 상위 코드에 `J209`, `J304` 같은 주요 코드가 포함되면 정상

## Q5. 청구가 많은 병원은 어디인가?

```sql
SELECT
  "병원코드(Integer>String)" AS hospital_code,
  "병원명" AS hospital_name,
  COUNT(*) AS claim_lines,
  COUNT(DISTINCT "사고번호(Real>String)") AS claim_cases
FROM "stt_sign_pple_mm"
GROUP BY "병원코드(Integer>String)", "병원명"
ORDER BY claim_lines DESC
LIMIT 5;
```

검증 포인트:
- 상위 병원에 대형 상급종합병원(예: 세브란스, 서울아산 등)이 포함되면 정상

## Q6. 담보코드명별 청구금액과 결정금액, 지급률은 어떻게 되는가?

```sql
WITH amt AS (
  SELECT
    "담보코드명" AS coverage_name,
    CAST(NULLIF(REPLACE(REPLACE(REPLACE(COALESCE("청구보험금액(Integer>Currency)", ''), char(8361), ''), ',', ''), ' ', ''), '') AS REAL) AS claim_amt,
    CAST(NULLIF(REPLACE(REPLACE(REPLACE(COALESCE("결정금액(Integer>Currency)", ''), char(8361), ''), ',', ''), ' ', ''), '') AS REAL) AS decided_amt
  FROM "stt_sign_pple_mm"
)
SELECT
  coverage_name,
  COUNT(*) AS lines,
  ROUND(SUM(COALESCE(claim_amt, 0)), 0) AS claim_amt_sum,
  ROUND(SUM(COALESCE(decided_amt, 0)), 0) AS decided_amt_sum,
  ROUND(CASE WHEN SUM(COALESCE(claim_amt, 0)) = 0 THEN NULL
             ELSE SUM(COALESCE(decided_amt, 0)) * 1.0 / SUM(COALESCE(claim_amt, 0)) END, 4) AS payout_ratio
FROM amt
GROUP BY coverage_name
ORDER BY claim_amt_sum DESC
LIMIT 5;
```

검증 포인트:
- `claim_amt_sum >= decided_amt_sum` 경향이 보이고, `payout_ratio`가 0~1 범위면 정상

## Q7. 유의대상병원 여부에 따라 청구 건수와 결정금액 규모 차이가 있는가?

```sql
WITH amt AS (
  SELECT
    COALESCE("유의대상병원여부", '(blank)') AS watch_hospital_yn,
    CAST(NULLIF(REPLACE(REPLACE(REPLACE(COALESCE("결정금액(Integer>Currency)", ''), char(8361), ''), ',', ''), ' ', ''), '') AS REAL) AS decided_amt
  FROM "stt_sign_pple_mm"
)
SELECT
  watch_hospital_yn,
  COUNT(*) AS claim_lines,
  ROUND(SUM(COALESCE(decided_amt, 0)), 0) AS decided_amt_sum,
  ROUND(AVG(COALESCE(decided_amt, 0)), 0) AS avg_decided_amt
FROM amt
GROUP BY watch_hospital_yn
ORDER BY claim_lines DESC
LIMIT 5;
```

검증 포인트:
- `watch_hospital_yn` 값으로 그룹이 2개 이상 나오고 각 그룹 건수가 조회되면 정상
