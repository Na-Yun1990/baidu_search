#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
百度新闻搜索CLI程序
允许用户输入关键词，从百度搜索相关新闻，并展示新闻的标题、摘要和链接。
同时提供将搜索结果保存为JSON或CSV格式的功能。
"""

import argparse
import sys
import time
from colorama import init, Fore, Style
from tqdm import tqdm

from news_searcher import BaiduNewsSearcher
from data_saver import save_to_json, save_to_csv

# 初始化colorama
init(autoreset=True)


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="百度新闻搜索CLI - 搜索并展示百度新闻结果",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "keywords", 
        nargs="+", 
        help="搜索关键词"
    )
    
    parser.add_argument(
        "-p", "--page", 
        type=int, 
        default=1, 
        help="要获取的页数 (默认: 1)"
    )
    
    parser.add_argument(
        "-n", "--num", 
        type=int, 
        default=10, 
        help="每页显示的结果数量 (默认: 10)"
    )
    
    parser.add_argument(
        "-s", "--save", 
        choices=["json", "csv", "both"], 
        help="保存结果为JSON或CSV格式"
    )
    
    parser.add_argument(
        "-o", "--output", 
        default="baidu_news_results", 
        help="输出文件名 (不含扩展名，默认: baidu_news_results)"
    )
    
    parser.add_argument(
        "-d", "--delay", 
        type=float, 
        default=1.0, 
        help="请求之间的延迟时间(秒) (默认: 1.0)"
    )
    
    return parser.parse_args()


def display_results(news_items, page_size=10):
    """在命令行中显示搜索结果"""
    if not news_items:
        print(f"{Fore.YELLOW}未找到相关新闻结果。")
        return
    
    total_items = len(news_items)
    total_pages = (total_items + page_size - 1) // page_size
    current_page = 1
    
    while True:
        start_idx = (current_page - 1) * page_size
        end_idx = min(start_idx + page_size, total_items)
        
        # 清屏 (Windows和Unix兼容)
        print("\033c", end="")
        
        print(f"{Fore.CYAN}===== 百度新闻搜索结果 =====")
        print(f"{Fore.CYAN}总共找到 {total_items} 条结果，当前显示第 {current_page}/{total_pages} 页")
        print(f"{Fore.CYAN}=============================\n")
        
        for i, item in enumerate(news_items[start_idx:end_idx], start=start_idx+1):
            print(f"{Fore.GREEN}[{i}] {Style.BRIGHT}{item['title']}")
            print(f"{Fore.BLUE}{item['url']}")
            print(f"{Fore.WHITE}{item['summary']}")
            print(f"{Fore.CYAN}来源: {item.get('source', '未知')} | 时间: {item.get('time', '未知')}")
            print("-" * 80)
        
        if total_pages <= 1:
            break
            
        print(f"\n{Fore.YELLOW}[第 {current_page}/{total_pages} 页]")
        print(f"{Fore.YELLOW}n: 下一页 | p: 上一页 | q: 退出 | 数字: 跳转到指定页")
        
        choice = input(f"{Fore.YELLOW}请选择操作: ").strip().lower()
        
        if choice == 'q':
            break
        elif choice == 'n':
            current_page = min(current_page + 1, total_pages)
        elif choice == 'p':
            current_page = max(current_page - 1, 1)
        elif choice.isdigit():
            page_num = int(choice)
            if 1 <= page_num <= total_pages:
                current_page = page_num
            else:
                print(f"{Fore.RED}页码超出范围，请输入 1-{total_pages} 之间的数字")
                time.sleep(1)


def main():
    """主函数"""
    try:
        # 解析命令行参数
        args = parse_arguments()
        
        # 构建搜索关键词
        keywords = " ".join(args.keywords)
        print(f"{Fore.CYAN}正在搜索: {Fore.YELLOW}{keywords}")
        
        # 创建搜索器实例
        searcher = BaiduNewsSearcher()
        
        # 显示进度条
        with tqdm(total=args.page, desc="搜索进度", unit="页") as pbar:
            # 执行搜索
            news_items = []
            for page in range(1, args.page + 1):
                try:
                    page_items = searcher.search(keywords, page=page)
                    news_items.extend(page_items)
                    pbar.update(1)
                    
                    # 添加延迟，避免被反爬
                    if page < args.page:
                        time.sleep(args.delay)
                except Exception as e:
                    print(f"{Fore.RED}搜索第 {page} 页时出错: {str(e)}")
                    break
        
        # 显示结果
        display_results(news_items, page_size=args.num)
        
        # 保存结果
        if args.save:
            if args.save in ["json", "both"]:
                json_file = f"{args.output}.json"
                save_to_json(news_items, json_file)
                print(f"{Fore.GREEN}结果已保存为JSON: {json_file}")
                
            if args.save in ["csv", "both"]:
                csv_file = f"{args.output}.csv"
                save_to_csv(news_items, csv_file)
                print(f"{Fore.GREEN}结果已保存为CSV: {csv_file}")
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}程序已被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}程序运行出错: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()