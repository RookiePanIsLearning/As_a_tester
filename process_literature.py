#!/usr/bin/env python3
"""
文獻處理腳本 - 用於批量生成 Markdown 檔案模板
使用方法: python process_literature.py "文獻標題" "作者" "分類路徑"
"""

import sys
import os
from datetime import datetime

def create_literature_template(title, author, category):
    # 生成檔案名稱
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}_{title.replace(' ', '_')}.md"

    # 確定檔案路徑
    base_path = "/workspaces/As_a_tester/docs"
    file_path = os.path.join(base_path, category, filename)

    # 確保目錄存在
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # 模板內容
    template = f"""---
title: {title}
author: {author}
date: {date_str}
tags: []
category: {category}
---

# {title}

## 概述

## 詳細內容

## 實務應用

## 參考資料
"""

    # 寫入檔案
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(template)

    print(f"已建立檔案: {file_path}")
    return file_path

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("使用方法: python process_literature.py '文獻標題' '作者' '分類路徑'")
        print("範例: python process_literature.py '邊界值分析' '張三' '02_Methodologies/Black_Box'")
        sys.exit(1)

    title = sys.argv[1]
    author = sys.argv[2]
    category = sys.argv[3]

    create_literature_template(title, author, category)