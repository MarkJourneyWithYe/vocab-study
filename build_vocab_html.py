"""Build interactive vocab HTML.

Modes: 목록 · 플래시카드 · 퀴즈 (방향 토글) · 받아쓰기 · 시험지 (인쇄).
"""
import json
import runpy

mod = runpy.run_path("/Users/pyunhanga/output/build_vocab.py", run_name="vocab_data")

DATA = {
    "suneung":  {"label": "수능",   "color": "#1F6FEB", "words": mod["수능_단어"],   "idioms": mod["수능_숙어"]},
    "toeic":    {"label": "토익",   "color": "#2DA44E", "words": mod["토익_단어"],   "idioms": mod["토익_숙어"]},
    "gongmuwon":{"label": "공무원", "color": "#BF8700", "words": mod["공무원_단어"], "idioms": mod["공무원_숙어"]},
    "naesin":   {"label": "내신",   "color": "#8250DF", "words": mod["내신_단어"],   "idioms": mod["내신_숙어"]},
}

js_data = {
    k: {
        "label": v["label"],
        "color": v["color"],
        "words":  [[e, k_, ex] for (e, k_, ex) in v["words"]],
        "idioms": [[e, k_, ex] for (e, k_, ex) in v["idioms"]],
    }
    for k, v in DATA.items()
}
data_json = json.dumps(js_data, ensure_ascii=False)

HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>시험별 필수 어휘·숙어 학습기</title>
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css" rel="stylesheet">
<style>
  :root {
    --bg: #FAF7F2;
    --card: #FFFFFF;
    --ink: #1F2328;
    --muted: #656D76;
    --line: #E6E4DF;
    --shadow: 0 1px 2px rgba(0,0,0,.04), 0 8px 24px rgba(0,0,0,.06);
    --radius: 14px;
    --accent: #1F6FEB;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; }
  body {
    font-family: 'Pretendard Variable', Pretendard, -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
    background: var(--bg);
    color: var(--ink);
    min-height: 100vh;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
  }
  .app {
    max-width: 1100px;
    margin: 0 auto;
    padding: 24px 20px 80px;
  }
  header.top {
    display: flex; align-items: center; justify-content: space-between;
    gap: 16px; margin-bottom: 18px;
  }
  .title {
    font-size: 22px; font-weight: 800; letter-spacing: -0.02em;
    display: flex; align-items: center; gap: 10px;
  }
  .title .dot {
    width: 10px; height: 10px; border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 0 4px color-mix(in srgb, var(--accent) 18%, transparent);
    transition: background .25s, box-shadow .25s;
  }
  .stats {
    font-size: 13px; color: var(--muted);
    font-variant-numeric: tabular-nums;
  }
  .stats b { color: var(--ink); font-weight: 700; }

  .tabs {
    display: flex; flex-wrap: wrap; gap: 8px;
    background: var(--card); padding: 8px;
    border-radius: 12px; border: 1px solid var(--line);
    margin-bottom: 14px;
  }
  .tab {
    flex: 1; min-width: 90px;
    padding: 10px 14px;
    border: none; border-radius: 8px; background: transparent;
    font-family: inherit; font-size: 14px; font-weight: 600;
    color: var(--muted); cursor: pointer;
    transition: all .15s ease;
    display: flex; align-items: center; justify-content: center; gap: 6px;
  }
  .tab:hover { background: var(--bg); color: var(--ink); }
  .tab.active { color: #fff; background: var(--accent); }
  .tab .count { font-size: 11px; opacity: .85; font-weight: 500; }

  .toolbar {
    display: flex; gap: 10px; flex-wrap: wrap;
    margin-bottom: 14px; align-items: center;
  }
  .seg {
    display: inline-flex; background: var(--card);
    border: 1px solid var(--line); border-radius: 10px; padding: 4px;
  }
  .seg button {
    border: none; background: transparent; padding: 7px 14px;
    font-family: inherit; font-size: 13px; font-weight: 600;
    color: var(--muted); cursor: pointer; border-radius: 7px;
    transition: all .15s;
  }
  .seg button.on { background: var(--ink); color: #fff; }
  .search {
    flex: 1; min-width: 180px;
    padding: 9px 14px;
    border-radius: 10px; border: 1px solid var(--line);
    background: var(--card); font-family: inherit; font-size: 14px;
    color: var(--ink); outline: none;
    transition: border-color .15s, box-shadow .15s;
  }
  .search:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 16%, transparent);
  }
  .voice {
    display: flex; align-items: center; gap: 8px;
    background: var(--card); border: 1px solid var(--line);
    border-radius: 10px; padding: 4px 12px 4px 10px; font-size: 13px;
  }
  .voice label { color: var(--muted); }
  .voice input[type=range] { width: 90px; }

  .subbar {
    display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 14px;
    align-items: center; font-size: 13px;
  }
  .subbar label { color: var(--muted); margin-right: 4px; }
  .subbar select, .subbar input[type=number], .subbar input[type=text] {
    padding: 7px 10px; border-radius: 8px; border: 1px solid var(--line);
    background: var(--card); font-family: inherit; font-size: 13px;
    color: var(--ink); outline: none;
  }
  .subbar input[type=number] { width: 70px; }
  .subbar input[type=text] { min-width: 130px; }
  .subbar .ck { display: inline-flex; align-items: center; gap: 6px; color: var(--muted); }

  .panel {
    background: var(--card); border: 1px solid var(--line);
    border-radius: var(--radius); box-shadow: var(--shadow);
    overflow: hidden;
  }

  /* LIST */
  .list { display: flex; flex-direction: column; }
  .row {
    display: grid;
    grid-template-columns: 44px 1.1fr 1fr 1.6fr 110px;
    gap: 14px; padding: 12px 16px;
    align-items: center;
    border-top: 1px solid var(--line);
    transition: background .15s;
  }
  .row:first-child { border-top: none; }
  .row:hover { background: #FCFBF8; }
  .row.head {
    font-size: 12px; font-weight: 700; color: var(--muted);
    text-transform: uppercase; letter-spacing: 0.04em;
    background: #FAF8F3; padding: 10px 16px; border-top: none;
  }
  .row .no {
    font-variant-numeric: tabular-nums;
    color: var(--muted); font-size: 13px; text-align: right;
  }
  .row .eng { font-weight: 700; font-size: 15px; }
  .row .kor { font-size: 14px; color: var(--ink); }
  .row .ex { font-size: 13px; color: #4B5563; font-style: italic; line-height: 1.5; }
  .row .actions { display: flex; gap: 6px; justify-content: flex-end; }
  .iconbtn {
    width: 32px; height: 32px;
    border: 1px solid var(--line); background: var(--card);
    border-radius: 8px; cursor: pointer;
    display: inline-flex; align-items: center; justify-content: center;
    color: var(--muted); transition: all .15s;
    padding: 0;
  }
  .iconbtn:hover { color: var(--accent); border-color: var(--accent); background: color-mix(in srgb, var(--accent) 8%, white); }
  .iconbtn.known { background: #DCFCE7; border-color: #86EFAC; color: #166534; }
  .iconbtn.star.on { color: #D97706; border-color: #FBBF24; background: #FEF3C7; }
  .iconbtn svg { width: 16px; height: 16px; }
  .row.hidden { display: none; }
  .row.known { background: #F0FDF4; }
  .row.known:hover { background: #DCFCE7; }

  /* FLASHCARD */
  .flash-wrap {
    padding: 32px 24px 24px;
    display: flex; flex-direction: column; align-items: center;
    min-height: 480px;
  }
  .flash-counter {
    font-size: 13px; color: var(--muted);
    font-variant-numeric: tabular-nums;
    margin-bottom: 18px;
  }
  .flashcard {
    width: 100%; max-width: 560px;
    aspect-ratio: 4 / 2.6;
    perspective: 1200px; cursor: pointer;
  }
  .flash-inner {
    position: relative; width: 100%; height: 100%;
    transform-style: preserve-3d;
    transition: transform .55s cubic-bezier(.4,0,.2,1);
  }
  .flash-inner.flipped { transform: rotateY(180deg); }
  .flash-face {
    position: absolute; inset: 0;
    backface-visibility: hidden;
    border-radius: 18px;
    display: flex; flex-direction: column; justify-content: center; align-items: center;
    padding: 28px; text-align: center;
    border: 2px solid var(--line);
    background: #FFFFFF;
  }
  .flash-front { background: linear-gradient(160deg, #FFFFFF, #FAF8F3); }
  .flash-back  { transform: rotateY(180deg); background: linear-gradient(160deg, #FFFFFF, #F4F7FB); }
  .flash-eng {
    font-size: clamp(28px, 5vw, 44px);
    font-weight: 800; letter-spacing: -0.02em; margin-bottom: 8px;
  }
  .flash-hint { font-size: 12px; color: var(--muted); }
  .flash-kor {
    font-size: clamp(22px, 4vw, 32px);
    font-weight: 700; margin-bottom: 16px;
  }
  .flash-ex { font-size: 15px; color: #4B5563; font-style: italic; max-width: 480px; line-height: 1.55; }
  .flash-nav {
    display: flex; gap: 12px; margin-top: 22px; align-items: center;
    flex-wrap: wrap; justify-content: center;
  }
  .navbtn {
    padding: 10px 18px; border: 1px solid var(--line);
    background: var(--card); border-radius: 10px; font-family: inherit;
    font-size: 14px; font-weight: 600; color: var(--ink); cursor: pointer;
    transition: all .15s;
    display: inline-flex; align-items: center; gap: 6px;
  }
  .navbtn:hover { border-color: var(--accent); color: var(--accent); }
  .navbtn.primary { background: var(--accent); border-color: var(--accent); color: #fff; }
  .navbtn.primary:hover { color: #fff; opacity: .9; }
  .navbtn.success { background: #16A34A; border-color: #16A34A; color: #fff; }
  .navbtn svg { width: 14px; height: 14px; }

  /* QUIZ */
  .quiz-wrap {
    padding: 28px 24px; display: flex; flex-direction: column;
    align-items: center; min-height: 480px;
  }
  .quiz-bar {
    width: 100%; max-width: 600px;
    display: flex; justify-content: space-between; font-size: 13px;
    color: var(--muted); margin-bottom: 12px; font-variant-numeric: tabular-nums;
  }
  .quiz-progress {
    width: 100%; max-width: 600px; height: 6px;
    background: var(--line); border-radius: 999px; overflow: hidden;
    margin-bottom: 24px;
  }
  .quiz-progress > div {
    height: 100%; background: var(--accent);
    transition: width .35s ease, background .25s;
  }
  .quiz-question {
    font-size: 12px; font-weight: 700; color: var(--muted);
    text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 10px;
  }
  .quiz-prompt {
    font-size: clamp(26px, 4.5vw, 38px);
    font-weight: 800; letter-spacing: -0.02em; margin-bottom: 26px;
    display: flex; align-items: center; gap: 12px;
    text-align: center; flex-wrap: wrap; justify-content: center;
  }
  .quiz-options {
    display: grid; grid-template-columns: 1fr 1fr; gap: 10px;
    width: 100%; max-width: 600px;
  }
  .quiz-opt {
    padding: 14px 16px; background: var(--card);
    border: 1.5px solid var(--line); border-radius: 12px;
    cursor: pointer; font-family: inherit; font-size: 15px; text-align: left;
    transition: all .15s; line-height: 1.4;
    display: flex; align-items: center; gap: 10px;
  }
  .quiz-opt .lbl {
    width: 24px; height: 24px; border-radius: 50%;
    background: var(--bg); color: var(--muted);
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 12px; font-weight: 700; flex-shrink: 0;
  }
  .quiz-opt:hover { border-color: var(--accent); background: color-mix(in srgb, var(--accent) 5%, white); }
  .quiz-opt.correct { background: #DCFCE7; border-color: #16A34A; color: #14532D; }
  .quiz-opt.correct .lbl { background: #16A34A; color: #fff; }
  .quiz-opt.wrong { background: #FEE2E2; border-color: #DC2626; color: #7F1D1D; }
  .quiz-opt.wrong .lbl { background: #DC2626; color: #fff; }
  .quiz-opt:disabled { cursor: default; }
  .quiz-feedback {
    margin-top: 20px; min-height: 24px;
    font-size: 14px; color: var(--muted);
    max-width: 600px; width: 100%; text-align: center;
    font-style: italic;
  }
  .quiz-feedback b { font-style: normal; color: var(--ink); }

  /* TYPING */
  .type-wrap {
    padding: 32px 24px; display: flex; flex-direction: column;
    align-items: center; min-height: 480px;
  }
  .type-card {
    background: linear-gradient(160deg, #FFFFFF, #FAF8F3);
    border: 2px solid var(--line); border-radius: 18px;
    padding: 28px 24px; width: 100%; max-width: 560px;
    text-align: center;
  }
  .type-prompt {
    font-size: clamp(24px, 4.5vw, 36px);
    font-weight: 800; letter-spacing: -0.02em; margin-bottom: 8px;
    color: var(--ink);
  }
  .type-prompt.audio {
    font-size: 16px; color: var(--muted); font-weight: 600;
  }
  .type-hint-ex { font-size: 13px; color: var(--muted); font-style: italic; margin-bottom: 18px; }
  .type-input {
    width: 100%; max-width: 460px; margin: 16px auto 8px;
    padding: 14px 18px; font-family: 'JetBrains Mono', ui-monospace, monospace;
    font-size: 20px; text-align: center;
    border: 2px solid var(--line); border-radius: 12px;
    background: #FFFFFF; outline: none;
    color: var(--ink);
    transition: border-color .15s, box-shadow .15s;
  }
  .type-input:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 16%, transparent);
  }
  .type-input.correct { border-color: #16A34A; background: #F0FDF4; }
  .type-input.wrong   { border-color: #DC2626; background: #FEF2F2; }
  .type-feedback {
    margin-top: 14px; min-height: 60px; font-size: 14px;
    color: var(--muted); line-height: 1.55;
  }
  .type-feedback .ans { font-weight: 800; color: var(--ink); font-size: 18px; }
  .type-feedback .ex { font-style: italic; display: block; margin-top: 4px; color: #4B5563; }
  .type-feedback.ok    { color: #166534; }
  .type-feedback.bad   { color: #991B1B; }

  /* PRINT SHEET */
  .print-wrap { padding: 0; }
  .print-controls {
    padding: 18px 20px;
    background: #FAF8F3; border-bottom: 1px solid var(--line);
    display: flex; gap: 12px; flex-wrap: wrap; align-items: center;
  }
  .print-preview {
    padding: 0; background: #EFEDE8;
    max-height: 75vh; overflow-y: auto;
  }
  .sheet {
    background: #FFFFFF; margin: 18px auto; padding: 48px 44px;
    width: 210mm; min-height: 297mm;
    box-shadow: 0 2px 8px rgba(0,0,0,.08);
    color: #111; font-size: 12pt;
  }
  .sheet h1 {
    margin: 0 0 6px; font-size: 18pt; letter-spacing: -0.02em;
    border-bottom: 2px solid #111; padding-bottom: 10px;
  }
  .sheet .meta {
    display: flex; justify-content: space-between; gap: 16px;
    margin: 12px 0 22px; font-size: 11pt;
  }
  .sheet .meta span { display: inline-block; }
  .sheet .meta b { display: inline-block; width: 60px; }
  .sheet .meta u { display: inline-block; min-width: 120px; text-decoration: none; border-bottom: 1px solid #111; }
  .sheet table {
    width: 100%; border-collapse: collapse;
    font-size: 11pt;
  }
  .sheet td {
    padding: 8px 6px; border-bottom: 1px dashed #999;
    vertical-align: top;
  }
  .sheet td.no { width: 28px; color: #666; text-align: right; padding-right: 10px; }
  .sheet td.q { font-weight: 600; }
  .sheet td.blank {
    width: 40%; min-width: 120px;
  }
  .sheet td.blank .line {
    display: inline-block; min-width: 100%; min-height: 18px;
    border-bottom: 1px solid #333;
  }
  .sheet.answers h1 { color: #B91C1C; border-color: #B91C1C; }
  .sheet.answers td.ans { color: #B91C1C; font-weight: 700; }
  .sheet .ex-mini { font-size: 9pt; color: #666; font-style: italic; display: block; margin-top: 2px; }

  .empty {
    padding: 60px 20px; text-align: center; color: var(--muted);
    font-size: 14px;
  }

  @media (max-width: 720px) {
    .row { grid-template-columns: 32px 1fr 92px; }
    .row .kor { grid-column: 2; }
    .row .ex { display: none; }
    .row.head .ex { display: none; }
    .row.head { grid-template-columns: 32px 1fr 92px; }
    .quiz-options { grid-template-columns: 1fr; }
    .voice { display: none; }
    .sheet { width: 100%; padding: 24px 16px; }
  }

  @media print {
    body { background: #fff; }
    .app > header, .tabs, .toolbar, .subbar, .print-controls { display: none !important; }
    .panel { border: none; box-shadow: none; }
    .print-preview { max-height: none; overflow: visible; padding: 0; background: #fff; }
    .sheet { box-shadow: none; margin: 0; page-break-after: always; }
    .sheet:last-child { page-break-after: auto; }
  }
</style>
</head>
<body>
<div class="app">
  <header class="top">
    <div class="title"><span class="dot" id="accentDot"></span><span>시험별 필수 어휘 학습기</span></div>
    <div class="stats" id="stats">—</div>
  </header>

  <div class="tabs" id="examTabs"></div>

  <div class="toolbar">
    <div class="seg" id="kindSeg">
      <button data-kind="words" class="on">단어</button>
      <button data-kind="idioms">숙어</button>
    </div>
    <div class="seg" id="modeSeg">
      <button data-mode="list" class="on">목록</button>
      <button data-mode="flash">플래시카드</button>
      <button data-mode="quiz">퀴즈</button>
      <button data-mode="typing">받아쓰기</button>
      <button data-mode="print">시험지</button>
    </div>
    <input id="search" class="search" type="search" placeholder="단어/뜻 검색…" autocomplete="off">
    <div class="voice">
      <label>속도</label>
      <input id="rate" type="range" min="0.5" max="1.5" step="0.05" value="0.95">
    </div>
  </div>

  <div id="subbar"></div>

  <main class="panel" id="panel"></main>
</div>

<script>
const DATA = __DATA__;

const SVG = {
  speaker: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>',
  check:   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>',
  star:    '<svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>',
  prev:    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>',
  next:    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>',
  shuffle: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 3 21 3 21 8"></polyline><line x1="4" y1="20" x2="21" y2="3"></line><polyline points="21 16 21 21 16 21"></polyline><line x1="15" y1="15" x2="21" y2="21"></line><line x1="4" y1="4" x2="9" y2="9"></line></svg>',
  print:   '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 6 2 18 2 18 9"></polyline><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path><rect x="6" y="14" width="12" height="8"></rect></svg>',
};

const state = {
  exam: localStorage.getItem('exam') || 'suneung',
  kind: localStorage.getItem('kind') || 'words',
  mode: localStorage.getItem('mode') || 'list',
  search: '',
  rate: parseFloat(localStorage.getItem('rate') || '0.95'),

  flashIdx: 0,
  flashFlipped: false,

  quizDir: localStorage.getItem('quizDir') || 'en2ko',  // en2ko | ko2en
  quizIdx: 0,
  quizScore: 0,
  quizPool: [],
  quizCurrent: null,
  quizAnswered: false,

  typeSub: localStorage.getItem('typeSub') || 'meaning', // meaning | audio
  typeIdx: 0,
  typeScore: 0,
  typePool: [],
  typeAnswered: false,

  printCount: parseInt(localStorage.getItem('printCount') || '25'),
  printDir: localStorage.getItem('printDir') || 'en2ko',  // blank Korean | blank English
  printWithAnswers: localStorage.getItem('printWithAnswers') !== '0',
  printTitle: localStorage.getItem('printTitle') || '',
  printSeed: 0,
};

const itemKey = (exam, kind, eng) => `${exam}.${kind}.${eng}`;
const status = JSON.parse(localStorage.getItem('vocab_status') || '{}');
const starred = JSON.parse(localStorage.getItem('vocab_starred') || '{}');
function saveStatus() { localStorage.setItem('vocab_status', JSON.stringify(status)); }
function saveStarred() { localStorage.setItem('vocab_starred', JSON.stringify(starred)); }

// TTS
let voices = [];
function loadVoices() { voices = speechSynthesis.getVoices(); }
if ('speechSynthesis' in window) {
  loadVoices();
  speechSynthesis.onvoiceschanged = loadVoices;
}
function pickVoice() {
  if (!voices.length) return null;
  const en = voices.filter(v => v.lang.startsWith('en'));
  if (!en.length) return null;
  const us = en.find(v => v.lang === 'en-US' && /female|samantha|google us english|jenny|aria/i.test(v.name));
  if (us) return us;
  return en.find(v => v.lang === 'en-US') || en[0];
}
function speak(text) {
  if (!('speechSynthesis' in window)) return;
  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  const v = pickVoice();
  if (v) u.voice = v;
  u.lang = 'en-US';
  u.rate = state.rate;
  u.pitch = 1.0;
  speechSynthesis.speak(u);
}

function currentItems() {
  return DATA[state.exam][state.kind].map(x => ({ eng: x[0], kor: x[1], ex: x[2] }));
}
function filtered() {
  const q = state.search.trim().toLowerCase();
  if (!q) return currentItems();
  return currentItems().filter(i =>
    i.eng.toLowerCase().includes(q) || i.kor.toLowerCase().includes(q)
  );
}
function setAccent() {
  document.documentElement.style.setProperty('--accent', DATA[state.exam].color);
}
function updateStats() {
  const items = currentItems();
  const total = items.length;
  const knownCount = items.filter(i => status[itemKey(state.exam, state.kind, i.eng)] === 'known').length;
  const pct = total ? Math.round(knownCount / total * 100) : 0;
  document.getElementById('stats').innerHTML =
    `<b>${DATA[state.exam].label}</b> ${state.kind === 'words' ? '단어' : '숙어'} · 외움 <b>${knownCount}</b>/${total} (${pct}%)`;
}

function renderTabs() {
  const tabs = document.getElementById('examTabs');
  tabs.innerHTML = '';
  Object.entries(DATA).forEach(([key, v]) => {
    const btn = document.createElement('button');
    btn.className = 'tab' + (key === state.exam ? ' active' : '');
    btn.innerHTML = `${v.label}<span class="count">${v.words.length + v.idioms.length}</span>`;
    if (key === state.exam) btn.style.background = v.color;
    btn.onclick = () => {
      state.exam = key; localStorage.setItem('exam', key);
      resetModeStates();
      render();
    };
    tabs.appendChild(btn);
  });
}
function resetModeStates() {
  state.flashIdx = 0; state.flashFlipped = false;
  state.quizIdx = 0; state.quizScore = 0; state.quizPool = []; state.quizCurrent = null;
  state.typeIdx = 0; state.typeScore = 0; state.typePool = []; state.typeAnswered = false;
}
function renderToolbar() {
  document.querySelectorAll('#kindSeg button').forEach(b => {
    b.classList.toggle('on', b.dataset.kind === state.kind);
    b.onclick = () => {
      state.kind = b.dataset.kind; localStorage.setItem('kind', state.kind);
      resetModeStates(); render();
    };
  });
  document.querySelectorAll('#modeSeg button').forEach(b => {
    b.classList.toggle('on', b.dataset.mode === state.mode);
    b.onclick = () => {
      state.mode = b.dataset.mode; localStorage.setItem('mode', state.mode);
      if (state.mode === 'quiz')   initQuiz();
      if (state.mode === 'typing') initType();
      render();
    };
  });
  const s = document.getElementById('search');
  s.value = state.search;
  s.oninput = (e) => { state.search = e.target.value; renderPanel(); };
  const rate = document.getElementById('rate');
  rate.value = state.rate;
  rate.oninput = (e) => { state.rate = parseFloat(e.target.value); localStorage.setItem('rate', state.rate); };
}

function renderSubbar() {
  const sb = document.getElementById('subbar');
  sb.innerHTML = '';
  if (state.mode === 'quiz') {
    sb.innerHTML = `<div class="subbar">
      <label>방향</label>
      <div class="seg" id="quizDirSeg">
        <button data-dir="en2ko" class="${state.quizDir==='en2ko'?'on':''}">영 → 한</button>
        <button data-dir="ko2en" class="${state.quizDir==='ko2en'?'on':''}">한 → 영</button>
      </div>
    </div>`;
    sb.querySelectorAll('#quizDirSeg button').forEach(b => {
      b.onclick = () => {
        state.quizDir = b.dataset.dir; localStorage.setItem('quizDir', state.quizDir);
        initQuiz(); render();
      };
    });
  } else if (state.mode === 'typing') {
    sb.innerHTML = `<div class="subbar">
      <label>방식</label>
      <div class="seg" id="typeSubSeg">
        <button data-sub="meaning" class="${state.typeSub==='meaning'?'on':''}">뜻 보고 입력</button>
        <button data-sub="audio"   class="${state.typeSub==='audio'  ?'on':''}">듣고 입력</button>
      </div>
    </div>`;
    sb.querySelectorAll('#typeSubSeg button').forEach(b => {
      b.onclick = () => {
        state.typeSub = b.dataset.sub; localStorage.setItem('typeSub', state.typeSub);
        initType(); render();
      };
    });
  } else if (state.mode === 'print') {
    const items = currentItems();
    sb.innerHTML = `<div class="subbar">
      <label>제목</label>
      <input id="prTitle" type="text" placeholder="${DATA[state.exam].label} ${state.kind==='words'?'단어':'숙어'} 시험" value="${escAttr(state.printTitle)}">
      <label>문항</label>
      <input id="prCount" type="number" min="5" max="${items.length}" step="5" value="${state.printCount}">
      <label>방향</label>
      <div class="seg" id="prDirSeg">
        <button data-dir="en2ko" class="${state.printDir==='en2ko'?'on':''}">영→한 빈칸</button>
        <button data-dir="ko2en" class="${state.printDir==='ko2en'?'on':''}">한→영 빈칸</button>
      </div>
      <label class="ck"><input id="prAns" type="checkbox" ${state.printWithAnswers?'checked':''}> 정답표 포함</label>
      <button class="navbtn" id="prShuffle">${SVG.shuffle} 새 문제</button>
      <button class="navbtn primary" id="prPrint">${SVG.print} 인쇄</button>
    </div>`;
    document.getElementById('prTitle').oninput = (e) => { state.printTitle = e.target.value; localStorage.setItem('printTitle', state.printTitle); };
    document.getElementById('prCount').oninput = (e) => {
      state.printCount = Math.max(5, Math.min(items.length, parseInt(e.target.value)||25));
      localStorage.setItem('printCount', state.printCount); renderPanel();
    };
    sb.querySelectorAll('#prDirSeg button').forEach(b => {
      b.onclick = () => { state.printDir = b.dataset.dir; localStorage.setItem('printDir', state.printDir); renderSubbar(); renderPanel(); };
    });
    document.getElementById('prAns').onchange = (e) => {
      state.printWithAnswers = e.target.checked;
      localStorage.setItem('printWithAnswers', state.printWithAnswers ? '1' : '0');
      renderPanel();
    };
    document.getElementById('prShuffle').onclick = () => { state.printSeed = Math.random(); renderPanel(); };
    document.getElementById('prPrint').onclick = () => window.print();
  }
}

function renderPanel() {
  const p = document.getElementById('panel');
  if (state.mode === 'list')   p.innerHTML = listHTML();
  if (state.mode === 'flash')  p.innerHTML = flashHTML();
  if (state.mode === 'quiz')   p.innerHTML = quizHTML();
  if (state.mode === 'typing') p.innerHTML = typeHTML();
  if (state.mode === 'print')  p.innerHTML = printHTML();
  bindPanelEvents();
  updateStats();
}

function listHTML() {
  const items = filtered();
  if (!items.length) return '<div class="empty">검색 결과가 없습니다.</div>';
  let html = `<div class="list">
    <div class="row head">
      <div class="no">#</div>
      <div>English</div>
      <div>Korean</div>
      <div class="ex-head">Example</div>
      <div style="text-align:right">Action</div>
    </div>`;
  items.forEach((it, i) => {
    const k = itemKey(state.exam, state.kind, it.eng);
    const isKnown = status[k] === 'known';
    const isStar = !!starred[k];
    html += `<div class="row ${isKnown ? 'known' : ''}" data-eng="${escAttr(it.eng)}">
      <div class="no">${i + 1}</div>
      <div class="eng">${escHtml(it.eng)}</div>
      <div class="kor">${escHtml(it.kor)}</div>
      <div class="ex">${escHtml(it.ex)}</div>
      <div class="actions">
        <button class="iconbtn" data-act="speak" title="발음 듣기">${SVG.speaker}</button>
        <button class="iconbtn star ${isStar ? 'on' : ''}" data-act="star" title="즐겨찾기">${SVG.star}</button>
        <button class="iconbtn ${isKnown ? 'known' : ''}" data-act="known" title="외움">${SVG.check}</button>
      </div>
    </div>`;
  });
  html += `</div>`;
  return html;
}

function flashHTML() {
  const items = filtered();
  if (!items.length) return '<div class="empty">표시할 항목이 없습니다.</div>';
  const idx = Math.min(state.flashIdx, items.length - 1);
  const it = items[idx];
  const k = itemKey(state.exam, state.kind, it.eng);
  const isKnown = status[k] === 'known';
  return `<div class="flash-wrap">
    <div class="flash-counter">${idx + 1} / ${items.length} ${isKnown ? '· ✓ 외움' : ''}</div>
    <div class="flashcard" id="flashcard">
      <div class="flash-inner ${state.flashFlipped ? 'flipped' : ''}">
        <div class="flash-face flash-front">
          <div class="flash-eng">${escHtml(it.eng)}</div>
          <div class="flash-hint">탭하여 뜻 보기 · 스페이스로 발음</div>
        </div>
        <div class="flash-face flash-back">
          <div class="flash-kor">${escHtml(it.kor)}</div>
          <div class="flash-ex">"${escHtml(it.ex)}"</div>
        </div>
      </div>
    </div>
    <div class="flash-nav">
      <button class="navbtn" data-act="prev">${SVG.prev} 이전</button>
      <button class="navbtn" data-act="speak">${SVG.speaker} 발음</button>
      <button class="navbtn" data-act="shuffle">${SVG.shuffle} 셔플</button>
      <button class="navbtn ${isKnown ? 'success' : ''}" data-act="known">${SVG.check} ${isKnown ? '외움' : '외움 표시'}</button>
      <button class="navbtn primary" data-act="next">다음 ${SVG.next}</button>
    </div>
  </div>`;
}

// QUIZ
function initQuiz() {
  state.quizPool = shuffle(currentItems().slice());
  state.quizIdx = 0; state.quizScore = 0;
  nextQuiz();
}
function nextQuiz() {
  if (!state.quizPool.length) { state.quizCurrent = null; return; }
  const items = currentItems();
  const target = state.quizPool[state.quizIdx];
  const distractors = shuffle(items.filter(x => x.eng !== target.eng)).slice(0, 3);
  state.quizCurrent = { target, options: shuffle([target, ...distractors]) };
  state.quizAnswered = false;
}
function quizHTML() {
  if (!state.quizPool.length) initQuiz();
  if (!state.quizCurrent) return '<div class="empty">표시할 항목이 없습니다.</div>';
  const { target, options } = state.quizCurrent;
  const total = state.quizPool.length;
  const cur = state.quizIdx + 1;
  const pct = Math.round(((cur - 1) / total) * 100);
  const isEn2Ko = state.quizDir === 'en2ko';

  const promptText = isEn2Ko ? target.eng : target.kor;
  const questionLabel = isEn2Ko ? '다음 단어의 뜻은?' : '다음 뜻에 해당하는 영어는?';
  const speakBtn = isEn2Ko ? `<button class="iconbtn" data-act="speak" title="발음">${SVG.speaker}</button>` : '';

  let optHtml = '';
  options.forEach((o, i) => {
    const optText = isEn2Ko ? o.kor : o.eng;
    optHtml += `<button class="quiz-opt" data-eng="${escAttr(o.eng)}">
      <span class="lbl">${String.fromCharCode(65 + i)}</span>
      <span>${escHtml(optText)}</span>
    </button>`;
  });

  return `<div class="quiz-wrap">
    <div class="quiz-bar">
      <span>${cur} / ${total}</span>
      <span>점수 <b>${state.quizScore}</b></span>
    </div>
    <div class="quiz-progress"><div style="width:${pct}%"></div></div>
    <div class="quiz-question">${questionLabel}</div>
    <div class="quiz-prompt">${escHtml(promptText)} ${speakBtn}</div>
    <div class="quiz-options" id="quizOpts">${optHtml}</div>
    <div class="quiz-feedback" id="quizFeedback"></div>
  </div>`;
}

// TYPING
function initType() {
  state.typePool = shuffle(currentItems().slice());
  state.typeIdx = 0; state.typeScore = 0; state.typeAnswered = false;
}
function typeCurrent() { return state.typePool[state.typeIdx]; }
function typeHTML() {
  if (!state.typePool.length) initType();
  const it = typeCurrent();
  if (!it) return '<div class="empty">표시할 항목이 없습니다.</div>';
  const total = state.typePool.length;
  const cur = state.typeIdx + 1;
  const pct = Math.round(((cur - 1) / total) * 100);

  const promptHTML = state.typeSub === 'audio'
    ? `<div class="type-prompt audio">🔊 들은 단어를 입력하세요</div>
       <button class="navbtn" id="typeReplay">${SVG.speaker} 다시 듣기</button>`
    : `<div class="type-prompt">${escHtml(it.kor)}</div>`;

  return `<div class="type-wrap">
    <div class="quiz-bar" style="max-width:560px;">
      <span>${cur} / ${total}</span>
      <span>점수 <b>${state.typeScore}</b></span>
    </div>
    <div class="quiz-progress" style="max-width:560px;"><div style="width:${pct}%"></div></div>
    <div class="type-card">
      ${promptHTML}
      <input id="typeInput" class="type-input" type="text" autocomplete="off" autocapitalize="off"
             spellcheck="false" placeholder="영어로 입력 후 Enter" lang="en">
      <div id="typeFb" class="type-feedback"></div>
    </div>
    <div class="flash-nav">
      <button class="navbtn" data-act="skip">건너뛰기 ${SVG.next}</button>
      <button class="navbtn primary" id="typeSubmit">${SVG.check} 확인</button>
    </div>
  </div>`;
}

// PRINT SHEET
function pickPrintSet() {
  // Deterministic per printSeed/exam/kind/count for stable view until shuffle
  const items = currentItems().slice();
  // simple seeded shuffle using printSeed
  const seed = state.printSeed || 0.13;
  function rng(s) { let t = Math.floor((s*1e9 + 1) ^ 0x6D2B79F5); return function() {
    t |= 0; t = t + 0x6D2B79F5 | 0;
    let r = Math.imul(t ^ t >>> 15, 1 | t);
    r = r + Math.imul(r ^ r >>> 7, 61 | r) ^ r;
    return ((r ^ r >>> 14) >>> 0) / 4294967296;
  };}
  const rnd = rng(seed + state.exam.length * 0.07 + (state.kind === 'words' ? 1 : 3));
  for (let i = items.length - 1; i > 0; i--) {
    const j = Math.floor(rnd() * (i + 1));
    [items[i], items[j]] = [items[j], items[i]];
  }
  return items.slice(0, Math.min(state.printCount, items.length));
}
function printHTML() {
  const items = pickPrintSet();
  const title = state.printTitle || `${DATA[state.exam].label} ${state.kind === 'words' ? '단어' : '숙어'} 시험`;
  const isEn2Ko = state.printDir === 'en2ko';
  const today = new Date();
  const dateStr = `${today.getFullYear()}.${String(today.getMonth()+1).padStart(2,'0')}.${String(today.getDate()).padStart(2,'0')}`;

  let qRows = '';
  items.forEach((it, i) => {
    if (isEn2Ko) {
      qRows += `<tr>
        <td class="no">${i+1}.</td>
        <td class="q">${escHtml(it.eng)}<span class="ex-mini">${escHtml(it.ex)}</span></td>
        <td class="blank"><span class="line">&nbsp;</span></td>
      </tr>`;
    } else {
      qRows += `<tr>
        <td class="no">${i+1}.</td>
        <td class="q">${escHtml(it.kor)}</td>
        <td class="blank"><span class="line">&nbsp;</span></td>
      </tr>`;
    }
  });

  let ansRows = '';
  items.forEach((it, i) => {
    const ans = isEn2Ko ? it.kor : it.eng;
    ansRows += `<tr>
      <td class="no">${i+1}.</td>
      <td class="q">${escHtml(isEn2Ko ? it.eng : it.kor)}</td>
      <td class="ans">${escHtml(ans)}</td>
    </tr>`;
  });

  const answerSheet = state.printWithAnswers ? `
    <div class="sheet answers">
      <h1>정답 — ${escHtml(title)}</h1>
      <div class="meta">
        <span><b>날짜</b> ${dateStr}</span>
        <span><b>총 문항</b> ${items.length}문제</span>
      </div>
      <table>${ansRows}</table>
    </div>` : '';

  return `<div class="print-wrap">
    <div class="print-preview">
      <div class="sheet">
        <h1>${escHtml(title)}</h1>
        <div class="meta">
          <span><b>이름</b> <u>&nbsp;</u></span>
          <span><b>학번</b> <u>&nbsp;</u></span>
          <span><b>날짜</b> ${dateStr}</span>
          <span><b>점수</b> <u>&nbsp;</u> / ${items.length}</span>
        </div>
        <table>${qRows}</table>
      </div>
      ${answerSheet}
    </div>
  </div>`;
}

function bindPanelEvents() {
  if (state.mode === 'list') {
    document.querySelectorAll('.row[data-eng]').forEach(row => {
      const eng = row.dataset.eng;
      row.querySelectorAll('[data-act]').forEach(btn => {
        btn.onclick = (e) => {
          e.stopPropagation();
          const act = btn.dataset.act;
          if (act === 'speak') speak(eng);
          if (act === 'star') {
            const k = itemKey(state.exam, state.kind, eng);
            starred[k] = !starred[k]; saveStarred();
            btn.classList.toggle('on', !!starred[k]);
          }
          if (act === 'known') {
            const k = itemKey(state.exam, state.kind, eng);
            status[k] = status[k] === 'known' ? null : 'known';
            saveStatus();
            renderPanel();
          }
        };
      });
      row.addEventListener('click', () => speak(eng));
    });
  }
  if (state.mode === 'flash') {
    const card = document.getElementById('flashcard');
    if (card) card.onclick = () => {
      state.flashFlipped = !state.flashFlipped;
      renderPanel();
      if (!state.flashFlipped) {
        const it = filtered()[Math.min(state.flashIdx, filtered().length-1)];
        if (it) speak(it.eng);
      }
    };
    document.querySelectorAll('.flash-nav [data-act]').forEach(b => {
      b.onclick = (e) => {
        e.stopPropagation();
        const items = filtered();
        const act = b.dataset.act;
        if (act === 'next') {
          state.flashIdx = (state.flashIdx + 1) % items.length;
          state.flashFlipped = false; renderPanel();
          const it = items[state.flashIdx]; if (it) setTimeout(() => speak(it.eng), 80);
        }
        if (act === 'prev') {
          state.flashIdx = (state.flashIdx - 1 + items.length) % items.length;
          state.flashFlipped = false; renderPanel();
          const it = items[state.flashIdx]; if (it) setTimeout(() => speak(it.eng), 80);
        }
        if (act === 'speak') { const it = items[state.flashIdx]; if (it) speak(it.eng); }
        if (act === 'shuffle') {
          state.flashIdx = Math.floor(Math.random() * items.length);
          state.flashFlipped = false; renderPanel();
        }
        if (act === 'known') {
          const it = items[state.flashIdx]; if (!it) return;
          const k = itemKey(state.exam, state.kind, it.eng);
          status[k] = status[k] === 'known' ? null : 'known';
          saveStatus(); renderPanel();
        }
      };
    });
  }
  if (state.mode === 'quiz') {
    if (state.quizCurrent && state.quizDir === 'en2ko') speak(state.quizCurrent.target.eng);
    document.querySelectorAll('.quiz-opt').forEach(btn => {
      btn.onclick = () => {
        if (state.quizAnswered) return;
        state.quizAnswered = true;
        const eng = btn.dataset.eng;
        const correct = state.quizCurrent.target.eng;
        const isCorrect = eng === correct;
        if (isCorrect) state.quizScore++;
        document.querySelectorAll('.quiz-opt').forEach(b => {
          b.disabled = true;
          if (b.dataset.eng === correct) b.classList.add('correct');
          else if (b === btn && !isCorrect) b.classList.add('wrong');
        });
        const t = state.quizCurrent.target;
        document.getElementById('quizFeedback').innerHTML =
          (isCorrect ? '✓ 정답! ' : '✗ 오답 — ') +
          `<b>${escHtml(t.eng)}</b>: ${escHtml(t.kor)}<br><em>${escHtml(t.ex)}</em>`;
        setTimeout(() => {
          state.quizIdx++;
          if (state.quizIdx >= state.quizPool.length) {
            document.getElementById('panel').innerHTML = resultHTML(state.quizScore, state.quizPool.length, 'initQuiz');
            return;
          }
          nextQuiz(); renderPanel();
        }, 1800);
      };
    });
    const sp = document.querySelector('.quiz-prompt [data-act="speak"]');
    if (sp) sp.onclick = () => speak(state.quizCurrent.target.eng);
  }
  if (state.mode === 'typing') {
    const it = typeCurrent();
    if (state.typeSub === 'audio' && it) speak(it.eng);
    const input = document.getElementById('typeInput');
    if (input) {
      input.focus();
      input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') { e.preventDefault(); submitType(); }
      });
    }
    const replay = document.getElementById('typeReplay');
    if (replay) replay.onclick = () => { const c = typeCurrent(); if (c) speak(c.eng); };
    document.getElementById('typeSubmit').onclick = submitType;
    document.querySelectorAll('.flash-nav [data-act="skip"]').forEach(b => {
      b.onclick = () => { advanceType(); };
    });
  }
}

function submitType() {
  if (state.typeAnswered) { advanceType(); return; }
  const input = document.getElementById('typeInput');
  const it = typeCurrent();
  if (!it || !input) return;
  const guess = input.value.trim().toLowerCase().replace(/\s+/g, ' ');
  const target = it.eng.toLowerCase().trim();
  const isCorrect = guess === target;
  state.typeAnswered = true;
  input.disabled = true;
  input.classList.add(isCorrect ? 'correct' : 'wrong');
  const fb = document.getElementById('typeFb');
  fb.className = 'type-feedback ' + (isCorrect ? 'ok' : 'bad');
  fb.innerHTML = (isCorrect ? '✓ 정답!' : '✗ 오답') +
    ` &nbsp;<span class="ans">${escHtml(it.eng)}</span>` +
    (state.typeSub === 'meaning' ? '' : ` &nbsp;<span style="color:#666">${escHtml(it.kor)}</span>`) +
    `<span class="ex">"${escHtml(it.ex)}"</span>` +
    `<div style="margin-top:8px;font-size:12px;">Enter로 다음 문제</div>`;
  if (isCorrect) state.typeScore++;
  speak(it.eng);
  document.getElementById('typeSubmit').textContent = '다음 →';
}
function advanceType() {
  state.typeIdx++;
  state.typeAnswered = false;
  if (state.typeIdx >= state.typePool.length) {
    document.getElementById('panel').innerHTML = resultHTML(state.typeScore, state.typePool.length, 'initType');
    return;
  }
  renderPanel();
}

function resultHTML(score, total, restartFn) {
  const pct = Math.round(score/total*100);
  return `<div class="empty" style="padding:80px 20px;">
    <div style="font-size:38px;font-weight:800;margin-bottom:8px;">${score} / ${total}</div>
    <div style="margin-bottom:20px;">${pct}% 정답</div>
    <button class="navbtn primary" onclick="window.${restartFn}(); window.renderPanel();">다시 풀기</button>
  </div>`;
}

function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}
function escHtml(s) {
  return String(s).replace(/[&<>"']/g, c => ({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[c]));
}
function escAttr(s) { return escHtml(s); }

document.addEventListener('keydown', (e) => {
  const tag = e.target.tagName;
  if (tag === 'INPUT' || tag === 'TEXTAREA') return;
  if (state.mode === 'flash') {
    if (e.key === 'ArrowRight') document.querySelector('.flash-nav [data-act="next"]')?.click();
    if (e.key === 'ArrowLeft')  document.querySelector('.flash-nav [data-act="prev"]')?.click();
    if (e.key === ' ') { e.preventDefault(); document.querySelector('.flash-nav [data-act="speak"]')?.click(); }
    if (e.key === 'Enter') { e.preventDefault(); document.getElementById('flashcard')?.click(); }
  }
});

function render() { setAccent(); renderTabs(); renderToolbar(); renderSubbar(); renderPanel(); }

window.initQuiz = initQuiz; window.initType = initType;
window.renderPanel = renderPanel; window.state = state;

render();
</script>
</body>
</html>
"""

out = HTML.replace("__DATA__", data_json)
out_path = "/Users/pyunhanga/output/vocab_study.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(out)
print("Wrote:", out_path, "—", len(out), "bytes")
