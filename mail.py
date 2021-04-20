import imaplib
import email
from email.header import decode_header
import re
import csv

# 저장할 csv 파일 만들어주
f = open('pair_feedback.csv', 'w', newline='')
write = csv.writer(f)
write.writerow(['#', '페어 이름', '스프린트', '잘한 점', '개선할 점', '메일 제목', '수신 일시'])

# User Credentials
user = "##########"
password = "##########"  # 2단계 인증 설정된 사용자의 경우 앱 비밀번호 생성해야

# Connect to the IMAP server
imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login(user, password)

# status = message that indicates whether we received the message successfully
# messages = number of total messages in the folder
imap.select("inbox")  # ('OK', [b'25425'])
status, messages = imap.uid('search', None, '(FROM "notifications@typeform.com")')
messages = messages[0].split()  # list of all message ids

for n, message in enumerate(messages):

    res, msg = imap.uid('fetch', message, git "(RFC822)")  # Standard format for fetching email message
    raw = msg[0][1]
    email_message = email.message_from_bytes(raw)  # type(email_message) == <class 'email.message.Message'>

    # decode 'from', 'date' info
    From, _ = decode_header(email_message.get("From"))[0]  # [0] 안 붙이면 [('notifications@typeform.com', None)]
    date, _ = decode_header(email_message.get("Date"))[0]  # [0] 안 붙이면 = [('Thu, 08 Apr 2021 05:10:04 +0000', None)]

    # decode 'subject' info
    subject, encoding = decode_header(email_message["Subject"])[0]
    subject = subject.decode(encoding)  # 한국어로 디코딩하는 작업

    # email_message.get_content_type() == 'text/html'

    body = email_message.get_payload(decode=True).decode()
    body = body[:body.rindex('<br/>')].replace('<br/>', ' ')

    regex_dict = {
        'sprint': '\[[\D]+\]',  # 대괄호 안이 Whitespace 가 아닌
        'awesome': '[가-힣]+님이\s평가한\s[가-힣]+님의\s잘한\s점:',  # 한글 이름 + 기존 문장 값
        'improve': '[가-힣]+님이\s생각한\s[가-힣]+님의\s개선하면\s좋을\s점:'  # 한글 이름 + 기존 문장 값
    }

    index_dict = {}

    for key, value in regex_dict.items():
        reg = re.compile(value, re.M)
        match = reg.search(body)
        index_dict[f'startindex_{key}'] = match.start()
        index_dict[f'endindex_{key}'] = match.end()

    sprint = body[index_dict['startindex_sprint']:index_dict['startindex_awesome']]
    is_awesome = body[index_dict['endindex_awesome']:index_dict['startindex_improve']]
    to_improve = body[index_dict['endindex_improve']:]

    write.writerow([n, 'pair name', sprint, is_awesome, to_improve, subject, date])

f.close()
imap.close()
imap.logout()

