#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
百度新闻MCP服务器
提供百度新闻搜索功能的MCP服务器，可以被智能助手调用
"""

import os
import sys
import json
from typing import List, Dict, Optional
from mcp.server.fastmcp import FastMCP

# 确保可以导入百度新闻搜索模块
current_dir = os.path.dirname(os.path.abspath(__file__))
baidu_news_dir = os.path.join(current_dir, "baidu_news_cli")
sys.path.insert(0, baidu_news_dir)

# 导入百度新闻搜索器
from news_searcher import BaiduNewsSearcher

# 创建 MCP Server
mcp = FastMCP("百度新闻搜索服务")

# 创建搜索器实例
searcher = BaiduNewsSearcher(timeout=15, max_retries=3)

@mcp.tool()
def search_news(keywords: str, page: int = 1, num: int = 10) -> str:
    """搜索百度新闻
    
    Args:
        keywords: 搜索关键词
        page: 页码，默认为1
        num: 每页显示的结果数量，默认为10
        
    Returns:
        搜索结果的JSON字符串
    """
    try:
        # 执行搜索
        results = searcher.search(keywords, page=page)
        
        # 限制结果数量
        results = results[:num]
        
        # 返回JSON格式的结果
        return json.dumps(results, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "error": True,
            "message": f"搜索新闻时出错: {str(e)}"
        }, ensure_ascii=False)

@mcp.tool()
def get_news_details(keywords: str, page: int = 1, num: int = 10) -> str:
    """获取新闻详细信息
    
    Args:
        keywords: 搜索关键词
        page: 页码，默认为1
        num: 每页显示的结果数量，默认为10
        
    Returns:
        格式化的新闻详情字符串
    """
    try:
        # 执行搜索
        results = searcher.search(keywords, page=page)
        
        # 限制结果数量
        results = results[:num]
        
        if not results:
            return f"未找到与 '{keywords}' 相关的新闻。"
        
        # 格式化输出
        output = f"## 百度新闻搜索结果: {keywords}\n\n"
        output += f"找到 {len(results)} 条相关新闻：\n\n"
        
        for i, item in enumerate(results, 1):
            output += f"### {i}. {item['title']}\n"
            output += f"**链接**: {item['url']}\n"
            output += f"**摘要**: {item['summary']}\n"
            output += f"**来源**: {item.get('source', '未知')} | **时间**: {item.get('time', '未知')}\n\n"
            output += "---\n\n"
        
        return output
    except Exception as e:
        return f"获取新闻详情时出错: {str(e)}"

@mcp.tool()
def search_news_by_topic(topic: str, page: int = 1, num: int = 10) -> str:
    """按主题搜索百度新闻
    
    Args:
        topic: 新闻主题（如科技、体育、财经等）
        page: 页码，默认为1
        num: 每页显示的结果数量，默认为10
        
    Returns:
        格式化的新闻详情字符串
    """
    # 主题映射到关键词
    topic_keywords = {
        "科技": "科技 新闻",
        "体育": "体育 新闻",
        "财经": "财经 新闻",
        "娱乐": "娱乐 新闻",
        "教育": "教育 新闻",
        "健康": "健康 医疗 新闻",
        "军事": "军事 新闻",
        "社会": "社会 新闻",
        "国际": "国际 新闻",
        "国内": "国内 新闻"
    }
    
    # 获取对应的关键词
    keywords = topic_keywords.get(topic, f"{topic} 新闻")
    
    try:
        # 执行搜索
        results = searcher.search(keywords, page=page)
        
        # 限制结果数量
        results = results[:num]
        
        if not results:
            return f"未找到与主题 '{topic}' 相关的新闻。"
        
        # 格式化输出
        output = f"## {topic}新闻搜索结果\n\n"
        output += f"找到 {len(results)} 条相关新闻：\n\n"
        
        for i, item in enumerate(results, 1):
            output += f"### {i}. {item['title']}\n"
            output += f"**链接**: {item['url']}\n"
            output += f"**摘要**: {item['summary']}\n"
            output += f"**来源**: {item.get('source', '未知')} | **时间**: {item.get('time', '未知')}\n\n"
            output += "---\n\n"
        
        return output
    except Exception as e:
        return f"获取{topic}新闻时出错: {str(e)}"

if __name__ == "__main__":
    # 初始化并运行服务器
    mcp.run()