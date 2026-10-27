# -*- coding: utf-8 -*-
"""릴리즈 노트 빌드. 작업본(releases_src.html)과 캡처(img/*.png)로 발송본 releases.html 을 만든다.

  python3 _도구/릴리즈/build.py

- @@FONT@@ 자리에 business.html 의 Pretendard @font-face 를 그대로 넣는다.
- @@IMG:이름|설명@@ 자리에 img/이름.png 를 1600px webp 로 넣는다. 캡처가 없으면 점선 자리만 둔다.
발송본(releases.html)은 손으로 고치지 않는다. 작업본을 고치고 다시 돌린다.
"""
import base64, io, os, re
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
import sys; sys.path.insert(0, os.path.join(HERE, '..', '공통'))
from site_header import fill as site_header
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
src = open(os.path.join(HERE, 'releases_src.html'), encoding='utf-8').read()
usage = open(os.path.join(ROOT, 'business.html'), encoding='utf-8').read()
font = re.search(r'@font-face\{[^}]*\}', usage).group(0)
src = src.replace('@@FONT@@', font)
src = site_header(src)

def img(m):
    name, cap = m.group(1), m.group(2)
    p = os.path.join(HERE, 'img', name + '.png')
    if not os.path.exists(p):
        return f'<figure><div class="ph">캡처 자리: {name}</div><figcaption>{cap}</figcaption></figure>'
    im = Image.open(p).convert('RGB')
    if im.width > 1600:
        im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'WEBP', quality=86)
    data = base64.b64encode(b.getvalue()).decode()
    return (f'<figure><img src="data:image/webp;base64,{data}" width="{im.width}" height="{im.height}" '
            f'alt="{cap}" loading="lazy"><figcaption>{cap}</figcaption></figure>')

out = re.sub(r'@@IMG:([\w-]+)\|([^@]+)@@', img, src)
dst = os.path.join(ROOT, 'releases.html')
open(dst, 'w', encoding='utf-8').write(out)
print(dst, round(len(out) / 1024), 'KB', 'emdash', out.count('—'))
