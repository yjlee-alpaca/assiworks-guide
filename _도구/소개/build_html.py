import re, base64, sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from legal import modal as legal_modal
src = open(os.environ.get('SRC','project/Main.dc.html'), encoding='utf-8').read()
A = '/Users/yeonjae/dev/New-assi-works-front/src/assets/'
blobs = {
 'Assi0ccfd3ed139be6e942f26de71d10270a'[4:]: (A+'logo-assiworks-symbol.svg','image/svg+xml'),
 'c7f7b7731a71ce37a9e932fbd1b4dee6': (A+'logo-assiworks.svg','image/svg+xml'),
 'c5b35a591e950ae63edf0068ac7e8d23': (A+'fonts/pretendard/woff2/PretendardVariable.woff2','font/woff2'),
 'bdf9836e234673c7eea7420d94fc42a2': (A+'icons/icon_tool_Selected.svg','image/svg+xml'),
 'f690464fec29a9ee86690e9ea81151f7': (A+'icons/icon_operator_Selected.svg','image/svg+xml'),
 '556ce54f9cc13c6ec7c14490ffcca18f': (A+'icons/icon_flow_Selected.svg','image/svg+xml'),
 'a6c7bff8d6a1e65f88482b40c9acfc28': (A+'icons/icon_loop_Selected.svg','image/svg+xml'),
}
TITLE = re.search(r'<title>(.*?)</title>', src).group(1)
style = re.search(r'<helmet>\s*<style>(.*?)</style>\s*</helmet>', src, re.S).group(1)
body = re.search(r'</helmet>(.*?)</x-dc>', src, re.S).group(1)
SCROLL_JS = '''<script>\n(function(){try{if(matchMedia('(prefers-reduced-motion: reduce)').matches||!('IntersectionObserver' in window))return;document.documentElement.classList.add('anim-on');var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:0.15,rootMargin:'0px 0px -8% 0px'});document.querySelectorAll('.rv').forEach(function(el){io.observe(el)})}catch(e){}try{var q=document.querySelector('.a-q');if(q&&q.getAnimations){var sync=function(){var ref=q.getAnimations().filter(function(a){return a.animationName==='k-q'})[0];if(!ref)return;document.querySelectorAll('.anim-in *').forEach(function(el){el.getAnimations().forEach(function(a){if(a!==ref&&a.animationName&&a.animationName.indexOf('k-')===0)a.currentTime=ref.currentTime})})};setTimeout(sync,400);q.addEventListener('animationiteration',function(e){if(e.target===q)sync()})}}catch(e){}})();\n</script>'''
out = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<style>{style}
html{{scroll-behavior:smooth}}
</style>
</head>
<body>{body}{SCROLL_JS}
{legal_modal()}</body>
</html>
'''
for bid,(path,mime) in blobs.items():
    data = base64.b64encode(open(path,'rb').read()).decode()
    out = out.replace('/_blob/'+bid, f'data:{mime};base64,{data}')
assert '/_blob/' not in out and 'x-dc' not in out and '{{' not in out
if len(sys.argv)>2 and sys.argv[2]=='site':
    out=out.replace('https://assiworks-guide.vercel.app/usage','/usage').replace('https://assiworks-guide.vercel.app/','/')
open(sys.argv[1],'w',encoding='utf-8').write(out)
print(len(out))
