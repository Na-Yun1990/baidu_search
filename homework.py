"""基于 Assistant 实现的文本计数智能助手

这个模块提供了一个智能文本计数助手，可以：
1. 通过自然语言进行文本分析
2. 支持多种交互方式（GUI、TUI、测试模式）
3. 支持文本字符数、单词数、行数统计等功能
"""

import os
import asyncio
from typing import Optional
# import dashscope
from qwen_agent.agents import Assistant
from qwen_agent.gui import WebUI

# dashscope.api_key = os.getenv('DASHSCOPE_API_KEY', '')  # 从环境变量获取 API Key
# dashscope.timeout = 30  # 设置超时时间为 30 秒

def init_agent_service():
    """初始化文本计数助手服务
    
    配置说明：
    - 使用 qwen-max 作为底层语言模型
    - 设置系统角色为文本分析助手
    - 配置文本计数 MCP 工具
    
    Returns:
        Assistant: 配置好的文本计数助手实例
    """
    # LLM 模型配置
    llm_cfg = {
        'model_server': 'http://localhost:1234/v1',  # base_url，也称为 api_base
        'api_key': 'lm-studio',
        'model': 'qwen/qwen3-1.7b',  # 使用标准命名格式的模型名称
        'temperature': 0.7,  # 设置生成文本的随机性
        'max_tokens': 2048,  # 设置最大响应长度
        'timeout': 60,  # 增加模型调用超时时间
        'retry_count': 3,  # 设置重试次数
        'stop': None,  # 设置停止词（如有需要）
        'stream': True,  # 是否启用流式输出
    }
    # 系统角色设定
    system = ('你是一个全能的智能助手，你可以帮助用户完成各种任务。'
              '你可以使用各种工具来完成各种任务。'
              '如果你不知道如何完成某个任务，你可以使用工具来解决。'
              '如果遇到无法解决的问题，请告诉我你不知道答案'
              '请使用中文回答我的问题。')
    # MCP 工具配置
    tools = [{
        "mcpServers": {
            "txt-counter": {
                "command": "python",
                "args": [r"C:\Users\nayun\Desktop\11-MCP与A2A的应用\CASE-MCP_Demo-1\txt_counter.py"],
                "port": 6277
            },
            "amap-maps": {
                "type": "sse",
                "url": "https://mcp.api-inference.modelscope.net/d0c82e28215740/sse"
            },
            "baidu-news": {
                "command": "python",
                "args": [r"C:\Users\nayun\Desktop\11-MCP与A2A的应用\baidu_news_mcp.py"],
                "port": 6278
            }
            

        }
    }]
    
    try:
        # 创建助手实例
        bot = Assistant(
            llm=llm_cfg,
            name='智能助手',
            description='非常有用的智能助手',
            system_message=system,
            function_list=tools,
        )
        print("助手初始化成功！")
        return bot
    except Exception as e:
        print(f"助手初始化失败: {str(e)}")
        raise

def test(query='帮我统计这段文本的字数：Hello World', file: Optional[str] = None):
    """测试模式
    
    用于快速测试单个查询
    
    Args:
        query: 查询语句，默认为简单的文本统计
        file: 可选的输入文件路径
    """
    try:
        # 初始化助手
        bot = init_agent_service()

        # 构建对话消息
        messages = []

        # 根据是否有文件输入构建不同的消息格式
        if not file:
            messages.append({'role': 'user', 'content': query})
        else:
            messages.append({'role': 'user', 'content': [{'text': query}, {'file': file}]})

        print("正在处理您的请求...")
        # 运行助手并打印响应
        for response in bot.run(messages):
            print('bot response:', response)
    except Exception as e:
        print(f"处理请求时出错: {str(e)}")

def app_tui():
    """终端交互模式
    
    提供命令行交互界面，支持：
    - 连续对话
    - 文件输入
    - 实时响应
    """
    try:
        # 初始化助手
        bot = init_agent_service()

        # 对话历史
        messages = []
        while True:
            try:
                # 获取用户输入
                query = input('user question: ')
                # 获取可选的文件输入
                file = input('file url (press enter if no file): ').strip()
                
                # 输入验证
                if not query:
                    print('user question cannot be empty！')
                    continue
                    
                # 构建消息
                if not file:
                    messages.append({'role': 'user', 'content': query})
                else:
                    messages.append({'role': 'user', 'content': [{'text': query}, {'file': file}]})

                print("正在处理您的请求...")
                # 运行助手并处理响应
                response = []
                for response in bot.run(messages):
                    print('bot response:', response)
                messages.extend(response)
            except Exception as e:
                print(f"处理请求时出错: {str(e)}")
                print("请重试或输入新的问题")
    except Exception as e:
        print(f"启动终端模式失败: {str(e)}")

def app_gui():
    """图形界面模式
    
    提供 Web 图形界面，特点：
    - 友好的用户界面
    - 预设查询建议
    - 智能文本分析
    """
    try:
        print("正在启动 Web 界面...")
        # 初始化助手
        bot = init_agent_service()
        # 配置聊天界面
        chatbot_config = {
            'prompt.suggestions': [
                '帮我统计这段文本的字数：Hello World',
                '计算下面这段文本的行数：\n第一行\n第二行\n第三行',
                '这段文本有多少个单词：The quick brown fox jumps over the lazy dog',
                '分析这段多语言文本：你好，世界！Hello World!',
                '统计下面文本的标点符号数量：Hello, World! How are you?',
                '帮我计算这段代码的行数：\ndef hello():\n    print("Hello")\n    return True',
                '这段文本中有多少个中文字符：你好，这是一段中文文本',
                '统计这段文本的空格数量：Hello  World   !',
                '计算这段文本的总字符数（包括空格和标点）',
                '分析这段文本的基本信息（字数、行数、单词数）',
                '搜索有关人工智能的最新新闻',
                '查找关于气候变化的新闻报道',
                '获取今天的科技新闻',
                '搜索体育新闻',
                '查询财经新闻头条'
            ]
        }
        
        print("Web 界面准备就绪，正在启动服务...")
        # 启动 Web 界面
        WebUI(
            bot,
            chatbot_config=chatbot_config
        ).run()
    except Exception as e:
        print(f"启动 Web 界面失败: {str(e)}")
        print("请检查网络连接和 API Key 配置")

if __name__ == '__main__':
    # 运行模式选择
    # test()           # 测试模式
    # app_tui()        # 终端交互模式
    app_gui()          # 图形界面模式（默认）