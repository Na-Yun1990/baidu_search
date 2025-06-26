#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
百度新闻搜索CLI程序启动脚本
"""

import sys
import os

# 确保可以导入项目模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入主程序
from main import main

if __name__ == "__main__":
    main()