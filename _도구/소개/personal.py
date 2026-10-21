# 조직용 원본(Main.dc.html)에서 개인용(Personal.dc.html)을 만든다. 팀 관리 내용만 빼고 문구를 바꾼다
import re, sys
src, out = 'project/Main.dc.html', 'project/Personal.dc.html'
t = open(src, encoding='utf-8').read()
def rep(a, b, n=1):
    global t
    c = t.count(a)
    assert c == n, (c, a[:80])
    t = t.replace(a, b)
rep('<title>어시웍스 소개</title>', '<title>어시웍스 개인용 소개</title>')
# 전환 스위치: 개인 쪽을 선택 상태로
rep('<a href="https://assiworks-guide.vercel.app/business" aria-current="page" style="padding:5px 12px;border-radius:999px;background:#FFFFFF;color:#1B1B1B;text-decoration:none;box-shadow:0 1px 2px rgba(27,27,27,0.08)">조직</a><a href="https://assiworks-guide.vercel.app/personal" style="padding:5px 12px;border-radius:999px;color:#71717B;text-decoration:none">개인</a>',
    '<a href="https://assiworks-guide.vercel.app/business" style="padding:5px 12px;border-radius:999px;color:#71717B;text-decoration:none">조직</a><a href="https://assiworks-guide.vercel.app/personal" aria-current="page" style="padding:5px 12px;border-radius:999px;background:#FFFFFF;color:#1B1B1B;text-decoration:none;box-shadow:0 1px 2px rgba(27,27,27,0.08)">개인</a>')
rep('<a class="navlink" href="#roles">앱과 팀</a>', '<a class="navlink" href="#roles">만들고 쓰기</a>')
rep('<a class="btn btn-g hide-sm" href="https://assiworks.aifactory.space" style="height:40px;font-size:15px;padding:0 16px">로그인</a>\n', '')
rep('<a class="btn btn-k" href="#contact" style="height:40px;font-size:15px;padding:0 18px">도입 문의</a>',
    '<a class="btn btn-k" href="https://assiworks.aifactory.space" style="height:40px;font-size:15px;padding:0 18px">시작하기</a>')
# 첫 화면
rep('기관과 기업 팀이 쓰는 AI 업무 플랫폼', '내 업무에 맞춰 직접 만드는 AI 업무 도구')
rep('관리자가 팀 업무에 맞는 유닛을 만들어 두면 팀원은 대화창에서 평소 쓰는 말로 요청합니다.', '필요한 유닛을 직접 만들어 두면 대화창에서 평소 쓰는 말로 일을 맡길 수 있습니다.')
rep('<a class="btn btn-p" href="#contact">도입 상담 신청 <span aria-hidden="true">→</span></a>', '<a class="btn btn-p" href="https://assiworks.aifactory.space">시작하기 <span aria-hidden="true">→</span></a>')
rep('aria-label="팀원이 난간 사진과', 'aria-label="사용자가 난간 사진과')
rep('<span style="margin-left:auto;font-size:12px;font-weight:600;color:#525264;background:#F4F4F5;border-radius:6px;padding:4px 8px">업무1팀</span>', '')
rep('<span style="color:#71717B;font-size:11px">업무1팀</span>', '<span style="color:#71717B;font-size:11px">개인</span>')
# 만들고 쓰기 (조직용의 앱과 팀)
rep('<p style="margin:0;font-size:15px;font-weight:600;color:#71717B">앱과 팀</p>', '<p style="margin:0;font-size:15px;font-weight:600;color:#71717B">만들고 쓰기</p>')
rep('조직에서는 관리자가 앱을 구성하고 팀별 사용 권한을 설정해, 구성원에게 필요한 기능을 제공할 수 있습니다.', '만든 화면에서 바로 써도 되고, 대화형 화면만 열어 두고 꺼내 써도 됩니다.')
rep('>관리자</span><span style="font-size:15px;color:#71717B">팀장, 운영 담당</span>', '>만드는 화면</span><span style="font-size:15px;color:#71717B">Admin</span>')
rep('팀 업무에 맞는 유닛을 만들고,<br>앱에 담아 팀에 나눠 줍니다', '필요한 유닛을 만들고,<br>그 자리에서 바로 실행합니다')
rep('>Settings › 팀</span><span style="font-size:16px;font-weight:500;color:#1B1B1B">팀마다 쓸 앱과 팀원 지정', '>Schedules</span><span style="font-size:16px;font-weight:500;color:#1B1B1B">정기 실행 예약')
rep('>팀원</span><span style="font-size:15px;color:#B4B4BC">지정받은 앱을 쓰는 사람', '>쓰는 화면</span><span style="font-size:15px;color:#B4B4BC">대화형 화면')
rep('앱 주소로 들어와<br>대화로 일을 맡깁니다', '만들어 둔 유닛을<br>대화로 꺼내 씁니다')
# 운영: 팀별 권한 칸을 빼고 3열로
lines = t.split('\n')
i = [k for k, l in enumerate(lines) if l.startswith('<div class="rv op d3"')]
assert len(i) == 1 and '팀별 권한' in lines[i[0]]
del lines[i[0]]
t = '\n'.join(lines)
k = t.index('<div class="rv op d1"'); g = t.rindex('<div class="g4">', 0, k)
t = t[:g] + '<div class="g4 g3">' + t[g + len('<div class="g4">'):]
rep('>내부 자료 연결</span><span style="font-size:15px;line-height:1.65;color:#525264">기관 내부 데이터 저장소를 연결하고,', '>내 자료 연결</span><span style="font-size:15px;line-height:1.65;color:#525264">쓰던 데이터 저장소를 연결하고,')
rep('베이스맵 위에 기관 자료를 켜고 끕니다', '베이스맵 위에 내 지도 자료를 켜고 끕니다')
# 마무리
rep('팀 업무 하나로<br>먼저 시작해 보세요', '내 업무 하나로<br>먼저 시작해 보세요')
rep('매주 반복되는 업무 하나를 알려 주시면, 어떤 유닛으로 나눠 만들 수 있는지 함께 살펴보겠습니다.', '매주 반복하는 일을 하나 골라 유닛으로 만들어 보세요. 처음부터 따라 하는 순서는 사용 가이드에 있습니다.')
rep('<a class="btn btn-p" href="#contact" style="margin-top:8px">도입 상담 신청 <span aria-hidden="true">→</span></a>',
    '<div style="display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin-top:8px"><a class="btn btn-p" href="https://assiworks.aifactory.space">시작하기 <span aria-hidden="true">→</span></a><a class="btn btn-g" href="https://assiworks-guide.vercel.app/usage" style="background:#FFFFFF">사용 가이드 보기</a></div>')
t = re.sub(r'\n<span style="font-size:14px;color:#71717B">문의 메일 .*?</span>', '', t, count=1)
assert '문의 메일' not in t and '업무1팀' not in t and '도입' not in t, [w for w in ('문의 메일','업무1팀','도입') if w in t]
open(out, 'w', encoding='utf-8').write(t)
print('ok', len(t))
