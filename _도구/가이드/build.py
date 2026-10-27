# -*- coding: utf-8 -*-
"""가이드 두 쪽 빌드. 작업본과 캡처로 발송본 index.html, usage.html 을 만든다.

  python3 _도구/가이드/build.py

- index_src.html  구조 및 개념 가이드 작업본 → index.html
- usage_src.html  사용 가이드 작업본 → usage.html
- @@NEW:이름@@ 자리에 img/이름.webp 를 넣는다. 새 캡처는 1600px(crop 이 붙은 것은 900px), 품질 80 webp 로 img 에 둔다.
- @@IMG 번호@@ 자리에 *_imgs.json 의 해당 번호 이미지를 넣는다. 2026-10-20 이전 캡처다.
발송본은 손으로 고치지 않는다. 작업본을 고치고 다시 돌린다.
"""
import base64, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
import sys; sys.path.insert(0, os.path.join(HERE, '..', '공통'))
from site_header import fill as site_header
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))

def new(m):
    p = os.path.join(HERE, 'img', m.group(1) + '.webp')
    return 'data:image/webp;base64,' + base64.b64encode(open(p, 'rb').read()).decode()

for src, imgs, out in [('usage_src.html', 'usage_imgs.json', 'usage.html'),
                       ('index_src.html', 'index_imgs.json', 'index.html')]:
    t = open(os.path.join(HERE, src), encoding='utf-8').read()
    old = json.load(open(os.path.join(HERE, imgs)))
    t = re.sub(r'@@NEW:([a-z0-9-]+)@@', new, t)
    t = re.sub(r'@@IMG(\d+)@@', lambda m: old[int(m.group(1))], t)
    t = site_header(t, '1140px')
    assert '@@' not in t, out + ' 에 채우지 못한 자리가 남았다'
    open(os.path.join(ROOT, out), 'w', encoding='utf-8').write(t)
    v = re.sub(r'data:image/[a-z]+;base64,[A-Za-z0-9+/=]+', 'IMG', t)
    print(out, t.count('data:image/'), len(t) // 1024, 'KB', 'emdash', v.count('—'))
