import os, django, time
import numpy as np
import gradio as gr
import random

os.environ['DJANGO_SETTINGS_MODULE'] = 'hackathon.settings'
django.setup()

import APP.chat, APP.layout


def main():
    price_current, price_predict, price_overall, temperature_now, wet, Co2, tree = load_data(None, False)
    with gr.Blocks(css=APP.layout.CSS()) as demo:

        with gr.Tab("Monitor"):
            with gr.Row():
                temperature_setting, temperature_now, wet, setting_enter, setting_edit = APP.layout.FEELING(temperature_now, wet)

            with gr.Row():
                price_overall = APP.layout.PRICE_his(price_overall)

            with gr.Row():
                with gr.Column():
                    price_current, price_predict = APP.layout.PRICE(price_current, price_predict)
                with gr.Column():
                    Co2, tree = APP.layout.ENVIRONMENT(Co2, tree)

        with gr.Tab("Chat"):
            with gr.Accordion("configuration", open=False):
                with gr.Row():
                    room_size, machine_power = APP.layout.CONFIG()
            chatbot = APP.chat.CHATBOT(room_size, machine_power)

        setting_enter.click(reloads_lock, inputs=None, outputs=[price_current, price_predict, price_overall, temperature_now, wet, Co2, tree, temperature_setting, setting_enter, setting_edit])
        setting_edit.click(reloads, inputs=None, outputs=[price_current, price_predict, price_overall, temperature_now, wet, Co2, tree, temperature_setting, setting_enter, setting_edit])

    demo.queue()
    demo.launch(share=True)


def load_data(reload, lock):
    price_current, price_predict = random.randrange(30, 80), random.randrange(30, 80)
    price_overall = [[int(i) for i in range(1, 32)], [int(i) for i in np.random.randint(19, 32, size=31)]]
    temperature_now, wet = 31, 70
    Co2, tree = random.randrange(0, 10), random.randrange(100, 300)
    if reload:
        price_current, price_predict = APP.layout.PRICE(price_current, price_predict)
        price_overall = APP.layout.PRICE_his(price_overall)
        temperature_setting, temperature_now, wet, setting_enter, setting_edit = APP.layout.FEELING(temperature_now, wet)
        Co2, tree = APP.layout.ENVIRONMENT(Co2, tree)
        temperature_setting, setting_enter, setting_edit = gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=False)
        return price_current, price_predict, price_overall, temperature_now, wet, Co2, tree, temperature_setting, setting_enter, setting_edit
    return price_current, price_predict, price_overall, temperature_now, wet, Co2, tree


def reloads_lock():
    return load_data(True, True)


def reloads():
    return load_data(True, False)




if __name__ == '__main__':
    main()
