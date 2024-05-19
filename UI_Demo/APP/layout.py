import APP.monitor
import gradio as gr


def CONFIG(*args):
    room_size = gr.Textbox(label='坪數', scale=3)
    machine_power = gr.Textbox(label='冷氣瓦數', scale=3)
    # predict_btn = gr.Button('預測', elem_id="reload_button")
    return room_size, machine_power


def PRICE(*args):
    with gr.Column():
        price_current = gr.Textbox(f"$ {args[0]}", label='目前花費 / 天', elem_id="middle-textbox-left")
        price_predict = gr.Textbox(f"$ {args[1]}", label='花費預測 / 小時', elem_id="middle-textbox-left")
    return price_current, price_predict


def PRICE_his(*args):
    with gr.Row():
        price_overall = gr.HTML(HTML(args[0]))
    return price_overall


def FEELING(*args):
    temperature_setting = gr.Textbox(label="設定溫度 ('c)", lines=5, scale=4, elem_id="large-textbox-white", interactive=True)
    with gr.Column(scale=1):
        setting_enter = gr.Button("預測", scale=1)
        setting_edit = gr.Button("修改", scale=1, interactive=False)
    temperature_now = gr.Textbox(f"{args[0]} 'c", label="現在溫度", lines=5, scale=4, elem_id="large-textbox")
    wet = gr.Textbox(f"{args[1]} %", label="濕度", lines=5, scale=4, elem_id="large-textbox")
    return temperature_setting, temperature_now, wet, setting_enter, setting_edit


def ENVIRONMENT(*args):
    with gr.Column():

        Co2 = gr.Textbox(f"{args[0]}   kgCO2", label='碳排量計算', elem_id="middle-textbox")
        tree = gr.Textbox(f"{args[1]}  棵", label='我一共拯救了多少樹', elem_id="middle-textbox")
    return Co2, tree


def CSS():
    _ = """
    #large-textbox-white textarea {
        background-color: #4b5563;
        font-size: 66px !important;
        text-align: center !important;
    }
    #large-textbox textarea {
        font-size: 66px !important;
        text-align: center !important;
    }
    #middle-textbox-left textarea {
        font-size: 30px !important;
        text-align: left !important;
    }
    #middle-textbox textarea {
        font-size: 30px !important;
        text-align: center !important;
    }
    #middle-button button {
        border-radius: 12px;
    }
    .bubble-wrap {
    display: flex;
    flex-direction: column-reverse;
    overflow-y: auto;
    }
    """
    return _


def HTML(data):
    _ = f"""<div style='height: 300px;
                        width: 100%;
                        display: flex;
                        justify-content: center;
                        align-items: center;'>{APP.monitor.generate_line_plot(data)}</div>"""
    return _