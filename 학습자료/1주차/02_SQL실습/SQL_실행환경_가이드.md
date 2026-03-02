# SQL 실행환경 가이드(신입용)

이 문서는 `1주차/02_SQL실습/sql`에 있는 SQL 예시를 실제로 실행하는 방법을 설명합니다.

## 1. 준비물

### A. DBeaver 경로(권장, 신입 기본)

1. DBeaver 설치
2. SQLite DB 파일: `data/db/stt_sign_pple_mm.sqlite`

### B. Python 경로(선택)

1. Python 3.10+
2. 실행 스크립트: `1주차/02_SQL실습/scripts/run_sql_workbook.py`

추가 패키지는 필요 없습니다(표준 라이브러리만 사용).

## 2. DBeaver로 실행하기 (신입 필수 경로)

### 1) 새 연결 만들기

1. DBeaver 실행
2. `Database` -> `New Database Connection`
3. `SQLite` 선택 후 `Next`
4. `Database file`에 아래 파일 선택
- `.../학습자료/data/db/stt_sign_pple_mm.sqlite`
5. `Test Connection` 클릭
6. 드라이버 다운로드 창이 뜨면 `Download` 진행
7. 성공하면 `Finish`

### 2) SQL 열고 실행

1. 연결 우클릭 -> `SQL Editor` -> `Open SQL Script`
2. `1주차/02_SQL실습/주요질문_SQL.md`에서 SQL 복사 또는  
   `1주차/02_SQL실습/sql/eda_결정금액_예시.sql` 열기
3. 실행할 쿼리만 선택 후 `Ctrl+Enter` (선택 쿼리 실행)
4. 스크립트 전체 실행은 툴바 `Execute SQL Script` 버튼 사용

### 3) 결과 저장

1. 결과 그리드 우클릭 -> `Export Resultset`
2. 형식 `CSV` 선택
3. 옵션 권장값
- Encoding: `UTF-8`
- Include column header: `ON`
4. 저장 후 `02_SQL실습/주요질문_SQL_샘플결과.md`와 비교

### 4) 정답 검증 팁

1. 숫자가 완전히 같지 않아도 정렬/필터 조건이 동일하면 상위 패턴은 유사해야 함
2. 특히 Q4(질병코드), Q5(병원), Q6(담보별 금액)의 상위 항목이 유사하면 정상
## 3. Python 스크립트로 실행하기 (선택)

프로젝트 루트(현재 폴더)에서 아래 명령 실행:

```powershell
python 1주차/02_SQL실습/scripts/run_sql_workbook.py
```

실행 결과:
1. `1주차/02_SQL실습/sql/*.sql` 파일을 순서대로 실행
2. 결과를 `1주차/02_SQL실습/results/run_YYYYMMDD_HHMMSS/`에 저장
3. `report.md`와 각 쿼리 결과 `csv/*.csv` 생성

## 4. 특정 SQL 파일만 실행

```powershell
python 1주차/02_SQL실습/scripts/run_sql_workbook.py --sql 1주차/02_SQL실습/sql/eda_결정금액_예시.sql
```

## 5. 결과 저장 행 수 늘리기

기본은 쿼리당 최대 2000행 저장입니다.

```powershell
python 1주차/02_SQL실습/scripts/run_sql_workbook.py --max-rows 10000
```

## 6. 결과 파일 구조

예시:

1. `1주차/02_SQL실습/results/run_20260301_210000/report.md`: 실행 리포트(쿼리 미리보기 포함)
2. `1주차/02_SQL실습/results/run_20260301_210000/csv/eda_결정금액_예시_q01.csv`
3. `1주차/02_SQL실습/results/run_20260301_210000/csv/eda_결정금액_예시_q02.csv`

## 7. 자주 생기는 문제

1. `Database not found`
- `data/db/stt_sign_pple_mm.sqlite` 경로가 맞는지 확인

2. `No SQL files found`
- `1주차/02_SQL실습/sql` 폴더에 `.sql` 파일이 있는지 확인

3. 결과가 2000행에서 잘림
- `--max-rows` 값을 늘려서 실행

4. DBeaver에서 쿼리 일부만 실행됨
- `Ctrl+Enter`는 선택된 쿼리만 실행됨. 전체 실행은 `Execute SQL Script` 사용

5. DBeaver 실행 결과가 샘플과 조금 다름
- 정렬/필터/실행 쿼리 범위 확인 후 상위 패턴(Top 항목) 기준으로 비교

## 8. 주피터 노트북으로 실행하기

노트북 파일:

1. `1주차/02_SQL실습/notebooks/week1_sql_eda_practice.ipynb`

실행 예시:

```powershell
jupyter lab
```

열어서 위에서 아래로 순서대로 실행하면 됩니다.
