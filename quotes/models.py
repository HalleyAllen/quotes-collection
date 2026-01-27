#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据模型文件
"""


class Quote:
    """名言数据模型"""
    
    def __init__(self, content, pinyin, author="", dynasty="", sentiment="", 
                 meaning="", usage_scene="", category="", allusion="", 
                 translation="", usage_notes=""):
        """初始化名言对象
        
        Args:
            content: 名言内容
            pinyin: 拼音
            author: 作者/来源
            dynasty: 朝代/时期
            sentiment: 褒贬含义
            meaning: 意义
            usage_scene: 日常使用场景
            category: 分类标签
            allusion: 相关典故
            translation: 翻译
            usage_notes: 使用注意事项
        """
        self.content = content
        self.pinyin = pinyin
        self.author = author
        self.dynasty = dynasty
        self.sentiment = sentiment
        self.meaning = meaning
        self.usage_scene = usage_scene
        self.category = category
        self.allusion = allusion
        self.translation = translation
        self.usage_notes = usage_notes
