from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import pandas as pd


def initial():
    # 初始化 ChatOpenAI
    chat = ChatOpenAI(
        model="anthropic.claude-3-sonnet-20240229-v1:0",
        temperature=0,
        openai_api_key='P3AsA2Fi6W3GiU7u1fsF92YtpNIHhXA37TkvLPXz',
        openai_api_base='http://Claude-Proxy-prCIrmYU8XNp-1214113462.us-west-2.elb.amazonaws.com/api/v1',
    )

    # 設定 Prompt 模板
    template = """以下是使用者的在12坪大的房間當中冷氣設定的溫度以及室內溫度的變化數據，需要考慮到房間大小。請詳細閱讀這些數據後給我以下三個你分析後得出使用者標籤，，除了這三個標籤外請你在自行發想額外三個，請使用繁體中文回覆。
    - 三個限制皆須提出數據支持
        1. **每日使用時段**：
        2. **平均使用時長**：
        3. **設定溫度偏好**：
    """

    # 設定初始的 Prompt 模板
    initial_prompt = PromptTemplate.from_template(template)
    llm_chain = LLMChain(prompt=initial_prompt, llm=chat)
    return chat, template, llm_chain


# 讀取 Excel 文件
def read_excel_file(file_path):
    df = pd.read_excel(file_path)
    return df


# 從 Excel 數據準備需要的內容
def prepare_data_from_excel(df):
    # 提取所需的數據
    data = df[[r'Time',
               r'Zone1 Air Temperature (F)',
               r'Zone1 Cooling Setpoint Temperature(F)']].to_dict(orient='records')

    return data


# 設定問題並將數據傳遞給模型
def analyze_initial_data(file_path, template, llm_chain):
    df = read_excel_file(file_path)
    data = prepare_data_from_excel(df)
    # 將數據添加道問題描述中
    question = template + "\n數據:\n" + str(data)
    response = llm_chain({'question': question})
    return response['text'].strip()


# # 使用者問題
# def chat_process(chat_user, user_labels):
#
#     return combined_llm_chain


# 設定問題並將數據傳遞給模型
def analyze_combined_data(file_path,combine_prompt,combined_llm_chain):
    df = read_excel_file(file_path)
    question = combine_prompt + str(df)
    response = combined_llm_chain({'question': question})
    return response['text'].strip()


def launch(chat_user):
    chat, template, llm_chain= initial()

    initial_excel_path = "./data/zone_1.xlsx"
    user_labels = analyze_initial_data(initial_excel_path, template, llm_chain)
    combined_excel_path = "./data/machine_data.xlsx"
    # machine_labels = analyze_initial_data(initial_excel_path)
    user_prompt = chat_user

    # 合併後的 Prompt 模板
    combine_prompt = f'''請你判斷現在使用者的問題屬於以下哪一種情境，注意"在回覆過程中不要提到你現在是情境一或二 !"，因為你背後運作的機制不需要讓使用者知道，並且只針對一種情境進行回覆：\n

        情境一： 如果我今天有詢問你購買冷氣的相關問題時，請你詳細閱讀下面我提供給你的數據，並且依據我的使用者習慣標籤{user_labels}，回答我這個問題：{user_prompt}。
        你現在是一位日立冷氣銷售專員，根據這個以下參考數據與你的專業知識，我今天希望買一台冷氣，
        你需要告訴我應該要選擇買數據中的哪一個型號的冷氣最好，需要明確說出冷氣型號，須考量到電價、節能面向、最快達到我所想要的舒適溫度，同時考量我的使用者習慣標籤：\n

        情境二： 如果我沒有提到情境一的購買問題，就請你扮演日立冷氣的 AI 客服名叫小幸，一開始請你先自我介紹一下，以下是我的使用標籤，需要你透過以下標籤來了解我的使用習慣：{'user_labels'}。
        ，我們未來的對話中你都需要參考這些標籤來回答我，最後一定要使用繁體中文回覆，絕對不能出現簡體中文字：\n
        '''

    # 設定合併後的 Prompt 模板
    combined_prompt = PromptTemplate.from_template(combine_prompt)
    combined_llm_chain = LLMChain(prompt=combined_prompt, llm=chat)

    result = analyze_combined_data(combined_excel_path, combined_prompt, combined_llm_chain)

    # combined_llm_chain = chat_process(chat_user, user_labels)

    return result


