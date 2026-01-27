#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库操作文件
"""

import sqlite3
import os
from quotes.models import Quote

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'quotes.db')


def get_db_connection():
    """获取数据库连接
    
    Returns:
        sqlite3.Connection: 数据库连接对象
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """初始化数据库，创建quotes表"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 创建quotes表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        pinyin TEXT,
        author TEXT,
        dynasty TEXT,
        sentiment TEXT,
        meaning TEXT,
        usage_scene TEXT,
        category TEXT,
        allusion TEXT,
        translation TEXT,
        usage_notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()


def insert_quote(quote):
    """插入名言数据
    
    Args:
        quote: Quote对象
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO quotes (content, pinyin, author, dynasty, sentiment, meaning, 
                       usage_scene, category, allusion, translation, usage_notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        quote.content,
        quote.pinyin,
        quote.author,
        quote.dynasty,
        quote.sentiment,
        quote.meaning,
        quote.usage_scene,
        quote.category,
        quote.allusion,
        quote.translation,
        quote.usage_notes
    ))
    
    conn.commit()
    conn.close()


def get_quote_count():
    """获取名言数量
    
    Returns:
        int: 名言数量
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM quotes')
    count = cursor.fetchone()[0]
    
    conn.close()
    return count


def get_all_quotes(order_by='id', order_dir='asc'):
    """获取所有名言
    
    Args:
        order_by: 排序字段，默认为'id'
        order_dir: 排序方向，默认为'asc'（升序），'desc'为降序
    
    Returns:
        list: 名言列表，每个元素是sqlite3.Row对象
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 验证排序字段
    valid_fields = ['id', 'content', 'author', 'dynasty', 'created_at']
    if order_by not in valid_fields:
        order_by = 'id'
    
    # 验证排序方向
    if order_dir not in ['asc', 'desc']:
        order_dir = 'asc'
    
    cursor.execute(f'SELECT * FROM quotes ORDER BY {order_by} {order_dir}')
    quotes = cursor.fetchall()
    
    conn.close()
    return quotes


def get_quotes_by_page(page=1, page_size=10, order_by='id', order_dir='asc'):
    """分页获取名言
    
    Args:
        page: 页码，从1开始
        page_size: 每页数量
        order_by: 排序字段
        order_dir: 排序方向
    
    Returns:
        tuple: (名言列表, 总页数)
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 验证排序字段
    valid_fields = ['id', 'content', 'author', 'dynasty', 'created_at']
    if order_by not in valid_fields:
        order_by = 'id'
    
    # 验证排序方向
    if order_dir not in ['asc', 'desc']:
        order_dir = 'asc'
    
    # 获取总记录数
    cursor.execute('SELECT COUNT(*) FROM quotes')
    total_count = cursor.fetchone()[0]
    
    # 计算总页数
    total_pages = (total_count + page_size - 1) // page_size
    
    # 计算偏移量
    offset = (page - 1) * page_size
    
    # 分页查询
    cursor.execute(
        f'SELECT * FROM quotes ORDER BY {order_by} {order_dir} LIMIT ? OFFSET ?',
        (page_size, offset)
    )
    quotes = cursor.fetchall()
    
    conn.close()
    return quotes, total_pages


def get_quote_by_id(quote_id):
    """根据ID获取名言
    
    Args:
        quote_id: 名言ID
    
    Returns:
        sqlite3.Row: 名言数据
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM quotes WHERE id = ?', (quote_id,))
    quote = cursor.fetchone()
    
    conn.close()
    return quote


def get_quote_by_content(content):
    """根据内容检查名言是否已存在
    
    Args:
        content: 名言内容
    
    Returns:
        sqlite3.Row: 名言数据，如果不存在返回None
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM quotes WHERE content = ?', (content,))
    quote = cursor.fetchone()
    
    conn.close()
    return quote


def clean_duplicate_quotes():
    """清理重复的名言数据
    
    Returns:
        int: 清理的重复数据数量
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 查找重复的名言内容
    cursor.execute('''
    SELECT content, MIN(id) as keep_id
    FROM quotes
    GROUP BY content
    HAVING COUNT(*) > 1
    ''')
    duplicates = cursor.fetchall()
    
    deleted_count = 0
    
    # 删除重复数据，保留最小ID的记录
    for duplicate in duplicates:
        content = duplicate['content']
        keep_id = duplicate['keep_id']
        
        # 删除除了keep_id之外的所有相同内容的记录
        cursor.execute('DELETE FROM quotes WHERE content = ? AND id != ?', (content, keep_id))
        deleted_count += cursor.rowcount
    
    conn.commit()
    conn.close()
    
    return deleted_count
