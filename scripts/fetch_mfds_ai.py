"""의료기기안심책방에서 AI 후보 분류명 품목을 모아 knowledge/11_한국_AI허가목록.md 를 만든다.

사용: py scripts/fetch_mfds_ai.py
"""
import datetime
import html
import re
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

BASE = "https://emedi.mfds.go.kr/search/data/list"
TERMS = ["진단보조", "검출보조", "의료영상분석장치소프트웨어", "영상 분석 소프트웨어", "생체신호 분석 소프트웨어"]
OUT = Path(__file__).resolve().parent.parent / "knowledge" / "11_한국_AI허가목록.md"


def fetch(term, page):
    q = {
        "chkList": "1", "nowPageNum": "1" if page == 1 else str((page - 1) * 10), "tabGubun": "1",
        "query2": term, "grade": "0", "indtyCd": "1|2|21|22", "chkGroup": "GROUP_BY_FIELD_01",
        "pageNum": str(page), "searchYn": "true" if page == 1 else "", "searchAfKey": "", "searchOn": "Y",
    }
    req = urllib.request.Request(BASE + "?" + urllib.parse.urlencode(q), headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8")


def cells(tr):
    tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
    return [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t))).strip() for t in tds]


def collect():
    items, totals = {}, {}
    for term in TERMS:
        got = 0
        for page in range(1, 60):
            doc = fetch(term, page)
            if page == 1:
                m = re.search(r"총\s*([\d,]+)\s*건", re.sub(r"<[^>]+>", "", doc))
                totals[term] = int(m.group(1).replace(",", "")) if m else 0
            body = re.search(r"<tbody[^>]*>(.*?)</tbody>", doc, re.S)
            rows = [cells(tr) for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", body.group(1) if body else "", re.S)]
            # 원본 HTML 에는 순번 뒤에 빈 칸이 하나 더 있다
            rows = [c[:1] + c[2:] if len(c) > 1 and c[1] == "" else c for c in rows]
            rows = [c for c in rows if len(c) >= 11]
            for c in rows:
                got += 1
                items.setdefault(c[3], c)
            if not rows or got >= totals[term]:
                break
    return items, totals


def group_of(name):
    n = name.replace(" ", "")
    if "검출" in n or "진단보조" in n:
        return "A. 검출·진단보조 (AI 가능성 높음)"
    if "생체신호" in n:
        return "C. 생체신호 분석"
    return "B. 영상 분석 (AI·일반 SW 섞임)"


def main():
    items, totals = collect()
    today = datetime.date.today().isoformat()
    groups = defaultdict(list)
    for c in items.values():
        groups[group_of(c[2])].append(c)
    lines = [
        "# 한국 — AI 의료기기 후보 허가 목록 (식약처)", "",
        f"기준일: {today}", "",
        "출처: 의료기기안심책방 품목검색 (https://emedi.mfds.go.kr/search/data/MNU20237). `scripts/fetch_mfds_ai.py` 로 다시 만든다.", "",
        "**분류명 기준 후보 목록이다. AI 여부는 각 품목 상세 기재사항(작용원리·학습데이터)으로 확인해야 한다.**", "",
        "## 읽는 법",
        "- A 묶음(검출·진단보조): 병변을 찾거나 진단을 돕는 SW. 대부분 AI.",
        "- B 묶음(영상 분석): 크기·부피 측정, 3D 재구성 등. AI 제품과 일반 영상처리 SW가 섞임.",
        "- C 묶음(생체신호 분석): 심전도·활력징후로 위험 예측 등.",
        "- 상태 '전환' = 디지털의료제품법 시행으로 디지털의료기기로 전환된 품목. '정상'과 함께 현재 유효.",
        "- 품목명이 같은 종류라도 띄어쓰기가 다르게 등록됨(예: 뇌영상검출·진단보조소프트웨어 / 뇌 영상 검출·진단보조 소프트웨어).", "",
        "## 검색어별 건수", "", "| 검색어 | 건수 |", "|---|---|",
        *[f"| {t} | {n} |" for t, n in totals.items()],
        f"| 중복 제거 합계 (허가번호 기준) | {len(items)} |", "",
    ]
    for g in sorted(groups):
        rows = sorted(groups[g], key=lambda c: c[10], reverse=True)
        valid = sum(1 for c in rows if c[5] in ("정상", "전환"))
        lines += [f"## {g} — {len(rows)}건 (유효 {valid}건)", "",
                  "| 업체 | 품목명 | 제품명·모델명 | 허가번호 | 등급 | 상태 | 허가일 |", "|---|---|---|---|---|---|---|"]
        for c in rows:
            prod = " / ".join(x for x in (c[8], c[9]) if x).replace("|", "/")
            state = c[5] + (f" ({c[6]})" if c[6] else "")
            lines.append(f"| {c[1]} | {c[2]} | {prod} | {c[3]} | {c[4]} | {state} | {c[10]} |")
        lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(len(items), totals)


if __name__ == "__main__":
    main()
