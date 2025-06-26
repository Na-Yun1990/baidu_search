# baidu_search
这是一个mcp工具，用于让agent调用它，从百度搜索，获得用户指定的内容，然后转换为markdown文件形式展示给用户。由于没有使用收费的api，所以不知道后期频繁使用会不会被官方限制访问。

运行步骤：

1.下载并解压本项目

2.创建并运行python虚拟环境

  python -m venv .venv
  
  .venv\Scripts\activate

3.打开 homework.py 

  找到这行代码：
  
            "baidu-news": {
                "command": "python",
                "args": [r"C:\Users\nayun\Desktop\11-MCP与A2A的应用\baidu_news_mcp.py"],
                "port": 6278
            }

  修改这个代码为你的实际文件路径：
  
           "args": [r"C:\Users\nayun\Desktop\11-MCP与A2A的应用\baidu_news_mcp.py"]

4.安装 requirements.txt

5.运行 baidu_news_mcp.py 它是提供mcp服务的程序

6.运行例子：homework.py 这个是千问agent，调用本地的 lm_studio 上的大语言模型，并安装了baidu_search的mcp工具可以简单的跑一下看看效果

7.之后你就可以只运行 baidu_news_mcp.py
然后把

{
        "mcpServers": {
            "baidu-news": {
                "command": "python",
                "args": [r"C:\Users\nayun\Desktop\11-MCP与A2A的应用\baidu_news_mcp.py"],
                "port": 6278
            }
        }
    }

 加入到你自己的mcp工具中就可以让agent自动调用了


