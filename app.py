import gradio as gr
from datetime import datetime
import json
import os
import matplotlib
matplotlib.use('agg')

class MyApp:
    def __init__(self):
        self.file_path = "websites.json"
        self.websites = self.load_websites()
        self.log = ""

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

app = MyApp()

with gr.Blocks(title='功能网站检索') as demo:
    gr.HTML("""
        <div class="hint" style="text-align: center;background-color: rgba(255, 255, 0, 0.15); padding: 10px; margin: 10px; border-radius: 5px; border: 1px solid #ffcc00;">
            <p>这里是常用网站合集</p>
        </div>
    """)

    with gr.Tab("搜索网站"):
        query_input = gr.Textbox(label="搜索关键词")
        search_button = gr.Button("搜索")
        results_output = gr.Textbox(label="搜索结果", interactive=False)
        search_button.click(fn=lambda query: '\n'.join([
            f"网址: {site['网址']}, 重点: {', '.join(site['重点'])}, 介绍: {site['介绍']}, 领域: {site['领域']}, 魔法标签: {', '.join(site['魔法标签'])}"
            for site in app.search_web(query)]), inputs=query_input, outputs=results_output)

    with gr.Tab("添加网站"):
        url_input = gr.Textbox(label="网址")
        keynote_input = gr.Textbox(label="重点", placeholder="用逗号分隔")
        introduce_input = gr.Textbox(label="介绍")
        field_input = gr.Textbox(label="领域")
        magic_tags_input = gr.Textbox(label="魔法标签")
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

if __name__ == "__main__":
    demo.launch()
