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
import html, os, re, shutil, sys

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

SITE = 'https://assiworks.aifactory.page'
OG_DIR = os.path.join(ROOT, '_도구', 'og', 'out')

# 링크 미리보기(슬랙, 카톡 등). 이미지는 _도구/og/make_og.py 로 만든다
OG = {
    'business.html': ('/', 'business', '어시웍스 조직용 소개',
                      '업무에 맞게 만드는 AI 플랫폼. 반복 업무는 AI에게, 중요한 판단은 사람에게.'),
    'personal.html': ('/personal', 'personal', '어시웍스 개인용 소개',
                      '내 업무에 맞춰 직접 만드는 AI 업무 도구. 반복되는 일은 줄이고, 중요한 일에 집중하세요.'),
    'index.html': ('/guide', 'guide', None, None),
    'usage.html': ('/guide/usage', 'usage', None, None),
    'releases.html': ('/releases', 'releases', None, None),
}

def og_tags(t, src):
    """<head> 에 description 과 og·twitter 태그를 넣는다. 제목·설명이 None 이면 쪽의 <title>, description 을 쓴다"""
    path, img, title, desc = OG[src]
    title = title or html.unescape(re.search(r'<title>(.*?)</title>', t, re.S).group(1).strip())
    m = re.search(r'<meta name="description" content="([^"]*)">', t)
    desc = desc or html.unescape(m.group(1))
    e = lambda s: html.escape(s, quote=True)
    tags = [f'<meta property="og:type" content="website">',
            f'<meta property="og:site_name" content="어시웍스 AssiWorks">',
            f'<meta property="og:title" content="{e(title)}">',
            f'<meta property="og:description" content="{e(desc)}">',
            f'<meta property="og:url" content="{SITE}{path}">',
            f'<meta property="og:image" content="{SITE}/og/{img}.png">',
            '<meta property="og:image:width" content="1200">',
            '<meta property="og:image:height" content="630">',
            '<meta property="og:locale" content="ko_KR">',
            '<meta name="twitter:card" content="summary_large_image">',
            f'<link rel="canonical" href="{SITE}{path}">']
    if not m:
        tags.insert(0, f'<meta name="description" content="{e(desc)}">')
    assert 'og:image' not in t, src + ' 에 이미 og 태그가 있다'
    return t.replace('</title>', '</title>\n' + '\n'.join(tags), 1)

def main():
    if len(sys.argv) != 2:
        print(__doc__); sys.exit(2)
    out = os.path.join(os.path.abspath(sys.argv[1]), 'public', 'site')
    os.makedirs(out, exist_ok=True)
    for src, dst in FILES.items():
        t = open(os.path.join(ROOT, src), encoding='utf-8').read()
        t2, n = re.subn(r'<a\b([^>]*?)href="([^"]*)"([^>]*)>(.*?)</a>', 바꾸기, t, flags=re.S)
        t2 = og_tags(t2, src)
        open(os.path.join(out, dst), 'w', encoding='utf-8').write(t2)
        print(f'{src} → public/site/{dst}  링크 {n}개 확인, {len(t2) // 1024} KB')
    og = os.path.join(os.path.abspath(sys.argv[1]), 'public', 'og')
    os.makedirs(og, exist_ok=True)
    for k in ('business', 'personal', 'guide', 'usage', 'releases'):
        shutil.copyfile(os.path.join(OG_DIR, k + '.png'), os.path.join(og, k + '.png'))
    print('og 이미지 5장 → public/og/')

if __name__ == '__main__':
    main()
