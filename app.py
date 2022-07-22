import streamlit as st
import sqlite3
import pandas as pd
import os.path
import googletrans
import urllib.request

con = sqlite3.connect('db.db')
cur = con.cursor()

def login_user(id, pw):
    cur.execute(f"SELECT * FROM users WHERE id = '{id}' and pwd = '{pw}'")
    return cur.fetchone()

menu = st.sidebar.selectbox('MENU', options=['로그인','회원가입','회원목록'])
functions = st.sidebar.selectbox('functions', options=['구글 번역기', '환율 계산기', '만족도 조사'])
if menu == '로그인':
    st.subheader('로그인')

    login_id = st.text_input('아이디', placeholder='아이디를 입력하세요')
    login_pw = st.text_input('비밀번호', placeholder='비밀번호를 입력하세요',type='password')

    login_btn = st.button('로그인')
    if login_btn:
        user_info = login_user(login_id,login_pw)
        file_name = './img/'+user_info[0]+'.jpg'

        if os.path.exists(file_name):
            st.sidebar.image(file_name)
            st.sidebar.write(user_info[4],'님, 환영합니다')
        else:
            st.sidebar.write(user_info[4],'님, 환영합니다')

if menu == '회원가입':
    st.info('다음 양식을 모두 입력 후 회원가입 버튼을 클릭하세요.')
    uid = st.text_input('아이디', max_chars=10)
    uname = st.text_input('이름', max_chars=10)
    upw = st.text_input('비밀번호', type='password')
    upw_chk = st.text_input('비밀번호 확인', type='password')
    uage = st.text_input('나이')
    ugender = st.radio('성별', options=['남', '여'], horizontal=True)

    ubtn = st.button('회원가입')

    if ubtn:
        if upw!=upw_chk:
            st.error('비밀번호가 일치하지 않습니다.')
            st.warning('비밀번호가 일치하지 않습니다.')
            st.stop()

        cur.execute(f"INSERT INTO users(id, pwd, gender, age, name ) VALUES (" f"'{uid}', '{upw}', '{ugender}','{uage}', '{uname}')")
        st.success('회원가입에 성공했습니다.')
        con.commit()

    st.subheader('회원가입')
if menu == '회원목록':
    st.subheader('회원목록')
    df = pd.read_sql("SELECT name,age,gender FROM users", con)
    st.dataframe(df)

if functions == '구글 번역기':
    st.subheader("구글 번역기")
    from_text = st.text_input("번역할 글", "안녕")
    btn_translate = st.button("번역하기")

    source = st.selectbox("나의 언어 (또는 자동)", ("auto", "en", "ko", "ja"))
    destination = st.selectbox("무슨 언어로 번역할지", ("en", "ko", "ja"))

    translator = googletrans.Translator()

    if btn_translate:  # 버튼 누르면

        if not source or source == "auto":  # 나의 언어 선택을 안했거나, "auto"이면
            src = translator.detect(from_text).lang  # 언어 감지하기
            source = src

        if not destination:  # 무슨 언어로 번역할지 선택을 안했으면
            destination = "en"  # 기본은 영어로 한다.


        result = translator.translate(
            from_text, dest=destination, src=source
        )
        st.success(result.text)

if functions == '환율 계산기':
    st.subheader("환율 계산기 입니다.")
    # 환율 정보를 불러오는 라인
    page = urllib.request.urlopen(
    "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%ED%99%98%EC%9C%A8")
    text = page.read().decode("utf8")
    # 시간 정보를 확인 합니다
    where = text.find('class="grp_info"> <em>')
    start_of_time = where + 22
    end_of_time = start_of_time + 16
    prin = text[start_of_time:end_of_time]
    st.subheader(prin, "의 KEB하나은행 환율정보 입니다.")
    # ==============돈 값을 가져오고 정수형으로 바꾸는 부분=================================
    # 위안
    cnywhere = text.find('<span>중국 <em>CNY</em></span></a></th> <td><span>')
    cnyletter = text[cnywhere + 48:cnywhere + 54]
    # 달러
    usdwhere = text.find('<span>미국 <em>USD</em></span></a></th> <td><span>')
    usdletter = text[usdwhere + 48] + text[usdwhere + 50:usdwhere + 56]
    # 엔
    jpywhere = text.find('<span>일본 <em>JPY 100</em></span></a></th> <td><span>')
    jpyletter = text[jpywhere + 52:jpywhere + 59]
    apple = jpyletter.replace("<", "")
    apple2 = apple.replace(",", "")
    # GBP
    gbpwhere = text.find('<span>영국 <em>GBP</em></span></a></th> <td><span>')
    gbpletter = text[gbpwhere + 48] + text[gbpwhere + 50:gbpwhere + 56]
    # EUR
    eurwhere = text.find('<span>유럽연합 <em>EUR</em></span></a></th> <td><span>')
    eurletter = text[eurwhere + 50] + text[eurwhere + 52:eurwhere + 58]
    # AUD
    audwhere = text.find('<span>호주 <em>AUD</em></span></a></th> <td><span>')
    audletter = text[audwhere + 48:audwhere + 54]
    # CAD
    cadwhere = text.find('<span>캐나다 <em>CAD</em></span></a></th> <td><span>')
    cadletter = text[cadwhere + 49:cadwhere + 55]
    # NZD
    nzdwhere = text.find('<span>뉴질랜드 <em>NZD</em></span></a></th> <td><span>')
    nzdletter = text[nzdwhere + 50:nzdwhere + 56]
    # ==============환율정보를 출력하는 부분 =======================================
    st.subheader("[USD],[JPY],[EUR],[CNY],[GBP],[AUD],[CAD],[NZD] 를 지원합니다. ")
    money = st.text_input("계산하시고자 하는 화폐의 종류를 대문자로 입력하세요 : ")
    money3 = st.text_input("얼마의 외화가 필요하신가요? :")
    dsbtn = st.button('계산하기')
    money2 = 1
    if money == "USD":
        money2 = usdletter
    elif money == "JPY":
        money2 = jpyletter
    elif money == "EUR":
        money2 = eurletter
    elif money2 == "CNY":
        money2 = cnyletter
    elif money2 == "GBP":
        money2 = gbpletter
    elif money == "AUD":
        money2 = audletter
    elif money == "CAD":
        money2 = cadletter
    elif money == "NZD":
        money2 = nzdletter
    st.subheader(float(money3) * float(money2))