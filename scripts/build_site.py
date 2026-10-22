"""knowledge/·sources/·prompts/·docs/ 의 .md 를 공개 사이트(site/)로 만든다.

site/index.html 은 왼쪽 메뉴 + 오른쪽 문서 틀(maiReport 공유 사이트와 같은 구조),
site/p/<id>.html 은 문서 한 장씩. 깃허브 Actions 가 site/ 를 GitHub Pages 로 올린다.
"""
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

# (그룹, [(id, 아이콘+제목, 원본 경로)]) — ADMIN_GROUPS 는 관리자 로그인 후에만 메뉴에 보임
ADMIN_GROUPS = {"관리자 · 에이전트"}
MENU = [
    ("한눈에 보기", [
        ("compare", "📊 관할 비교표", "knowledge/90_관할비교표.md"),
        ("common", "🌐 공통 기반 · 국제 조화", "knowledge/00_공통_국제조화.md"),
    ]),
    ("관할별 지식", [
        ("kr", "🇰🇷 한국 MFDS", "knowledge/10_한국_MFDS.md"),
        ("us", "🇺🇸 미국 FDA", "knowledge/20_미국_FDA.md"),
        ("eu", "🇪🇺 EU MDR · AI Act", "knowledge/30_EU_MDR_AIAct.md"),
        ("sg", "🇸🇬 싱가포르 HSA", "knowledge/40_싱가포르_HSA.md"),
        ("jp", "🇯🇵 일본 PMDA", "knowledge/50_일본_PMDA.md"),
    ]),
    ("허가 사례", [
        ("kr-ai-list", "📋 한국 AI 허가 후보 목록", "knowledge/11_한국_AI허가목록.md"),
    ]),
    ("근거", [
        ("sources", "🔗 출처 목록", "sources/출처목록.md"),
    ]),
    ("관리자 · 에이전트", [
        ("prompt", "🤖 범용 인허가 에이전트 프롬프트", "prompts/범용_인허가에이전트_프롬프트.md"),
        ("design", "🧩 에이전트 설계 요소", "docs/에이전트_설계요소.md"),
    ]),
]

PAGE = (ROOT / "scripts" / "site_page.html").read_text(encoding="utf-8")
SHELL = (ROOT / "scripts" / "site_index.html").read_text(encoding="utf-8")

(SITE / "p").mkdir(parents=True, exist_ok=True)
nav = []
for group, items in MENU:
    links = []
    for pid, label, src in items:
        path = ROOT / src
        if not path.exists():
            continue
        md = path.read_text(encoding="utf-8")
        (SITE / "p" / f"{pid}.html").write_text(
            PAGE.replace("__TITLE__", html.escape(label[2:].strip()))
                .replace("/*__MD__*/\"\"", json.dumps(md, ensure_ascii=False).replace("</", "<\\/")),
            encoding="utf-8")
        cls = ' class="admin-only"' if group in ADMIN_GROUPS else ""
        links.append(f'<a{cls} href="#{pid}" data-src="p/{pid}.html">{html.escape(label)}</a>')
    if links:
        if group in ADMIN_GROUPS:
            nav.append('<div class="admin-heading admin-only">관리자 작업 공간</div>')
        gcls = "nav-group admin-only" if group in ADMIN_GROUPS else "nav-group"
        nav.append(f'<details class="{gcls}" open><summary>{html.escape(group)}'
                   f'<span class="group-count">{len(links)}</span></summary>'
                   f'<div class="group-links">\n' + "\n".join(links) + "\n</div></details>")

(SITE / "index.html").write_text(SHELL.replace("<!--__NAV__-->", "\n".join(nav)), encoding="utf-8")
(SITE / ".nojekyll").write_text("", encoding="utf-8")
print(f"site built: {sum(len(i) for _, i in MENU)} pages")
