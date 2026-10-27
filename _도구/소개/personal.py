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
rep('<a class="navlink" href="#roles">앱과 팀</a>', '<a class="navlink" href="#roles">만들고 사용하기</a>')
rep('<a class="btn btn-k" href="#contact" style="height:40px;font-size:15px;padding:0 18px">도입 문의</a>',
    '<a class="btn btn-k" href="https://assiworks.aifactory.space" style="height:40px;font-size:15px;padding:0 18px">시작하기</a>')
# 첫 화면
rep('업무에 맞게 만드는 AI 플랫폼', '내 업무에 맞춰 직접 만드는 AI 업무 도구')
rep('반복 업무는 AI에게,<br>중요한 판단은 사람에게.</h1>', '반복되는 일은 줄이고,<br>중요한 일에 집중하세요.</h1>')
rep('자료 검색부터 이력 비교, 보고서 작성까지 필요한 업무를 AI 유닛으로 자동화할 수 있습니다. 유닛은 직접 만들 수도 있고, 어시웍스에 맡길 수도 있습니다. 완성된 유닛은 대화창에서 간편하게 사용할 수 있습니다.', '자료 검색부터 내용 정리, 문서 작성까지 반복되는 업무를 AI 유닛에 맡길 수 있습니다. 필요한 유닛을 직접 만들거나 제작을 맡기고, 대화창에서 간편하게 사용할 수 있습니다.')
rep('<a class="btn btn-p" href="#contact">도입 상담 신청 <span aria-hidden="true">→</span></a>', '<a class="btn btn-p" href="https://assiworks.aifactory.space">시작하기 <span aria-hidden="true">→</span></a>')
rep('aria-label="팀원이 난간 사진과', 'aria-label="사용자가 난간 사진과')
rep('<span style="margin-left:auto;font-size:12px;font-weight:600;color:#525264;background:#F4F4F5;border-radius:6px;padding:4px 8px">업무1팀</span>', '')
rep('<span style="color:#71717B;font-size:11px">업무1팀</span>', '<span style="color:#71717B;font-size:11px">개인</span>')
# 만들고 사용하기 (조직용의 앱과 팀)
rep('<p style="margin:0;font-size:15px;font-weight:600;color:#71717B">앱과 팀</p>', '<p style="margin:0;font-size:15px;font-weight:600;color:#71717B">만들고 사용하기</p>')
rep('조직에서는 관리자가 앱을 구성하고 팀별 사용 권한을 설정해, 구성원에게 필요한 기능을 제공할 수 있습니다.', '만든 화면에서 사용해도 되고, 대화형 화면만 열어 두고 대화에서 바로 사용해도 됩니다.')
rep('>관리자</span><span style="font-size:15px;color:#71717B">팀장, 운영 담당</span>', '>만드는 화면</span><span style="font-size:15px;color:#71717B">Admin</span>')
rep('팀 업무에 맞는 유닛을 만들고,<br>앱에 담아 팀에 나눠 줍니다', '필요한 유닛을 만들고,<br>그 자리에서 바로 실행합니다')
rep('>Settings › 팀</span><span style="font-size:16px;font-weight:500;color:#1B1B1B">팀마다 사용할 앱과 팀원 지정', '>Schedules</span><span style="font-size:16px;font-weight:500;color:#1B1B1B">정기 실행 예약')
rep('>팀원</span><span style="font-size:15px;color:#B4B4BC">지정받은 앱을 사용하는 사람', '>사용하는 화면</span><span style="font-size:15px;color:#B4B4BC">대화형 화면')
rep('앱 주소로 들어와<br>대화로 일을 맡깁니다', '만들어 둔 유닛을<br>대화에서 바로 사용합니다')
# 운영: 팀별 권한 칸을 빼고 3열로
lines = t.split('\n')
i = [k for k, l in enumerate(lines) if l.startswith('<div class="rv op d3"')]
assert len(i) == 1 and '팀별 권한' in lines[i[0]]
del lines[i[0]]
t = '\n'.join(lines)
k = t.index('<div class="rv op d1"'); g = t.rindex('<div class="g4">', 0, k)
t = t[:g] + '<div class="g4 g3">' + t[g + len('<div class="g4">'):]
rep('>내부 자료 연결</span><span style="font-size:15px;line-height:1.65;color:#525264">기관 내부 데이터 저장소를 연결하고,', '>내 자료 연결</span><span style="font-size:15px;line-height:1.65;color:#525264">사용하던 데이터 저장소를 연결하고,')
rep('베이스맵 위에 기관 자료를 켜고 끕니다', '베이스맵 위에 내 지도 자료를 켜고 끕니다')
# ── 개인용 시나리오: 시설물 점검 대신 회의 메모 정리 ──
def swap(a, b):
    global t
    assert t.count(a) >= 1, ('없음', a[:60])
    t = t.replace(a, b)
