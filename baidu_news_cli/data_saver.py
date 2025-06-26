#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据保存模块
提供将搜索结果保存为JSON或CSV格式的功能
"""

import json
import csv
import os
from datetime import datetime


def save_to_json(data, filename):
    """
    将数据保存为JSON文件
    
    Args:
        data (list): 要保存的数据列表
        filename (str): 输出文件名
    
    Returns:
        bool: 保存成功返回True，否则返回False
    """
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        # 添加元数据
        output_data = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "count": len(data)
            },
            "results": data
        }
        
        # 写入JSON文件
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        return True
    
    except Exception as e:
        print(f"保存JSON文件时出错: {str(e)}")
        return False


def save_to_csv(data, filename):
    """
    将数据保存为CSV文件
    
    Args:
        data (list): 要保存的数据列表
        filename (str): 输出文件名
    
    Returns:
        bool: 保存成功返回True，否则返回False
    """
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        # 如果数据为空，创建一个空文件并返回
        if not data:
            with open(filename, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['title', 'url', 'summary', 'source', 'time'])
            return True
        
        # 获取所有可能的字段名
        fieldnames = set()
        for item in data:
            fieldnames.update(item.keys())
        
        # 确保基本字段在前面
        basic_fields = ['title', 'url', 'summary', 'source', 'time']
        all_fields = []
        
        # 先添加基本字段
        for field in basic_fields:
            if field in fieldnames:
                all_fields.append(field)
                fieldnames.remove(field)
        
        # 再添加其他字段
        all_fields.extend(sorted(fieldnames))
        
        # 写入CSV文件
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=all_fields)
            writer.writeheader()
            writer.writerows(data)
        
        return True
    
    except Exception as e:
        print(f"保存CSV文件时出错: {str(e)}")
        return False


if __name__ == "__main__":
    # 简单测试
    test_data = [
        {
            "title": "测试新闻标题1",
            "url": "https://example.com/news/1",
            "summary": "这是一个测试新闻摘要1",
            "source": "测试来源1",
            "time": "2023-06-01 12:00"
        },
        {
            "title": "测试新闻标题2",
            "url": "https://example.com/news/2",
            "summary": "这是一个测试新闻摘要2",
            "source": "测试来源2",
            "time": "2023-06-02 13:00"
        }
    ]
    
    save_to_json(test_data, "test_output.json")
    save_to_csv(test_data, "test_output.csv")
    
    print("测试数据已保存为JSON和CSV文件")