# -*- coding: utf-8 -*-
"""소개 페이지 푸터의 이용약관·개인정보처리방침 모달.

원문은 about-assiworks 저장소의 content/legal/*.mdx 이고, 여기 legal/ 는 그 사본이다.
약관을 고치면 그쪽 원문을 고치고 여기로 다시 복사한다(sync_legal 참고). 내용은 손대지 않는다.

build_html.py 가 modal() 결과를 </body> 앞에 넣는다.
푸터의 /terms, /privacy 링크를 누르면 페이지 이동 대신 큰 모달(<dialog>)로 연다.
스크립트가 꺼진 환경에서는 링크대로 /ko/terms, /ko/privacy 페이지가 열린다.
"""
import html, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ABOUT_LEGAL = '/Users/yeonjae/dev/about-assiworks-migrate/content/legal'


def sync_legal():
    """about-assiworks 원문을 legal/ 로 복사한다. 원문이 없으면 지금 사본을 쓴다"""
    import shutil
    for n in ('terms.mdx', 'privacy.mdx'):
        src = os.path.join(ABOUT_LEGAL, n)
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(HERE, 'legal', n))


def _inline(s):
    s = s.replace("\\'", "'")
    s = html.escape(s, quote=False)
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)


def _html_block(block):
    """mdx 안의 HTML 표를 일반 HTML 로. JSX 속성(rowSpan={2}, className)을 바꾼다"""
    block = re.sub(r'rowSpan=\{(\d+)\}', r'rowspan="\1"', block)
    block = re.sub(r'colSpan=\{(\d+)\}', r'colspan="\1"', block)
    block = re.sub(r'\s*className="[^"]*"', '', block)
    return block


def mdx_to_html(path):
    text = open(path, encoding='utf-8').read()
    m = re.match(r'---\s*\n(.*?)\n---\s*\n', text, re.S)
    title = re.search(r'title:\s*(.+)', m.group(1)).group(1).strip() if m else ''
    body = text[m.end():] if m else text
    has_html_table = '<table' in body
    # HTML 표는 통째로 떼어 둔다
    tables = []
    body = re.sub(r'<table>.*?</table>', lambda t: (tables.append(_html_block(t.group(0))), f'\n@@T{len(tables) - 1}@@\n')[1], body, flags=re.S)
    out, para, items, pipe = [], [], [], []

    def flush():
        if para:
            out.append('<p>' + '<br>'.join(_inline(x) for x in para) + '</p>'); para.clear()
        if items:
            out.append('<ol>' + ''.join(f'<li>{_inline(x)}</li>' for x in items) + '</ol>'); items.clear()
        if pipe:
            # 같은 내용의 HTML 표가 따로 있으면 마크다운 표는 건너뛴다(원문에 두 번 들어 있다)
            if not has_html_table:
                rows = [[c.strip() for c in r.strip().strip('|').split('|')] for r in pipe if not re.match(r'^\|?\s*-', r.strip())]
                h, *rest = rows
                out.append('<table><thead><tr>' + ''.join(f'<th>{_inline(c)}</th>' for c in h) + '</tr></thead><tbody>'
                           + ''.join('<tr>' + ''.join(f'<td>{_inline(c)}</td>' for c in r) + '</tr>' for r in rest) + '</tbody></table>')
            pipe.clear()

    for raw in body.split('\n'):
        line = raw.strip()
        if not line or re.fullmatch(r'(<br\s*/>)+', line):
            flush(); continue
        if line.startswith('@@T'):
            flush(); out.append(tables[int(line[3:-2])]); continue
        if re.fullmatch(r'<hr\s*/>', line):
            flush(); out.append('<hr>'); continue
        if line.startswith('#'):
            flush(); out.append('<h3>' + _inline(line.lstrip('#').strip()) + '</h3>'); continue
        if line.startswith('|'):
            if para or items: flush()
            pipe.append(line); continue
        mi = re.match(r'^\d+[.)]\s+(.*)', line)
        if mi:
            if para: flush()
            items.append(mi.group(1)); continue
        if items or pipe: flush()
        para.append(line)
    flush()
    return title, '\n'.join(out)


