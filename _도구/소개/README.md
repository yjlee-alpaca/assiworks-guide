# 소개 페이지 빌드

원본은 Claude 디자인 캔버스(어시웍스 소개, https://claude.ai/artifact/HUUjKjyYUHGVWYbEaRpEPj)입니다.
여기 `project/Main.dc.html` 은 그 조직용 원본의 사본입니다. 캔버스를 고쳤으면 먼저 이 파일을 캔버스 내용으로 바꿉니다.

이 폴더에서 차례로 돌립니다.

1. `python3 personal.py` : 조직용 원본에서 개인용 `project/Personal.dc.html` 을 만듭니다. 팀 관리 내용을 빼고 문구를 바꿉니다. 원본 문구가 바뀌어 치환할 자리를 못 찾으면 멈춥니다.
2. `python3 build_html.py ../../business.html site` : 조직용 사이트 파일
3. `SRC=project/Personal.dc.html python3 build_html.py ../../personal.html site` : 개인용 사이트 파일
4. iCloud 01_기획문서 사본은 `site` 없이 같은 명령으로 만듭니다. 링크가 사이트 전체 주소로 남습니다.

로고, 아이콘, 서체는 프로토타입 저장소(New-assi-works-front/src/assets)에서 읽어 파일 안에 넣습니다.
넘기기 전에 저장소 맨 위에서 `python3 _도구/verify.py business.html personal.html` 을 돌립니다.
