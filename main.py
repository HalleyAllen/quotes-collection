#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
名言名句收集项目主入口文件
"""

import sys
from quotes.database import init_db, get_all_quotes, get_quote_by_id, clean_duplicate_quotes
from quotes.spider import crawl_quotes, generate_mass_quotes


def display_quote(quote):
    """显示名言详细信息
    
    Args:
        quote: sqlite3.Row对象
    """
    print("\n=====================================")
    print(f"ID: {quote['id']}")
    print(f"名言: {quote['content']}")
    print(f"拼音: {quote['pinyin']}")
    # print(f"作者: {quote['author']}")
    # print(f"朝代: {quote['dynasty']}")
    print(f"褒贬: {quote['sentiment']}")
    print(f"意义: {quote['meaning']}")
    print(f"使用场景: {quote['usage_scene']}")
    print(f"分类: {quote['category']}")
    # print(f"典故: {quote['allusion']}")
    # print(f"翻译: {quote['translation']}")
    print(f"使用注意: {quote['usage_notes']}")
    print("=====================================\n")


def view_quotes():
    """查看名言列表"""
    quotes = get_all_quotes()
    
    if not quotes:
        print("数据库中暂无名言数据")
        return
    
    print(f"\n数据库中共有 {len(quotes)} 条名言:\n")
    
    for i, quote in enumerate(quotes, 1):
        print(f"{i}. [{quote['id']}] {quote['content']} - {quote['author']}")
    
    # 选择查看详情
    choice = input("\n请输入序号查看详情，或输入0返回主菜单: ")
    
    if choice == "0":
        return
    
    try:
        index = int(choice) - 1
        if 0 <= index < len(quotes):
            display_quote(quotes[index])
            input("按回车键返回...")
        else:
            print("无效序号")
    except ValueError:
        print("无效输入")


def main():
    """主函数"""
    # 自动初始化数据库
    print("正在初始化数据库...")
    init_db()
    print("数据库初始化完成")
    
    print("\n名言名句收集项目")
    print("1. 爬取名言数据")
    print("2. 查看名言列表")
    print("3. 清理重复数据")
    print("4. 批量生成名言数据")
    print("5. 退出")
    
    choice = input("请选择操作: ")
    
    if choice == "1":
        crawl_quotes()
        print("爬取完成")
    elif choice == "2":
        view_quotes()
    elif choice == "3":
        deleted_count = clean_duplicate_quotes()
        print(f"清理完成，共删除 {deleted_count} 条重复数据")
    elif choice == "4":
        generate_mass_quotes(10000)
        print("批量生成完成")
    elif choice == "5":
        print("退出程序")
        sys.exit(0)
    else:
        print("无效选择，请重新输入")
    
    # 操作完成后返回主菜单
    input("\n按回车键返回主菜单...")
    main()


if __name__ == "__main__":
    main()
