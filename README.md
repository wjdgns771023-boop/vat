# VAT Summary App (Streamlit)

CSV 업로드 → 기간 선택 → 부가가치세(VAT) 요약을 제공하는 간단한 스트림릿 앱입니다.

## 로컬 실행
```bash
pip install -r requirements.txt
streamlit run app_vat_streamlit.py
```

## CSV 포맷
필수 컬럼(소문자): `date, type, category, amount, tax_rate`  
- `date`: YYYY-MM-DD  
- `type`: sale | purchase  
- `category`: taxable | zero | exempt  
- `amount`: 정수 (총액 또는 공급가; 앱에서 선택)  
- `tax_rate`: 과세건 세율 (예: 0.1)

샘플: [`vat_sample.csv`](vat_sample.csv)

## Streamlit Community Cloud 배포
1. 이 저장소를 GitHub에 올립니다(또는 Fork).
2. https://streamlit.io/cloud 에서 로그인 → **New app**.
3. Repository/Branch 선택 후 **Main file path**에 `app_vat_streamlit.py` 지정.
4. **Deploy** 버튼을 누르면 빌드 후 앱 URL이 발급됩니다.
   - 패키지 의존성은 `requirements.txt`를 사용합니다.
   - (선택) 앱이 **`streamlit_app.py`** 라면 파일 경로를 비워도 자동 인식됩니다.

## 주의
- 학습/보조용입니다. 실제 신고 전 최신 법령/불공제 항목 검토 필수.
- 대용량 CSV는 업로드 제한에 부딪힐 수 있습니다. 필요시 파일을 분할하거나 요약 전처리를 권장합니다.
