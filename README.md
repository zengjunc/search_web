# 网站管理工具

这是一个使用Gradio库创建的简单网站管理工具。它允许用户搜索、添加和删除网站，并记录所有操作。

## 功能
![6c56e47180338df65a621656bf4eba2](https://github.com/user-attachments/assets/4f2a4e24-83e2-451c-9b44-a9d0da8f7f11)
![156f940b21bb9f57d739bdfe9944b4a](https://github.com/user-attachments/assets/438f067e-0f68-4678-ad1a-30be6871ce56)
![3f9de66a898db322b01b0e0ed6bd852](https://github.com/user-attachments/assets/b0ed8ff0-d7e2-4ac3-948e-06096d33d884)
![da96508b8ec66aaf3c8c1226db1cd78](https://github.com/user-attachments/assets/0d68c9d7-e72a-43c1-ad4f-44e43a93b458)

- 加载和保存网站数据
- 记录操作日志
- 搜索网站
- 添加网站
- 删除网站
- 显示操作日志和网站列表
- AI助手（调用星火的api），智能回答

## 使用方法

1. 确保已安装Gradio库和星火SDK。如果没有安装，请运行以下命令安装：

``` bash
pip install gradio
pip install --upgrade spark_ai_python
```

2. 运行以下命令启动网站管理工具：

```bash
python app.py  # 看具体的app版本名
```

3. 在浏览器中打开Gradio界面，使用工具提供的功能进行操作。

## 文件结构

- `app.py`: 主程序文件，包含Gradio界面的定义和逻辑。
- `websites.json`: 存储网站数据的JSON文件。
- `log.txt`: 存储操作日志的文本文件。

## 注意事项

- 请确保在运行程序之前，`websites.json`存在，并且具有适当的读写权限。
- 本程序仅用于学习和研究目的，请勿用于非法用途。

## 版权声明

本程序遵循MIT许可证发布。请参阅LICENSE文件了解更多信息。

---
