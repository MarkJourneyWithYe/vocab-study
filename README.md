# 영단어 마스터 — 수능·토익·공무원·내신

각 시험별 **필수 단어 100 + 숙어 50**, 총 **600개** 어휘 인터랙티브 학습기.

🌐 **Live**: https://vocab-study-eight.vercel.app

## 기능

- **🔊 발음** — Web Speech API. 단어/예문 각각 재생, 속도 0.5~1.4x, voice 선택
- **4가지 학습 모드**
  - 📋 **목록** — 검색·필터·외움 표시
  - 🃏 **카드** — 클릭/Space 뒤집기, 자동 발음, 키보드(← → P K)
  - 🧠 **복습 (SRS)** — SM-2 기반 망각곡선 간격 반복 (다시/어려움/좋음/쉬움 4단계)
  - 📝 **퀴즈** — 4지선다 10문항, 오답 리뷰
- **🎨 시험별 색상 테마** — 수능 Indigo · 토익 Orange · 공무원 Grape · 내신 Teal
- **📊 학습 분포** — 신규 / 학습 중 / 정착 시각화
- **💾 자동 저장** — localStorage(외움 표시, SRS 일정, 설정 모두 영구 보존)
- **📱 반응형 + 🌙 다크모드 + 🖨 인쇄용 스타일**

## SRS 알고리즘

- 카드별 상태: `ease(2.5±)`, `interval(일)`, `due`, `level(0–5)`
- 등급별 다음 간격:
  - **다시** → 1분 (세션 끝에 재등장), `ease −0.2`, lapse+1
  - **어려움** → `interval × 1.2`, `ease −0.15`
  - **좋음** → `interval × ease`
  - **쉬움** → `interval × ease × 1.3`, `ease +0.15`, level+2
- 일일 신규 한도 0–40장 (설정 가능, 기본 10장)
- 상단 🧠 카운터에 오늘 복습할 카드 수 실시간 표시

## 디자인

Pretendard Variable + JetBrains Mono · 크림 #FAF7F2 · [Open Color](https://yeun.github.io/open-color/) 팔레트

## 빌드

```bash
# 1. 마스터 MD에서 카테고리/퀴즈/JSON 생성
python3 build_vocab_pack.py

# 2. JSON을 HTML 템플릿에 임베드
python3 build_vocab_html.py
cp ../vocab_pack/vocab_app.html index.html
```

소스: `~/필수영단어_숙어_정리.md` (마스터 마크다운, 600 entries)

## 배포

`git push` → Vercel 자동 production 배포 (~45초)
