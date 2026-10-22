"""knowledge/·sources/ 의 .md 를 한 장짜리 확인용 페이지(site/index.html)로 묶는다."""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "scripts" / "site_template.html"
OUT = ROOT / "site" / "index.html"

LABELS = {
    "00": "공통·국제조화", "10": "한국 MFDS", "11": "한국 AI 허가 목록",
    "20": "미국 FDA", "30": "EU MDR·AI Act", "40": "싱가포르 HSA",
    "50": "일본 PMDA", "90": "관할 비교표",
}

docs = []
for f in sorted((ROOT / "knowledge").glob("*.md")):
    key = f.stem.split("_")[0]
    docs.append({"id": "k" + key, "label": LABELS.get(key, f.stem), "md": f.read_text(encoding="utf-8")})
docs.append({"id": "src", "label": "출처 목록", "md": (ROOT / "sources" / "출처목록.md").read_text(encoding="utf-8")})

html = TEMPLATE.read_text(encoding="utf-8").replace("/*__DOCS__*/[]", json.dumps(docs, ensure_ascii=False).replace("</", "<\\/"))
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(html, encoding="utf-8")
print(f"{OUT} ({len(docs)} docs)")
