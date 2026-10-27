# -*- coding: utf-8 -*-
"""가이드 사이트 발송본 다섯 쪽을 about-assiworks 저장소(assiworks.aifactory.page)로 옮긴다.

  python3 _도구/이전/export_about.py <about-assiworks 저장소 경로>

- 저장소 맨 위의 발송본(business, personal, index, usage, releases)을 읽어
  <저장소>/public/site/ 에 쓴다. 발송본은 손대지 않는다.
- 새 주소에 맞춰 페이지 사이 링크만 바꾼다.
    조직용 랜딩 /           개인용 랜딩 /personal
    구조 및 개념 가이드 /guide   사용 가이드 /guide/usage   릴리즈 노트 /releases
- 바꿀 링크는 (주소, 링크 글자) 쌍으로 정한다. 같은 "/" 라도 글자가 "구조 및 개념 가이드"면 /guide 로 간다.
  표에 없는 페이지 안 링크가 나오면 멈춘다. 새 링크를 만들었으면 아래 표에 더한다.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))

# 발송본 → public/site 안의 이름
FILES = {'business.html': 'business.html', 'personal.html': 'personal.html',
         'index.html': 'guide.html', 'usage.html': 'usage.html', 'releases.html': 'releases.html'}

# (지금 주소, 링크 글자) → 새 주소. 글자가 None 이면 글자와 상관없이 바꾼다
LINKS = {
    ('/business', None): '/',
    ('/business#contact', None): '/#contact',
    ('business', None): '/',
    ('/personal', None): '/personal',
    ('/usage', None): '/guide/usage',
    ('/releases', None): '/releases',
    ('usage', None): '/guide/usage',
    ('./', '구조 및 개념 가이드'): '/guide',
    ('/', '구조 및 개념 가이드'): '/guide',
    ('/', '어시웍스'): '/',
}

def 바꾸기(m):
    head, href, rest, body = m.group(1), m.group(2), m.group(3), m.group(4)
    if href.startswith(('#', 'http://', 'https://', 'mailto:', 'tel:', 'data:')):
        return m.group(0)
    text = re.sub(r'<[^>]+>', '', body).strip()
    new = LINKS.get((href, text), LINKS.get((href, None)))
    if new is None:
        raise SystemExit(f'표에 없는 링크: href="{href}" 글자="{text}"')
    return f'<a{head}href="{new}"{rest}>{body}</a>'

def main():
    if len(sys.argv) != 2:
        print(__doc__); sys.exit(2)
    out = os.path.join(os.path.abspath(sys.argv[1]), 'public', 'site')
    os.makedirs(out, exist_ok=True)
    for src, dst in FILES.items():
        t = open(os.path.join(ROOT, src), encoding='utf-8').read()
        t2, n = re.subn(r'<a\b([^>]*?)href="([^"]*)"([^>]*)>(.*?)</a>', 바꾸기, t, flags=re.S)
        open(os.path.join(out, dst), 'w', encoding='utf-8').write(t2)
        print(f'{src} → public/site/{dst}  링크 {n}개 확인, {len(t2) // 1024} KB')

if __name__ == '__main__':
    main()
