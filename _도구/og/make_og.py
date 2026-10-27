# -*- coding: utf-8 -*-
"""링크 미리보기(OG) 이미지 다섯 장을 만든다. 1200x630 PNG.

  python3 _도구/og/make_og.py

- out/<쪽>.png 에 쓴다. 쪽은 business, personal, guide, usage, releases.
- 가운데 정렬이다. 슬랙처럼 가운데를 정사각형으로 잘라 작게 보여 줘도 제목이 잘리지 않게 한다.
- 문구는 아래 PAGES 에서 고친다. 소개 페이지 첫 화면 문구와 같게 둔다.
- 화면은 playwright-core 로 찍는다(verify.py 와 같은 경로).
- export_about.py 가 out/ 을 about-assiworks 의 public/og/ 로 복사하고 각 쪽에 og 태그를 넣는다.
"""
import base64, json, os, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
A = '/Users/yeonjae/dev/New-assi-works-front/src/assets/'
PW = os.environ.get('PLAYWRIGHT_CORE',
    '/Users/yeonjae/dev/New-assi-works-front/node_modules/.pnpm/playwright-core@1.58.2/node_modules/playwright-core/index.mjs')

PAGES = {
    'business': ('조직용', '반복 업무는 AI에게,<br>중요한 판단은 사람에게.', '업무에 맞게 만드는 AI 플랫폼'),
    'personal': ('개인용', '반복되는 일은 줄이고,<br>중요한 일에 집중하세요.', '내 업무에 맞춰 직접 만드는 AI 업무 도구'),
    'guide': ('가이드', '어시웍스<br>구조 및 개념 가이드', '운영사, 고객사, 팀, 개인 공간의 관계와 주요 용어'),
    'usage': ('가이드', '어시웍스<br>사용 가이드', '유닛 만들기부터 대화형 화면, 어시지오까지'),
    'releases': ('릴리즈 노트', '어시웍스<br>릴리즈 노트', '새로 추가된 기능과 변경 사항'),
}


def b64(path):
    return base64.b64encode(open(path, 'rb').read()).decode()


def page_html(tag, title, sub):
    font = b64(A + 'fonts/pretendard/woff2/PretendardVariable.woff2')
    logo = b64(A + 'logo-assiworks.svg')
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:P;src:url(data:font/woff2;base64,{font}) format("woff2");font-weight:100 900}}
*{{margin:0;box-sizing:border-box}}
body{{width:1200px;height:630px;overflow:hidden;font-family:P,sans-serif;background:#FFFFFF;position:relative;color:#1B1B1B}}
.glow{{position:absolute;left:50%;top:50%;width:900px;height:900px;transform:translate(-50%,-50%);border-radius:50%;
 background:radial-gradient(circle,rgba(112,46,255,0.12) 0%,rgba(112,46,255,0.05) 38%,rgba(112,46,255,0) 66%)}}
.wrap{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 80px}}
.logo{{height:30px;width:auto;display:block;margin-bottom:44px}}
.tag{{display:inline-block;font-size:22px;font-weight:700;color:#702EFF;background:#F0E9FF;border-radius:999px;padding:7px 18px;margin-bottom:22px}}
h1{{font-size:58px;line-height:1.2;font-weight:800;letter-spacing:-0.035em}}
p{{margin-top:22px;font-size:25px;line-height:1.4;color:#525264;font-weight:500;letter-spacing:-0.01em}}
.url{{position:absolute;left:0;right:0;bottom:40px;text-align:center;font-size:19px;color:#A1A1AA;font-weight:500}}
</style></head><body>
<div class="glow"></div>
<div class="wrap">
<img class="logo" src="data:image/svg+xml;base64,{logo}" alt="">
<span class="tag">{tag}</span><h1>{title}</h1><p>{sub}</p>
</div>
<div class="url">assiworks.aifactory.page</div>
</body></html>'''


JS = '''import { chromium } from %s
const jobs = %s
const b = await chromium.launch()
const p = await b.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 })
for (const [file, out] of jobs) {
  await p.goto('file://' + file); await p.waitForTimeout(300)
  await p.screenshot({ path: out })
}
await b.close()
'''


def main():
    os.makedirs(OUT, exist_ok=True)
    tmp = tempfile.mkdtemp()
    jobs = []
    for key, (tag, title, sub) in PAGES.items():
        f = os.path.join(tmp, key + '.html')
        open(f, 'w', encoding='utf-8').write(page_html(tag, title, sub))
        jobs.append([f, os.path.join(OUT, key + '.png')])
    js = os.path.join(tmp, 'shot.mjs')
    open(js, 'w', encoding='utf-8').write(JS % (json.dumps(PW), json.dumps(jobs)))
    subprocess.run(['node', js], check=True)
    for _, out in jobs:
        print(out, os.path.getsize(out) // 1024, 'KB')


if __name__ == '__main__':
    main()
