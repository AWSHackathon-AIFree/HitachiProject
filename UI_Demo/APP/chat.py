from openai import OpenAI
import gradio as gr
import APP.models, APP.LLM_chat

client = OpenAI(api_key='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')


def CHATBOT(room_size, machine_power):
    chat_history = update_chat_history()
    chatbot = gr.Chatbot(chat_history, bubble_full_width=False,)
    chat_input = gr.MultimodalTextbox(interactive=True, file_types=None, placeholder="請輸入想詢問的內容", show_label=False)
    chat_msg = chat_input.submit(add_message, [chatbot, chat_input], [chatbot, chat_input])
    bot_msg = chat_msg.then(bot, chatbot, chatbot)
    bot_msg.then(lambda: gr.MultimodalTextbox(interactive=True), None, [chat_input])


def openai_chat(user_input):
    response = client.chat.completions.create(
        model='gpt-3.5-turbo-0125',
        messages=[{"role": "user", "content": user_input}],
        max_tokens=4096
    )
    return response.choices[0].message.content


def add_message(chats, message):
    if message["text"] is not None:
        chats.append((message["text"], None))
    return chats, gr.MultimodalTextbox(value=None, interactive=False)


def bot(chats):
    chat_user = chats[-1][0]
    #chat_system = openai_chat(chat_user)
    chat_system = APP.LLM_chat.launch(chat_user)
    chats[-1][1] = chat_system
    APP.models.chat_Model(chat_user=chat_user, chat_system=chat_system).save()
    chat_history = [[i['chat_user'], i['chat_system']] for i in
                    APP.models.chat_Model.objects.values('chat_user', 'chat_system')]
    return chat_history
    #yield chats


def update_chat_history():
    chat_history = [[i['chat_user'], i['chat_system']] for i in APP.models.chat_Model.objects.values('chat_user', 'chat_system')]
    return chat_history