# 어시지오는 개인용에서 뺀다
i = t.index('<!-- ═══ 어시지오 ═══ -->'); j = t.index('</section>', i) + len('</section>\n\n')
t = t[:i] + t[j:]
rep('<a class="navlink" href="#geo">어시지오</a>\n', '')
# 첫 화면: 사진, 질문, 도우미 말
i = t.index('class="a-photo"'); a = t.index('<svg', i); b = t.index('</svg>', a) + 6
t = t[:a] + ('<svg width="240" height="150" viewBox="0 0 200 118" style="position:absolute;inset:0"><rect width="200" height="118" fill="#E7E3DC"></rect>'
  '<g transform="rotate(-4 46 44)"><rect x="18" y="16" width="56" height="56" rx="3" fill="#FFE58A"></rect><g stroke="#8A7A3A" stroke-width="2.4" stroke-linecap="round"><line x1="26" y1="30" x2="64" y2="30"></line><line x1="26" y1="40" x2="56" y2="40"></line><line x1="26" y1="50" x2="60" y2="50"></line></g></g>'
  '<g transform="rotate(3 114 48)"><rect x="86" y="20" width="56" height="56" rx="3" fill="#FFC9D6"></rect><g stroke="#8A4A5A" stroke-width="2.4" stroke-linecap="round"><line x1="94" y1="34" x2="132" y2="34"></line><line x1="94" y1="44" x2="124" y2="44"></line></g></g>'
  '<g transform="rotate(-2 163 59)"><rect x="140" y="36" width="48" height="48" rx="3" fill="#C8EBD9"></rect><g stroke="#3F7A62" stroke-width="2.4" stroke-linecap="round"><line x1="147" y1="50" x2="180" y2="50"></line><line x1="147" y1="60" x2="172" y2="60"></line></g></g>'
  '<rect x="82" y="14" width="66" height="68" rx="6" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-dasharray="5 4"></rect></svg>') + t[b:]
rep('A구역_3번_난간.jpg', '회의메모_1021.jpg')
rep('이 난간 보수해야 할까? 전에도 문제 있었는지 확인해 줘.', '이 메모 정리해 주고, 지난주 회의에서 정한 일이랑도 비교해 줘.')
rep('사진부터 확인하고, 지난 점검 기록을 찾아볼게요.', '메모부터 읽고, 지난 회의록을 찾아볼게요.')
rep('aria-label="사용자가 난간 사진과 함께 보수가 필요한지 묻자, 현장 점검 도우미가 장착된 Tool 다섯 개 가운데 사진 파손 확인과 점검 이력 조회를 골라 순서대로 실행하고 보수 요청을 권하는 답을 보냅니다. 결정은 담당자가 합니다."',
    'aria-label="사용자가 회의 메모 사진을 올리며 정리를 부탁하자, 회의 정리 도우미가 장착된 Tool 다섯 개 가운데 메모 사진 읽기와 지난 회의록 검색을 골라 순서대로 실행하고 이번 주 할 일을 정리해 답합니다. 무엇을 할지는 사용자가 정합니다."')
rep('<span class="nm">담당자 찾기</span><span class="tg">API</span>', '<span class="nm">일정 확인</span><span class="tg">API</span>')
rep('<span class="nm">규정 문서 검색</span><span class="tg">VDB</span>', '<span class="nm">메일 초안 작성</span><span class="tg">LLM</span>')
rep('<span class="nm">점검 이력 조회</span><span class="tg">DB</span>', '<span class="nm">지난 회의록 검색</span><span class="tg">VDB</span>')
rep('기록 3건</div>', '회의록 2건</div>')
rep('난간 하단 지지대에 <b style="font-weight:600;color:#1B1B1B">균열로 보이는 자국</b>이 있습니다. 같은 위치는 지난 4월 점검 때도 녹이 있었습니다. 두 번 연속 같은 자리에서 문제가 나와 보수 요청을 권합니다.',
    '새로 정한 일이 3개 있습니다. 지난주 회의에서 정한 일 가운데 <b style="font-weight:600;color:#1B1B1B">2개가 아직 끝나지 않았습니다</b>. 두 목록을 합쳐 이번 주 할 일로 정리하기를 권합니다.')
