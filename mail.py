from email.header import decode_header
from datetime import datetime
import imaplib, re, csv, email
import os
from dotenv import load_dotenv

# 저장할 csv 파일 만들기
f = open('pair_feedback.csv', 'w', newline='')
write = csv.writer(f)
write.writerow(['#', '날짜', '페어', '스프린트', '잘한 점', '개선할 점'])

# 유저 개인정보 (환경변수 설정)
load_dotenv()
user = os.environ.get('mail')  # 이메일 주소 (ex. abcde@gmail.com)
password = os.environ.get('password')  # 앱 비밀번호 (16자리)

# IMAP 서버에 연결하기
imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login(user, password)

# 접근하고자 하는 메일함 이름
imap.select("INBOX") # 예) "중요한 편지함" 선택 시 "[Gmail]/Important" 로 변경

# status = 이메일 접근 상태
# messages = 선택한 조건에 해당하는 메일의 id 목록
# ('OK', [b'00001 00002 .....'])
status, messages = imap.uid('search', None, '(FROM "notifications@typeform.com")')
messages = messages[0].split()

# 각 메일에 대하여 실행
for n, message in enumerate(messages):

    print(f"Writing email #{n} on file...")

    res, msg = imap.uid('fetch', message, "(RFC822)")  # Standard format for fetching email message
    raw = msg[0][1]
    email_message = email.message_from_bytes(raw)  # type(email_message) == <class 'email.message.Message'>

    # decode 'subject' info (메일 제목)
    subject, encoding = decode_header(email_message["Subject"])[0]
    subject = subject.decode(encoding)  # 한국어로 디코딩하는 작업
    print(subject)
    if 'Review' in subject:

        # decode 'date' (날짜) & format
        temp, _ = decode_header(email_message.get("Date"))[0]  # date = 'Thu, 08 Apr 2021 05:10:04 +0000'

        temp = datetime.strptime(temp, '%a, %d %b %Y %H:%M:%S %z')
        date = temp.strftime('%Y년 %m월 %d일')

        # subject 에서 페어 이름 추출
        match = re.search(r'[가-힣]+님의', subject)  # 'ㅇㅇㅇ님의' 문자열 추출
        pair = match.group()  # 매치된 문자열 받아서 pair 변수에 할당
        pair = pair[:-2]   # 이름만 남도록 슬라이싱

        # get mail body (메일 본문)
        # email_message.get_content_type() == 'text/html'

        body = email_message.get_payload(decode=True).decode()
        body = body[:body.rindex('<br/>')].replace('<br/>', ' ').replace('▶︎', '') # 이메일 내용 (body) 의 시작점부터 마지막 <br/> 이 등장하는 지점까지 추출 후, 모든 <br/> 을 공백으로 대체
        body = re.sub(r'<[^>]+>', '', body)

        temp_match = re.search(r'아직 [가-힣]+님에게', body)
        if temp_match: 
            temp_start, _ = temp_match.span()
            body = body[:temp_start]

        # body 에서 Sprint 내용 추출
        match = re.search(r'\[[\D]+\]', body) # 대괄호 안이 Whitespace 가 아닌 값 (예 : '[JS/Node]') 찾기
        sprint = match.group() if match else '[해당 없음]' # 매치된 문자열 받아서 sprint 변수에 할당

        # body 에서 잘한 점, 개선할 점 내용 추출
        match = re.search(r'[가-힣]+님이\s평가한\s[가-힣]+님의\s잘한\s점[ ]*:', body) # 한글 이름 + 기존 문장 내용 (예 : '김코딩님이 평가한 박해커님의 잘한 점:')
        start_awesome, end_awesome = match.span() # '...잘한 점:' 문자열의 시작과 끝 인덱스 추출

        match = re.search(r'[가-힣]+님이\s생각한\s[가-힣]+님의\s개선하면\s좋을\s점[ ]*:', body) # 한글 이름 + 기존 문장 내용 (예 : '김코딩님이 평가한 박해커님의 개선하면 좋을 점:')
        match = match if match else re.search(r'[가-힣]+님이\s평가한\s[가-힣]+님의\s개선할\s점[ ]*:', body) 
        start_improve, end_improve = match.span() # '...개선하면 좋을 점:' 문자열의 시작과 끝 인덱스 추출

        awesome = body[end_awesome:start_improve]
        improve = body[end_improve:]

        # csv 파일에 저장한 내용 쓰기
        write.writerow([n, date, pair, sprint, awesome, improve])

print("All complete!")
f.close()
imap.close()
imap.logout()

