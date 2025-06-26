# 百度新闻搜索CLI程序

一个命令行界面(CLI)程序，允许用户输入关键词，从百度搜索相关新闻，并展示新闻的标题、摘要和链接。同时提供将搜索结果保存为JSON或CSV格式的功能。

## 功能特点

- 支持关键词搜索百度新闻
- 分页显示搜索结果
- 显示新闻标题、摘要、来源和发布时间
- 支持将结果保存为JSON或CSV格式
- 彩色输出，提升用户体验
- 内置反爬虫机制
- 支持自定义搜索页数和每页结果数

## 安装说明

1. 确保已安装Python 3.7或更高版本
2. 克隆或下载本项目
3. 进入项目目录
4. 安装依赖包：

```bash
pip install -r requirements.txt
```

## 使用方法

基本用法：

```bash
python main.py 搜索关键词
```

高级用法：

```bash
python main.py [-h] [-p PAGE] [-n NUM] [-s {json,csv,both}] [-o OUTPUT] [-d DELAY] keywords [keywords ...]
```

参数说明：

- `keywords`: 搜索关键词（必需）
- `-p`, `--page`: 要获取的页数（默认：1）
- `-n`, `--num`: 每页显示的结果数量（默认：10）
- `-s`, `--save`: 保存结果格式，可选 json、csv 或 both
- `-o`, `--output`: 输出文件名（不含扩展名，默认：baidu_news_results）
- `-d`, `--delay`: 请求之间的延迟时间(秒)（默认：1.0）
- `-h`, `--help`: 显示帮助信息

示例：

1. 简单搜索：
```bash
python main.py 人工智能
```

2. 获取多页结果：
```bash
python main.py -p 3 人工智能
```

3. 保存为JSON格式：
```bash
python main.py -s json -o ai_news 人工智能
```

4. 保存为CSV格式：
```bash
python main.py -s csv -o ai_news 人工智能
```

5. 同时保存为JSON和CSV：
```bash
python main.py -s both -o ai_news 人工智能
```

## 注意事项

1. 程序会自动处理反爬虫机制，但建议不要频繁请求
2. 默认每次请求之间有1秒延迟，可通过 `-d` 参数调整
3. 保存的文件会自动添加对应的扩展名（.json 或 .csv）
4. 如果遇到编码问题，请确保系统默认编码为UTF-8

## 错误处理

- 如果搜索请求失败，程序会自动重试（最多3次）
- 如果解析结果出错，程序会跳过问题条目并继续处理
- 所有错误都会有清晰的提示信息

## 开发环境

- Python 3.7+
- 依赖包版本信息见 requirements.txt

## 许可证

MIT License