# Completed:
- Obtain email from Gmail via IMAP server 
- Decode email contents (Encoded in utf-8)
- Trim unnecessary contents of email
- Write contents on CSV file
- Add name variable
- Optimize code

# In Progress:
- Optimize date
- Update file when new mail comes

# test

## 실행 전 안내사항
- user 정보를 잘 입력해주어야 함. 이메일, 비밀번호
- 지메일 2단계 인증 설정된 경우 앱 비밀번호 생성해야 함 
Google 계정 고객센터: 앱 비밀번호로 로그인
https://support.google.com/accounts/answer/185833?hl=ko
- csv 파일이 저장되는 경로는 mail.py 파일 경로와 동일함. 다른 곳에 저장하기 원한다면 경로 변경해주면 됨 


## 주의사항
- 메일함 선택 가능. 레퍼런스 링크 4번 참조. but 전체 inbox 를 선택 시 속도 저하 있을 수 있음. 
- python version 2점대 사용 시 한글로 된 주석을 제대로 읽지 못함 (ASCII 인코딩으로 되어 있어서 그럼. 3점대부터는 utf-8 로 인코딩되어 작동됨) 따라서 파이썬 버전을 3번대로 변경해주길 바람 
[How to set Python3 as a default python version on MacOS?](https://dev.to/malwarebo/how-to-set-python3-as-a-default-python-version-on-mac-4jjf)

### Reference:
1. [How to Read Emails in Python](https://www.thepythoncode.com/article/reading-emails-in-python)
2. [Python imaplib 을 통한 Gmail 읽기](https://its2eg.tistory.com/entry/Python-imaplib%EC%9D%84-%ED%86%B5%ED%95%9C-Gmail-%EC%9D%BD%EA%B8%B0)
3. [Fetch & Convert Email in Python Programming](https://www.youtube.com/watch?v=bbPwv0TP2UQ&t=554s&ab_channel=PythonCodex)
4. [IMAP Extensions](https://developers.google.com/gmail/imap/imap-extensions)


### Footnotes
- 메일의 첨부파일을 받아오고 싶다면 레퍼런스 링크 1번을 참고해주세요 (**"attachment" in content_disposition** 부분)