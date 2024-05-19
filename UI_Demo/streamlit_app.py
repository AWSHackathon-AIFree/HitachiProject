import streamlit as st
import pandas as pd
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application
import os, sys

import APP.chat, APP.models

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hackathon.settings")
application = get_wsgi_application()

def main():

    if 'chat' not in st.session_state:
        st.session_state.chat = False
    if 'monitor' not in st.session_state:
        st.session_state.monitor = False

    def chat_button():
        st.session_state.chat = True
        st.session_state.monitor = False

    def monitor_button():
        st.session_state.chat = False
        st.session_state.monitor = True

    monitor_btn = st.button('monitor', on_click=monitor_button)
    chat_btn = st.button('chat', on_click=chat_button)

    st.markdown("---")

    if chat_btn or st.session_state.chat:
        chat_page(chat_button)
    if monitor_btn or st.session_state.monitor:
        monitor_page(monitor_button)


def monitor_page(monitor_button):
    st.title('monitor')

def chat_page(chat_button):
    st.title('chat')
    chat_history = [[i['chat_user'],
                    i['chat_system']] for i in APP.models.chat_Model.objects.values('chat_user', 'chat_system')]
    print(chat_history)

    with st.container(height=300):
        for message in chat_history:
            st.write('使用者: '+message[0])
            st.write('系統: '+message[1])

    user_input = st.text_input("chat", placeholder="請輸入想詢問的內容")
    user_sent = st.button("Send", on_click=chat_button)
    if user_sent:
        if user_input:
            APP.chat.openai_chat(user_input)
        else:
            st.error("Please enter a question.")


if __name__ == '__main__':
    main()
