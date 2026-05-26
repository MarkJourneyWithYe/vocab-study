# 시험별 필수 어휘 학습기

수능 · 토익 · 공무원 · 내신 — 각 시험별 **단어 100 + 숙어 50**, 총 600개 어휘 인터랙티브 학습기.

🌐 **Live**: https://vocab-study.vercel.app

## 기능

- **발음**: Web Speech API (브라우저 내장 TTS), 속도 조절 0.5x–1.5x
- **5가지 학습 모드**
  - 목록 — 발음·외움 표시·즐겨찾기
  - 플래시카드 — 클릭으로 뒤집기, 자동 발음, 키보드(←→ Space Enter)
  - 퀴즈 — 4지선다, 영→한 / 한→영 양방향
  - 받아쓰기 — 뜻 보고 영어 입력 / 듣고 영어 입력
  - 시험지 — A4 인쇄용 시험지 + 정답표 생성
- **진척 저장**: localStorage (외움 표시·즐겨찾기·설정)
- **검색**: 영어/한국어 양쪽
- **모바일 반응형**

## 디자인

Pretendard + 크림 #FAF7F2 베이스. 시험별 액센트 컬러:
- 수능 #1F6FEB / 토익 #2DA44E / 공무원 #BF8700 / 내신 #8250DF

## 빌드

```bash
python3 build_vocab_html.py    # vocab_study.html 생성 (output/)
cp ../output/vocab_study.html index.html
```

데이터는 `build_vocab.py`의 8개 Python 리스트로 관리.

## 배포

`git push` 시 Vercel 자동 production 배포.
