# VAT Form App (Streamlit)
클릭 입력 방식으로 매출/매입/공제 금액을 넣으면 **즉시 부가가치세(VAT) 예상 납부·환급세액**을 계산해 주는 스트림릿 앱입니다.
> 학습/보조용입니다. 실제 신고 전 최신 법령·불공제 항목·한도 등을 반드시 확인하세요.

## 로컬 실행
```bash
pip install -r requirements.txt
streamlit run app_vat_form.py
```

## 화면 구성
- 사이드바: 기본 세율(과세건), 금액 기준(총액/공급가)
- 매출자료: 세금계산서 / 신용카드·현금영수증 / 현금매출
- 매입자료(공제가능): 증빙별 금액 + 공제가능 체크
- 공제세액(추가): 의제매입 공제(매입가액·공제율), 기타 공제 합계
- 요약: ①매출세액 − ②매입세액(공제) − ③추가공제

## Streamlit Community Cloud 배포
1. 이 저장소를 GitHub에 올립니다.
2. https://streamlit.io/cloud 접속 → **New app**.
3. Repository/Branch 선택 후 **Main file path**에 `app_vat_form.py` 입력.
4. **Deploy** 클릭 → 앱 URL이 발급됩니다.
   - 의존성은 `requirements.txt`로 자동 설치됩니다.

## 폴더 구조
```
.
├─ app_vat_form.py       # 메인 앱(폼 입력형)
├─ requirements.txt
└─ README.md
```
