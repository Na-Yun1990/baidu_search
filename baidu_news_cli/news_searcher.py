#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
百度新闻搜索模块
负责构建搜索URL、发送HTTP请求到百度新闻搜索，并处理可能的反爬虫机制
"""

import random
import time
import urllib.parse
import requests
from bs4 import BeautifulSoup

# 常用User-Agent列表，用于随机选择，减少被反爬的可能性
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
]


class BaiduNewsSearcher:
    """百度新闻搜索类"""
    
    def __init__(self, timeout=10, max_retries=3):
        """
        初始化搜索器
        
        Args:
            timeout (int): 请求超时时间（秒）
            max_retries (int): 最大重试次数
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        
        # 设置基本请求头
        self.session.headers.update({
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Referer": "https://www.baidu.com/",
        })
    
    def _get_random_user_agent(self):
        """随机获取一个User-Agent"""
        return random.choice(USER_AGENTS)
    
    def _build_search_url(self, keywords, page=1):
        """
        构建百度新闻搜索URL
        
        Args:
            keywords (str): 搜索关键词
            page (int): 页码
        
        Returns:
            str: 搜索URL
        """
        # 对关键词进行URL编码
        encoded_keywords = urllib.parse.quote(keywords)
        
        # 计算分页参数
        # 百度新闻的分页参数是pn，每页10条，从0开始
        pn = (page - 1) * 10
        
        # 构建URL
        url = f"https://news.baidu.com/ns?word={encoded_keywords}&pn={pn}&cl=2&ct=1&tn=news&rn=10&ie=utf-8&bt=0&et=0"
        
        return url
    
    def search(self, keywords, page=1):
        """
        执行百度新闻搜索
        
        Args:
            keywords (str): 搜索关键词
            page (int): 页码
        
        Returns:
            list: 搜索结果列表，每个结果是一个字典，包含标题、链接、摘要等信息
        """
        url = self._build_search_url(keywords, page)
        
        # 尝试发送请求，最多重试max_retries次
        for attempt in range(self.max_retries):
            try:
                # 更新User-Agent
                self.session.headers.update({"User-Agent": self._get_random_user_agent()})
                
                # 发送请求
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()  # 如果状态码不是200，抛出异常
                
                # 确保响应内容是UTF-8编码
                response.encoding = 'utf-8'
                
                # 解析搜索结果
                return self._parse_search_results(response.text)
                
            except requests.RequestException as e:
                if attempt < self.max_retries - 1:
                    # 如果不是最后一次尝试，等待一段时间后重试
                    wait_time = (attempt + 1) * 2  # 指数退避
                    time.sleep(wait_time)
                else:
                    # 如果是最后一次尝试，抛出异常
                    raise Exception(f"搜索请求失败: {str(e)}")
    
    def _parse_search_results(self, html_content):
        """
        解析百度新闻搜索结果HTML
        
        Args:
            html_content (str): HTML内容
        
        Returns:
            list: 搜索结果列表
        """
        soup = BeautifulSoup(html_content, 'lxml')
        results = []
        
        # 尝试多种可能的选择器来适应百度新闻的不同版本
        possible_selectors = [
            'div.result', 'div.news-item', 'div.c-container', 
            'div[class*="result"]', 'div[class*="news"]'
        ]
        
        news_items = []
        for selector in possible_selectors:
            items = soup.select(selector)
            if items:
                news_items = items
                print(f"找到 {len(items)} 条新闻，使用选择器: {selector}")
                break
        
        if not news_items:
            # 如果没有找到任何新闻条目，尝试查找所有可能包含新闻的div
            print("未找到新闻条目，尝试查找所有可能的新闻div...")
            all_divs = soup.find_all('div', class_=True)
            for div in all_divs:
                class_name = ' '.join(div.get('class', []))
                if any(keyword in class_name.lower() for keyword in ['result', 'news', 'item', 'container']):
                    news_items.append(div)
        
        print(f"总共找到 {len(news_items)} 个可能的新闻条目")
        
        for item in news_items:
            try:
                # 尝试多种可能的标题选择器
                title_element = None
                for selector in ['h3 a', 'a.news-title', 'a[class*="title"]', 'a']:
                    title_element = item.select_one(selector)
                    if title_element and title_element.get_text(strip=True):
                        break
                
                if not title_element:
                    continue
                    
                title = title_element.get_text(strip=True)
                url = title_element.get('href', '')
                
                # 如果URL是相对路径，转换为绝对路径
                if url.startswith('/'):
                    url = f"https://news.baidu.com{url}"
                
                # 尝试多种可能的摘要选择器
                summary_element = None
                for selector in ['div.c-summary', 'div.content', 'div[class*="summary"]', 'div[class*="content"]', 'p']:
                    summary_element = item.select_one(selector)
                    if summary_element and summary_element.get_text(strip=True):
                        break
                
                summary_text = summary_element.get_text(strip=True) if summary_element else ""
                
                # 从摘要中提取时间信息
                time_str = ""
                time_patterns = [
                    r'(\d+)分钟前',
                    r'(\d+)小时前',
                    r'(\d+)天前',
                    r'今天',
                    r'昨天',
                    r'(\d{1,2})月(\d{1,2})日',
                    r'(\d{4})年(\d{1,2})月(\d{1,2})日'
                ]
                
                # 首先检查摘要的开头是否包含时间信息
                import re
                for pattern in time_patterns:
                    match = re.search(pattern, summary_text[:50])
                    if match:
                        time_str = match.group(0)
                        # 从摘要中移除时间信息
                        summary_text = summary_text[len(time_str):].strip()
                        if summary_text.startswith('，'):
                            summary_text = summary_text[1:].strip()
                        break
                
                # 尝试多种可能的来源选择器
                source = ""
                for selector in ['div.c-author', 'div.source', 'span.source', 'div[class*="source"]']:
                    source_element = item.select_one(selector)
                    if source_element and source_element.get_text(strip=True):
                        source = source_element.get_text(strip=True)
                        break
                
                # 如果没有找到来源，尝试从摘要末尾提取
                if not source and summary_text:
                    # 查找最后一个包含常见新闻来源关键词的部分
                    source_keywords = ['网', '报', '新闻', '日报', '周刊', '电视台', '通讯社']
                    parts = summary_text.split('...')
                    if len(parts) > 1:
                        last_part = parts[-1].strip()
                        if any(keyword in last_part for keyword in source_keywords):
                            source = last_part
                            # 从摘要中移除来源信息
                            summary_text = '...'.join(parts[:-1]) + '...'
                
                # 构建结果字典
                news_item = {
                    'title': title,
                    'url': url,
                    'summary': summary_text.strip(),
                    'source': source,
                    'time': time_str
                }
                
                results.append(news_item)
                print(f"成功解析新闻: {title[:30]}...")
                
            except Exception as e:
                print(f"解析新闻条目时出错: {str(e)}")
                continue
        
        return results


if __name__ == "__main__":
    # 简单测试
    searcher = BaiduNewsSearcher()
    results = searcher.search("人工智能")
    
    for i, result in enumerate(results, 1):
        print(f"[{i}] {result['title']}")
        print(f"链接: {result['url']}")
        print(f"摘要: {result['summary']}")
        print(f"来源: {result['source']} | 时间: {result['time']}")
        print("-" * 80)