CSS = '''<style>
.legal-dlg{width:min(880px,calc(100% - 32px));max-height:min(85vh,900px);padding:0;border:0;border-radius:18px;background:#FFFFFF;color:#27272A;box-shadow:0 24px 80px rgba(27,27,27,0.24);overflow:hidden}
.legal-dlg[open]{display:flex;flex-direction:column}
.legal-dlg::backdrop{background:rgba(24,24,27,0.48);-webkit-backdrop-filter:blur(4px);backdrop-filter:blur(4px)}
.legal-dlg .lg-head{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:20px 24px 18px 32px;border-bottom:1px solid #F0F0F2;flex:none}
.legal-dlg .lg-head h2{margin:0;font-size:20px;font-weight:700;letter-spacing:-.01em;color:#1B1B1B}
.legal-dlg .lg-x{width:40px;height:40px;border:0;border-radius:999px;background:#F4F4F5;color:#1B1B1B;font-size:20px;line-height:1;cursor:pointer;flex:none}
.legal-dlg .lg-x:hover{background:#E4E4E7}
.legal-dlg .lg-body{overflow:auto;padding:8px 32px 40px;font-size:15px;line-height:1.75;color:#3F3F46;overscroll-behavior:contain}
.legal-dlg h3{margin:28px 0 8px;font-size:16px;font-weight:700;color:#1B1B1B}
.legal-dlg p{margin:0 0 10px}
.legal-dlg ol{margin:4px 0 12px;padding-left:22px}
.legal-dlg li{margin:4px 0}
.legal-dlg hr{border:0;border-top:1px solid #E4E4E7;margin:32px 0}
.legal-dlg table{width:100%;border-collapse:collapse;margin:12px 0 16px;font-size:14px}
.legal-dlg th,.legal-dlg td{border:1px solid #E4E4E7;padding:10px 12px;text-align:left;vertical-align:top}
.legal-dlg th{background:#F4F4F5;font-weight:600;color:#1B1B1B}
.legal-dlg .lg-tbl{overflow-x:auto}
@media (max-width:760px){.legal-dlg{width:calc(100% - 24px);max-height:88vh;border-radius:14px}.legal-dlg .lg-head{padding:16px 16px 14px 20px}.legal-dlg .lg-head h2{font-size:18px}.legal-dlg .lg-body{padding:4px 20px 32px;font-size:14px}}
</style>'''

JS = '''<script>
(function(){
  var map={terms:'legal-terms',privacy:'legal-privacy'},last=null;
  function open(key){var d=document.getElementById(map[key]);if(!d||!d.showModal)return false;last=document.activeElement;d.showModal();d.querySelector('.lg-body').scrollTop=0;d.querySelector('.lg-x').focus();return true}
  document.querySelectorAll('a[href]').forEach(function(a){
    var m=a.getAttribute('href').match(/\\/(terms|privacy)$/);
    if(!m)return;
    a.addEventListener('click',function(e){if(open(m[1]))e.preventDefault()});
  });
  Object.keys(map).forEach(function(k){
    var d=document.getElementById(map[k]);if(!d)return;
    d.querySelector('.lg-x').addEventListener('click',function(){d.close()});
    d.addEventListener('click',function(e){if(e.target===d)d.close()});
    d.addEventListener('close',function(){if(last&&last.focus)last.focus()});
  });
})();
</script>'''


def modal():
    parts = [CSS]
    for key, fn in (('terms', 'terms.mdx'), ('privacy', 'privacy.mdx')):
        title, body = mdx_to_html(os.path.join(HERE, 'legal', fn))
        body = re.sub(r'(<table>.*?</table>)', r'<div class="lg-tbl">\1</div>', body, flags=re.S)
        label = {'terms': '이용약관', 'privacy': '개인정보처리방침'}[key]
        parts.append(f'<dialog class="legal-dlg" id="legal-{key}" aria-labelledby="legal-{key}-t">'
                     f'<div class="lg-head"><h2 id="legal-{key}-t">{label}</h2>'
                     f'<button type="button" class="lg-x" aria-label="닫기">&times;</button></div>'
                     f'<div class="lg-body">{body}</div></dialog>')
    parts.append(JS)
    return '\n'.join(parts)


if __name__ == '__main__':
    for fn in ('terms.mdx', 'privacy.mdx'):
        t, b = mdx_to_html(os.path.join(HERE, 'legal', fn))
        print(fn, t, len(b), b.count('<h3>'), 'h3', b.count('<ol>'), 'ol', b.count('<table'), 'table')
