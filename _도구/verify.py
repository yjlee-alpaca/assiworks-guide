# -*- coding: utf-8 -*-
"""어시웍스 가이드 발송 전 검증. 하나라도 걸리면 0이 아닌 코드로 끝난다.

  python3 _도구/verify.py index.html usage.html

보는 것
  1 옛 이름      바뀐 화면 이름이 남아 있는지 (배포 히스토리, 켤 패널 ...)
  2 기관 표현    특정 기관이 드러나는 지명·업무 이름이 남아 있는지
  3 표기         한글 문장의 em dash, 겹낫표
  4 글 너비      본문에 max-width(ch) 제한이 다시 들어갔는지
  5 탭           사용 가이드 목차 일곱 개가 다 있는지
  6 화면         브라우저로 열어 콘솔 오류, 깨진 이미지, 가로 넘침(375 · 1280)

6은 playwright-core 가 있어야 돈다. 없으면 건너뛰었다고 적고 실패로 친다.
CSS 가 깨지면 6 의 넘침 검사는 오히려 통과할 수 있다. 화면은 눈으로도 한 번 본다.
"""
import io, os, re, sys, json, subprocess, tempfile

옛이름 = ['배포 히스토리', '켤 패널', '운영사가 정하는 값', '어드민 승인',
        '무엇을 돌릴까요', '언제 돌릴까요', '설정 바꾸기']
기관 = ['국립공원', '공원구역', '국공원', '항우연', '한국항공우주', 'KARI', '산림', '산사태',
       '설악', '대청봉', '지리산', '반야봉', '덕유산', '속초', '인제군', '양양', '고성군',
       '탐방로', '구상나무', '원자력통제', 'IBS', 'knps']
탭 = ['시작하기', '유닛 만들기', '앱과 팀', '자료와 연결', '예약과 기록',
     '대화형 화면 사용하기', '어시지오(지도) 사용하기']

PW = os.environ.get('PLAYWRIGHT_CORE',
    '/Users/yeonjae/dev/New-assi-works-front/node_modules/.pnpm/playwright-core@1.58.2/node_modules/playwright-core/index.mjs')

def 글자(html):
    """보이는 글자만. 스타일, 스크립트, base64 이미지는 뺀다"""
    t = re.sub(r'<(style|script)[^>]*>.*?</\1>', ' ', html, flags=re.S)
    # 약관 모달은 법률 원문 그대로라(「」 법령명 등) 표기 검사에서 뺀다
    t = re.sub(r'<dialog class="legal-dlg".*?</dialog>', ' ', t, flags=re.S)
    t = re.sub(r'data:[^"\')\s]+', ' ', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    import html as H
    return H.unescape(t)

def 정적(f):
    문제 = []
    src = io.open(f, encoding='utf-8').read()
    t = 글자(src)
    for w in 옛이름:
        if w in t: 문제.append(f'1 옛 이름 "{w}" {t.count(w)}건')
    for w in 기관:
        if w in t: 문제.append(f'2 기관 표현 "{w}" {t.count(w)}건')
    for m in re.finditer(r'[가-힣][^\n<]{0,3}—|—[^\n<]{0,3}[가-힣]', t):
        문제.append(f'3 em dash: …{t[max(0,m.start()-12):m.end()+12].strip()}…'); break
    if '「' in t or '」' in t: 문제.append('3 겹낫표 「」')
    css = ' '.join(re.findall(r'<style[^>]*>(.*?)</style>', src, flags=re.S))
    if re.search(r'max-width:\s*\d+ch', css): 문제.append('4 본문 글 너비 제한(max-width: ch)')
    if os.path.basename(f).startswith('usage'):
        for w in 탭:
            # 2026-10-22 위쪽 탭 줄을 왼쪽 목차(data-tab 링크)로 바꿨다. 둘 다 받는다
            if not re.search(r'(?:role="tab"|data-tab)[^>]*>(?:(?!</a>).)*' + re.escape(w), src, flags=re.S):
                문제.append(f'5 탭 없음 "{w}"')
    return 문제

JS = r'''
import { chromium } from %s
const files = %s
const out = {}
const b = await chromium.launch()
for (const f of files) {
  out[f] = []
  for (const w of [375, 1280]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } })
    const errs = []
    p.on('pageerror', e => errs.push(e.message))
    p.on('console', m => { if (m.type() === 'error') errs.push(m.text()) })
    await p.goto('file://' + f, { waitUntil: 'load' })
    await p.waitForTimeout(500)
    const r = await p.evaluate(() => {
      // 탭이 있으면 모든 패널을 펼쳐서 본다
      document.querySelectorAll('[role=tabpanel],.panel').forEach(e => { e.hidden = false; e.style.display = 'block' })
      // 확대 보기(#lb)처럼 src 가 비어 있는 자리는 뺀다
      const broken = [...document.images].filter(i => i.getAttribute('src') && i.complete && i.naturalWidth === 0).length
      const W = document.documentElement.clientWidth
      const over = [...document.querySelectorAll('body *')].filter(e => {
        if (e.closest('table,pre,.tabs,nav,[role=tablist]')) return false
        // svg 안의 도형은 svg 상자 밖으로 나가도 그 상자에서 잘린다. 넘침이 아니다
        if (e.ownerSVGElement) return false
        const r = e.getBoundingClientRect(); return r.width > 0 && r.right > W + 1
      }).slice(0, 3).map(e => e.tagName + '.' + (e.className || '') + ' ' + (e.textContent || '').trim().slice(0, 30))
      return { broken, over, scroll: document.documentElement.scrollWidth > W + 1 }
    })
    if (errs.length) out[f].push(`6 콘솔 오류 ${w}px: ${errs[0]}`)
    if (r.broken) out[f].push(`6 깨진 이미지 ${r.broken}장 (${w}px)`)
    if (r.scroll) out[f].push(`6 가로 스크롤 생김 (${w}px)`)
    for (const o of r.over) out[f].push(`6 넘침 ${w}px: ${o}`)
    await p.close()
  }
}
await b.close()
console.log(JSON.stringify(out))
'''

def 화면(files):
    if not os.path.exists(PW):
        return {f: ['6 화면 검사 건너뜀: playwright-core 없음 (PLAYWRIGHT_CORE 로 경로 지정)'] for f in files}
    with tempfile.NamedTemporaryFile('w', suffix='.mjs', delete=False, encoding='utf-8') as s:
        s.write(JS % (json.dumps(PW), json.dumps(files)))
    try:
        r = subprocess.run(['node', s.name], capture_output=True, text=True, timeout=300)
        return json.loads(r.stdout.strip().splitlines()[-1])
    except Exception as e:
        return {f: [f'6 화면 검사 실패: {e}'] for f in files}
    finally:
        os.unlink(s.name)

def main():
    files = [os.path.abspath(a) for a in sys.argv[1:]]
    if not files:
        print(__doc__); sys.exit(2)
    동적 = 화면(files)
    총 = 0
    for f in files:
        문제 = 정적(f) + 동적.get(f, [])
        총 += len(문제)
        print(f'■ {os.path.basename(f)}  {"통과" if not 문제 else str(len(문제)) + "건"}')
        for m in 문제: print('   ', m)
    print('=' * 50)
    print('전부 통과' if 총 == 0 else f'걸린 것 {총}건')
    sys.exit(1 if 총 else 0)

if __name__ == '__main__':
    main()
