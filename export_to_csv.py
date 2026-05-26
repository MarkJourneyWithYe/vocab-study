"""Export build_vocab.py data lists to CSVs under data/.

One-shot conversion script — after this, site.yaml + vocab_site_builder
is the source of truth.
"""
import csv
import runpy
from pathlib import Path

mod = runpy.run_path("build_vocab.py", run_name="vocab_data")

EXPORTS = {
    "suneung_words":     "수능_단어",
    "suneung_idioms":    "수능_숙어",
    "toeic_words":       "토익_단어",
    "toeic_idioms":      "토익_숙어",
    "gongmuwon_words":   "공무원_단어",
    "gongmuwon_idioms":  "공무원_숙어",
    "naesin_words":      "내신_단어",
    "naesin_idioms":     "내신_숙어",
}

out_dir = Path("data")
out_dir.mkdir(exist_ok=True)

for csv_name, var_name in EXPORTS.items():
    rows = mod[var_name]
    path = out_dir / f"{csv_name}.csv"
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["English", "Korean", "Example"])
        for eng, kor, ex in rows:
            w.writerow([eng, kor, ex])
    print(f"  {path}: {len(rows)} rows")

print("\n✓ Exported 8 CSVs. site.yaml is now ready for vocab_site_builder.")