rep('보수 요청서 초안 만들기', '할 일 목록 만들기')
rep('점검 이력 3건 보기', '지난 회의록 2건 보기')
rep('어시웍스는 분석 결과와 근거를 제공하고, 담당자는 이를 검토해 보수 여부를 결정합니다', '어시웍스는 정리한 결과와 근거를 보여 주고, 무엇을 할지는 직접 정합니다')
rep('A구역 3번 난간 보수 여부', '10.21 회의 메모 정리')
rep('B구역 표지판 사진 확인', '프로젝트 일정 확인')
# 유닛과 Flow 예시
rep('시설물 점검 업무라면 이렇게 나뉩니다.', '회의와 보고 업무라면 이렇게 나뉩니다.')
rep('점검 자료가 들어오면 아래 순서로 처리합니다', '한 주 동안 쌓인 메모가 들어오면 아래 순서로 처리합니다')
rep('이전 점검 이력 조회', '지난 보고 조회')
rep('>사진 분석<', '>메모 읽기<')
rep('>점검 결과 요약<', '>한 주 요약<')
rep('파손이 나온 경우에만 담당자 확인 단계로 보내도록 조건을 걸 수 있습니다.', '끝나지 않은 일이 있는 경우에만 다음 주 할 일로 넘기도록 조건을 걸 수 있습니다.')
swap('월간 점검 보고서 정리', '월간 업무 보고서 정리')
swap('9월 시설별 점검 보고서', '9월 업무 보고서')
swap('월간 점검 보고서', '월간 업무 보고서')
# 예약
swap('주간 파손 점검', '주간 보고 정리')
rep('매주 월요일 09:00 · ', '매주 금요일 17:00 · ')
rep('지난주 들어온 점검 사진에서 파손 의심 지점 찾아줘', '이번 주 회의 메모 모아서 주간 보고 초안 만들어줘')
rep('10.26 (월) 09:00', '10.24 (금) 17:00')
rep('A구역 난간 2곳에서 파손 의심 지점을 찾았습니다', '끝나지 않은 일 2개를 다음 주 할 일로 넘겼습니다')
rep('B구역 표지판 사진 14장은 이상이 없습니다', '주간 보고 초안을 만들었습니다')
swap('10.19 09:04', '10.17 17:03')
# 운영 작은 화면
rep('<span style="flex:1;color:#525264">홍길동</span>', '<span style="flex:1;color:#525264">역할 지시문 수정</span>')
rep('<span style="flex:1;color:#525264">김철수</span>', '<span style="flex:1;color:#525264">Tool 추가</span>')
rep('<span style="flex:1;color:#525264">이영희</span>', '<span style="flex:1;color:#525264">처음 만듦</span>')
rep('점검 이력 DB', '내 드라이브')
rep('>점검 문서<', '>회의 메모<')
# 남은 이름 한꺼번에
swap('현장 점검 도우미', '회의 정리 도우미')
swap('사진 파손 확인', '메모 사진 읽기')
swap('점검 이력 조회', '지난 회의록 검색')
swap('점검 자료 처리', '주간 보고 작성')
left = [w for w in ('점검', '난간', '파손', '시설', '김철수', '이영희', 'A구역', 'B구역') if w in t] + (['어시지오'] if '어시지오' in t.split('</helmet>')[1] else [])
assert not left, left
# 마무리
rep('팀 업무 하나로<br>먼저 시작해 보세요', '내 업무 하나로<br>먼저 시작해 보세요')
rep('지금 반복하고 있는 업무 하나를 알려 주세요. 어시웍스로 자동화하는 방법을 함께 찾아 드립니다.', '매주 반복하는 일을 하나 골라 유닛으로 만들어 보세요. 처음부터 따라 하는 순서는 사용 가이드에 있습니다.')
rep('<a class="btn btn-p" href="mailto:contact@aifactory.page" style="margin-top:8px">도입 상담 신청 <span aria-hidden="true">→</span></a>',
    '<div style="display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin-top:8px"><a class="btn btn-p" href="https://assiworks.aifactory.space">시작하기 <span aria-hidden="true">→</span></a><a class="btn btn-g" href="https://assiworks-guide.vercel.app/usage" style="background:#FFFFFF">사용 가이드 보기</a></div>')
# 문의 메일: 개인용은 사용 문의만 남긴다
t, n = re.subn(r'<span>도입 문의 <a href="mailto:contact@aifactory.page"[^>]*>contact@aifactory.page</a></span>', '', t)
assert n == 1, n
assert '문의 메일' not in t and '업무1팀' not in t and '도입' not in t, [w for w in ('문의 메일','업무1팀','도입') if w in t]
open(out, 'w', encoding='utf-8').write(t)
print('ok', len(t))
