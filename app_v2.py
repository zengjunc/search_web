import gradio as gr
from datetime import datetime
import json
import os
import matplotlib
matplotlib.use('agg')

# 搭载星火
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

# 星火认知大模型Spark Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v4.0/chat'
# 星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
SPARKAI_APP_ID = 'XXXXXXXXXX'
SPARKAI_API_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
SPARKAI_API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
# 星火认知大模型Spark Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_DOMAIN = '4.0Ultra'

class MyApp:
    def __init__(self):
        self.file_path = "websites.json"
        self.websites = self.load_websites()
        self.log = ""
        self.spark = ChatSparkLLM(
            spark_api_url=SPARKAI_URL,
            spark_app_id=SPARKAI_APP_ID,
            spark_api_key=SPARKAI_API_KEY,
            spark_api_secret=SPARKAI_API_SECRET,
            spark_llm_domain=SPARKAI_DOMAIN,
            streaming=False,
        )

    def load_websites(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_websites(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.websites, f, ensure_ascii=False, indent=4)

    def add_log(self, log):
        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
        self.log = formatted_now + ": " + log + "\n" + self.log

    def search_web(self, query):
        results = []
        for site in self.websites:
            if (query.lower() in site["网址"].lower() or
                    any(query.lower() in item.lower() for item in site["重点"]) or
                    query.lower() in site["介绍"].lower() or
                    query.lower() in site["领域"].lower() or
                    any(query.lower() in tag.lower() for tag in site["魔法标签"])):
                results.append(site)

        if results:
            self.add_log(f"搜索关键词 '{query}' 找到 {len(results)} 个结果")
        else:
            self.add_log(f"搜索关键词 '{query}' 未找到结果")

        return results

    def add_web(self, url, keynote, introduce, field, magic_tags):
        new_site = {
            "网址": url,
            "重点": keynote,
            "介绍": introduce,
            "领域": field,
            "魔法标签": magic_tags
        }
        self.websites.append(new_site)
        self.save_websites()  # 保存数据
        self.add_log(f"添加网站 {url}")

    def delete_web(self, url):
        initial_length = len(self.websites)
        self.websites = [site for site in self.websites if site["网址"] != url]

        if len(self.websites) < initial_length:
            self.save_websites()  # 保存数据
            self.add_log(f"删除网站 {url}")
            return f"网站 {url} 已删除。"
        else:
            self.add_log(f"未找到要删除的网站 {url}")
            return f"未找到网站 {url}。"

    def display_log(self):
        return self.log

    def display_websites(self):
        return '\n'.join([site['网址'] for site in self.websites])

    # 通用对话
    def chat(self, chat_query, chat_history):
        # 非流式调用，结果一次性输出，用户体验不佳，但性能要求低

        # 添加历史聊天
        prompts = []

        # 添加最新问题
        prompts.append(ChatMessage(role='user', content=chat_query))

        # 输出调试信息，检查 prompts 是否正确
        print(f"Prompts: {prompts}")

        # 将问题设为历史对话
        chat_history.append((chat_query, ''))
        # 进行对话生成
        try:
            # handler = ChunkPrintHandler()
            # for chunk_text in self.spark.generate([prompts], callbacks=[handler]):
            #     # 总结答案
            #     print(f"chunk_text: {chunk_text}")
            #     answer = chat_history[-1][1] + chunk_text
            #     # 替换最新的对话内容
            #     chat_history[-1] = (chat_query, answer)
            #     # 返回
            #     yield '', chat_history

            chunk_text = self.spark.generate([prompts])  # 返回的元组
            chunk_text2 = chunk_text.generations[0][0].text  # 回答
            chunk_text3 = chunk_text.llm_output  # token用量

            print(f"chunk_text: {chunk_text}")
            print(f"chunk_text2: {chunk_text2}")
            print(f"chunk_text3: {chunk_text3}")

            print(f"chat_history: {chat_history}")
            print(f"chat_history[-1][1]: {chat_history[-1][1]}")
            # 总结答案
            answer = chat_history[-1][1] + chunk_text2
            # 替换最新的对话内容
            print(f"answer: {answer}")
            chat_history[-1] = (chat_query, answer)
            print(f"chat_history[-1]: {chat_history[-1]}")
            # 返回
            yield '', chat_history

        except ValueError as e:
            print(f"Error during message conversion: {e}")
            raise


app = MyApp()

with gr.Blocks(title='功能网站检索') as demo:
    gr.HTML("""
        <div class="hint" style="text-align: center;background-color: rgba(255, 255, 0, 0.15); padding: 10px; margin: 10px; border-radius: 5px; border: 1px solid #ffcc00;">
            <p>这里是常用网站合集（个人使用版本），可用于保存自己常用网址，在有使用需求时快速检索</p>
        </div>
    """)

    with gr.Tab("搜索网站"):
        query_input = gr.Textbox(label="搜索关键词")
        search_button = gr.Button("搜索")
        results_output = gr.HTML(label="搜索结果")  # 用HTML显示结果

        def format_result(result):
            url = result['网址']
            keynote = ', '.join(result['重点'])
            introduce = result['介绍']
            field = result['领域']
            magic_tags = ', '.join(result['魔法标签'])
            return f"""<div style='margin: 10px; padding: 10px; border: 1px solid #ccc; border-radius: 5px;'>
                          <a href='{url}' target='_blank' style='font-size: 18px; font-weight: bold;'>{url}</a>
                          <p style='font-size: 14px; color: #555;'><strong>重点:</strong> {keynote}</p>
                          <p style='font-size: 14px; color: #555;'><strong>介绍:</strong> {introduce}</p>
                          <p style='font-size: 14px; color: #555;'><strong>领域:</strong> {field}</p>
                          <p style='font-size: 14px; color: #555;'><strong>魔法标签:</strong> {magic_tags}</p>
                       </div>"""

        def display_search_results(query):
            results = app.search_web(query)
            if results:
                return '\n'.join([format_result(result) for result in results])
            else:
                return "未找到相关结果。"

        search_button.click(fn=display_search_results, inputs=query_input, outputs=results_output)

    with gr.Tab("添加网站"):
        url_input = gr.Textbox(label="网址")
        keynote_input = gr.Textbox(label="重点", placeholder="用逗号分隔")
        introduce_input = gr.Textbox(label="介绍")
        field_input = gr.Textbox(label="领域")
        magic_tags_input = gr.Textbox(label="魔法标签", placeholder="√或×")
        add_button = gr.Button("添加")
        add_log_output = gr.Textbox(label="操作日志", interactive=False)

        def add_website(url, keynote, introduce, field, magic_tags):
            app.add_web(url, keynote.split(','), introduce, field, magic_tags.split(','))
            return app.display_log()

        add_button.click(fn=add_website,
                         inputs=[url_input, keynote_input, introduce_input, field_input, magic_tags_input],
                         outputs=add_log_output)

    with gr.Tab("管理网站"):
        manage_output = gr.Textbox(label="网站列表", interactive=False)
        manage_button = gr.Button("显示所有网站")

        manage_button.click(fn=app.display_websites, inputs=[], outputs=manage_output)

        delete_url_input = gr.Textbox(label="要删除的网址")
        delete_button = gr.Button("删除网站")
        delete_output = gr.Textbox(label="删除结果", interactive=False)
        delete_button.click(fn=lambda url: app.delete_web(url), inputs=delete_url_input, outputs=delete_output)

    with gr.Tab("AI助手"):
        # 聊天对话框
        chatbot = gr.Chatbot([], elem_id="chat-box", label="聊天历史")
        # 输入框
        chat_query = gr.Textbox(label="输入问题", placeholder="输入需要咨询的问题")
        # 按钮
        llm_submit_tab = gr.Button("发送", visible=True)
        # 问题样例
        gr.Examples(["请搜索一些关于剪辑学习的网站", "如何学习python？", "请介绍一下gradio官方文档"],
                    chat_query)
        # 通用对话按钮
        llm_submit_tab.click(fn=app.chat, inputs=[chat_query, chatbot], outputs=[chat_query, chatbot])

if __name__ == "__main__":
    demo.launch()
