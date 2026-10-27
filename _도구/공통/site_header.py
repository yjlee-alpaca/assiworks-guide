# -*- coding: utf-8 -*-
"""가이드 세 쪽(구조 및 개념 가이드, 사용 가이드, 릴리즈 노트)에 붙는 공통 헤더.

작업본의 @@SITE_HEADER:<쪽>@@ 자리를 render(<쪽>) 결과로 바꾼다.
쪽 이름은 guide, usage, releases. 지금 보는 쪽 링크에 aria-current 가 붙는다.

- 랜딩 헤더와 같은 구성이다: 로고(소개로), 가이드 링크 세 개, 도입 문의. 반투명 배경에 blur.
- 색은 가이드의 토큰(--paper, --ink ...)을 써서 다크 모드에서도 맞는다. 로고 글자도 --ink 를 따른다.
- 폭(1200px, 여백은 바깥), 높이(72px, 모바일 100px), 로고(21px)는 소개 페이지 헤더와 같다. 쪽마다 본문 폭이 달라도 헤더는 같다.
- 헤더 높이는 --hdr-h 로 내보낸다. 왼쪽 목차, 절 이동 여백이 이 값을 쓴다.
- 링크는 가이드 사이트(Vercel) 주소로 적는다. about-assiworks 로 옮길 때 export_about.py 가 새 주소로 바꾼다.
"""
import os, re

LOGO = '/Users/yeonjae/dev/New-assi-works-front/src/assets/logo-assiworks.svg'

CSS = '''<style>
:root{--hdr-h:73px}
@media (max-width:760px){:root{--hdr-h:101px}}
html{scroll-padding-top:calc(var(--hdr-h) + 16px)}
.site-hdr{position:sticky;top:0;z-index:60;border-bottom:1px solid var(--line);
 background:color-mix(in srgb,var(--paper) 72%,transparent);-webkit-backdrop-filter:saturate(180%) blur(16px);backdrop-filter:saturate(180%) blur(16px)}
@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))){.site-hdr{background:var(--paper)}}
.site-hdr .hrow{box-sizing:content-box;max-width:1200px;margin:0 auto;padding-left:max(24px,env(safe-area-inset-left,0px));padding-right:max(24px,env(safe-area-inset-right,0px));height:72px;display:flex;align-items:center;gap:40px}
.site-hdr .hlogo{display:flex;align-items:center;color:var(--ink)}
.site-hdr .hlogo svg{height:21px;width:auto;display:block}
.site-hdr .hpages{display:flex;align-items:center;gap:24px;margin-left:auto;margin-right:-12px}
.site-hdr .hl{font-size:15px;font-weight:500;line-height:1.4;color:var(--ink-2);text-decoration:none;white-space:nowrap}
.site-hdr .hl:hover{color:var(--ink)}
.site-hdr .hl[aria-current]{color:var(--ink);font-weight:700}
.site-hdr .hbtn{display:inline-flex;align-items:center;height:40px;padding:0 18px;border-radius:999px;background:var(--ink);color:var(--paper);font-size:15px;font-weight:600;text-decoration:none;white-space:nowrap}
.site-hdr .hsub{display:none}
.site-hdr a:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:6px}
@media (max-width:760px){
 .site-hdr .hrow{gap:12px}
 .site-hdr .hlogo svg{height:16px}
 .site-hdr .hpages{display:none}
 .site-hdr .hbtn{margin-left:auto}
 .site-hdr .hsub{display:flex;justify-content:center;align-items:flex-start;gap:20px;height:28px;box-sizing:border-box;padding:0 24px 12px}
 .site-hdr .hsub .hl{font-size:13px}
}
</style>'''

PAGES = [('guide', '/', '구조 및 개념 가이드'), ('usage', '/usage', '사용 가이드'), ('releases', '/releases', '릴리즈 노트')]


def _logo():
    svg = open(LOGO, encoding='utf-8').read()
    svg = re.sub(r'<\?xml[^>]*>', '', svg).strip()
    svg = svg.replace('fill="#2D2D2D"', 'fill="currentColor"')
    return svg.replace('<svg ', '<svg aria-hidden="true" focusable="false" ', 1)


def _links(cur):
    return '\n'.join(
        f'<a class="hl" href="{href}"' + (' aria-current="page"' if key == cur else '') + f'>{text}</a>'
        for key, href, text in PAGES)


def render(cur):
    assert cur in [p[0] for p in PAGES], cur
    return (CSS + '\n'
            '<header class="site-hdr">\n'
            '<div class="hrow">\n'
            f'<a class="hlogo" href="/business" aria-label="어시웍스 소개">{_logo()}</a>\n'
            f'<nav class="hpages" aria-label="가이드">\n{_links(cur)}\n</nav>\n'
            '<a class="hbtn" href="/business#contact">도입 문의</a>\n'
            '</div>\n'
            f'<nav class="hsub" aria-label="가이드">\n{_links(cur)}\n</nav>\n'
            '</header>')


def fill(html):
    """@@SITE_HEADER:<쪽>@@ 를 모두 바꾼다"""
    return re.sub(r'@@SITE_HEADER:(\w+)@@', lambda m: render(m.group(1)), html)
