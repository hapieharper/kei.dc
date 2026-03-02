# 1주차 보고서 예시: 결정금액 EDA

## 1) 분석 목적
- 본 분석은 보험금 청구 데이터에서 `결정금액` 분포와 고액 지급 패턴을 확인하기 위해 수행했다.
- 특히 고액 지급이 어떤 담보에서 많이 발생하는지 확인하고, 운영적으로 점검이 필요한 영역을 찾는 것이 목적이다.
- 추가로 `청구일 -> 지급일` 지연일수 분포를 함께 확인해 처리 속도 관점의 인사이트를 도출했다.

## 2) 데이터/범위
- 사용 테이블: `stt_sign_pple_mm`
- 건수 기준(라인수/사고건수): 라인수 기준
- 기간/조건: 전체 데이터(822,337건), 별도 필터 없음
- 전처리: `결정금액(Integer>Currency)`의 `₩`, `,`, 공백 제거 후 REAL 변환

## 3) 실행 SQL
### SQL #1 (결정금액 빈도 Top 10)
```sql
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
```

### SQL #2 (결정금액 이상치 건수: IQR 상한 690000)
```sql
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
```

### SQL #3 (청구일->지급일 지연일수 분포 Top 10)
```sql
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
```

## 4) 핵심 결과
| 지표 | 값 | 한 줄 설명 |
| --- | ---: | --- |
| 결정금액 중앙값 | 120,000 | 일반적인 지급 규모는 12만원 수준 |
| 결정금액 이상치 건수 | 55,669 | IQR 상한(690,000) 초과 건수 |
| 결정금액 이상치 비율 | 6.77% | 전체 대비 고액 지급 비중 |
| 지연일수 0일 건수 | 399,964 | 당일 처리 건수 비중이 가장 큼 |
| 지연일수 1일 건수 | 202,740 | 익일 처리도 매우 높은 비중 |

## 5) 비즈니스 해석
1. 결정금액 분포가 특정 정액 단위에 집중되어 정액형 담보 영향이 큰 구조로 보인다.
2. 이상치(고액 지급)는 전체의 6.77%로 무시하기 어려운 비중이며, 담보별로 분리 점검이 필요하다.
3. 처리일수는 0~1일 구간 비중이 높아 일반 처리 속도는 빠른 편이나, 장기 지연 꼬리 구간은 별도 원인 점검이 필요하다.

## 6) 후속 액션
1. 이상치 상위 100건을 추출해 `담보코드명 x 질병코드 x 병원코드` 교차분석 수행
2. 지연일수 7일 이상 건을 별도 분리해 서류 미비/심사 복잡도/특이 담보 여부 점검
3. `청구보험금액` 대비 `결정금액` 지급률을 담보별로 산출해 저지급/고지급 영역 탐색

## 7) 부록(선택)
- 참고 파일/쿼리 경로:
1. `1주차/02_SQL실습/sql/eda_결정금액_예시.sql`
2. `1주차/02_SQL실습/sql/eda_추가칼럼_예시.sql`
3. `1주차/02_SQL실습/주요질문_SQL.md`
- 추가 확인 필요 사항:
1. `DAL_*`, `DEAL_*`, `DAB_*` 내부 코드 정의서 확보
