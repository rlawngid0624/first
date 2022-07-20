import streamlit as st

st.subheader('2. radio button test')
food = st.radio(
     "좋아하는 음식은 무엇인가요?",
     ('초밥', '짜장면', '김치볶음밥'))

if food == '초밥':
    st.write('You selected 초밥.')
elif food == '짜장면':
    st.write('You selected 짜장면.')
elif food == '김치볶음밥':
    st.write('You selected 김치볶음밥')