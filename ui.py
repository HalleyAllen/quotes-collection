#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
名言名句收集项目UI界面
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from quotes.database import init_db, get_all_quotes, clean_duplicate_quotes, get_quotes_by_page
from quotes.spider import crawl_quotes, generate_mass_quotes


class QuotesApp:
    """名言名句收集项目UI应用"""
    
    def __init__(self, root):
        """初始化应用
        
        Args:
            root: tkinter根窗口
        """
        self.root = root
        self.root.title("名言名句收集项目")
        self.root.geometry("1000x600")
        self.root.resizable(True, True)
        # 设置窗口最小尺寸
        self.root.minsize(800, 500)
        
        # 设置窗口图标（可选）
        # self.root.iconbitmap("icon.ico")
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建顶部按钮框架
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=5)
        
        # 创建功能按钮
        self.btn_init_db = ttk.Button(self.button_frame, text="初始化数据库", command=self.init_database)
        self.btn_init_db.pack(side=tk.LEFT, padx=5)
        
        self.btn_crawl = ttk.Button(self.button_frame, text="爬取名言数据", command=self.crawl_data)
        self.btn_crawl.pack(side=tk.LEFT, padx=5)
        
        self.btn_clean = ttk.Button(self.button_frame, text="清理重复数据", command=self.clean_duplicates)
        self.btn_clean.pack(side=tk.LEFT, padx=5)
        
        self.btn_mass_generate = ttk.Button(self.button_frame, text="批量生成数据", command=self.mass_generate_data)
        self.btn_mass_generate.pack(side=tk.LEFT, padx=5)
        
        self.btn_refresh = ttk.Button(self.button_frame, text="刷新列表", command=self.refresh_quote_list)
        self.btn_refresh.pack(side=tk.LEFT, padx=5)
        
        # 创建排序选项
        self.sort_frame = ttk.Frame(self.button_frame)
        self.sort_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Label(self.sort_frame, text="排序:").pack(side=tk.LEFT, padx=5)
        
        self.sort_var = tk.StringVar(value="created_at")
        self.sort_combo = ttk.Combobox(self.sort_frame, textvariable=self.sort_var, width=10)
        self.sort_combo['values'] = ['id', 'author', 'created_at']
        self.sort_combo.pack(side=tk.LEFT, padx=5)
        
        self.order_var = tk.StringVar(value="desc")
        self.order_combo = ttk.Combobox(self.sort_frame, textvariable=self.order_var, width=8)
        self.order_combo['values'] = ['asc', 'desc']
        self.order_combo.pack(side=tk.LEFT, padx=5)
        
        self.btn_sort = ttk.Button(self.sort_frame, text="应用排序", command=self.refresh_quote_list)
        self.btn_sort.pack(side=tk.LEFT, padx=5)
        
        # 创建列显示控制区域
        self.column_frame = ttk.LabelFrame(self.main_frame, text="列显示控制")
        self.column_frame.pack(fill=tk.X, pady=5)
        
        # 列显示状态变量
        self.column_vars = {
            'id': tk.BooleanVar(value=True),
            'content': tk.BooleanVar(value=True),
            'author': tk.BooleanVar(value=True),
            'dynasty': tk.BooleanVar(value=True),
            'meaning': tk.BooleanVar(value=True),
            'created_at': tk.BooleanVar(value=True)
        }
        
        # 创建勾选框
        self.column_checkboxes = {}
        column_names = {
            'id': 'ID',
            'content': '名言内容',
            'author': '作者',
            'dynasty': '朝代',
            'meaning': '意义',
            'created_at': '添加时间'
        }
        
        for column, var in self.column_vars.items():
            checkbox = ttk.Checkbutton(self.column_frame, text=column_names[column], variable=var)
            checkbox.pack(side=tk.LEFT, padx=10)
            self.column_checkboxes[column] = checkbox
            # 绑定事件
            var.trace('w', lambda *args, col=column: self.toggle_column(col))

        
        # 创建表格区域
        self.table_frame = ttk.Frame(self.main_frame)
        self.table_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 创建滚动条
        self.table_scroll_y = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL)
        self.table_scroll_x = ttk.Scrollbar(self.table_frame, orient=tk.HORIZONTAL)
        
        # 创建表格
        self.tree = ttk.Treeview(self.table_frame, 
                                columns=('id', 'content', 'author', 'dynasty', 'meaning', 'created_at'),
                                show='headings',
                                yscrollcommand=self.table_scroll_y.set,
                                xscrollcommand=self.table_scroll_x.set)
        
        # 绑定双击事件，用于查看详情
        self.tree.bind('<Double-1>', self.on_tree_double_click)
        
        # 配置滚动条
        self.table_scroll_y.config(command=self.tree.yview)
        self.table_scroll_x.config(command=self.tree.xview)
        
        # 设置列宽和标题
        self.tree.heading('id', text='ID')
        self.tree.column('id', width=50, anchor=tk.CENTER)
        
        self.tree.heading('content', text='名言内容')
        self.tree.column('content', width=300, anchor=tk.W)
        
        self.tree.heading('author', text='作者')
        self.tree.column('author', width=100, anchor=tk.CENTER)
        
        self.tree.heading('dynasty', text='朝代')
        self.tree.column('dynasty', width=100, anchor=tk.CENTER)
        
        self.tree.heading('meaning', text='意义')
        self.tree.column('meaning', width=200, anchor=tk.W)
        
        self.tree.heading('created_at', text='添加时间')
        self.tree.column('created_at', width=150, anchor=tk.CENTER)
        
        # 布局
        self.table_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.table_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 分页相关变量
        self.current_page = 1
        self.page_size = 10
        self.total_pages = 1
        
        # 初始化数据
        self.quotes_data = []
        
        # 创建分页控件
        self.pagination_frame = ttk.Frame(self.main_frame)
        self.pagination_frame.pack(fill=tk.X, pady=5)
        
        self.page_info_var = tk.StringVar()
        self.page_info_var.set(f"第 1 页，共 1 页")
        self.page_info_label = ttk.Label(self.pagination_frame, textvariable=self.page_info_var)
        self.page_info_label.pack(side=tk.LEFT, padx=10)
        
        self.pagination_buttons = ttk.Frame(self.pagination_frame)
        self.pagination_buttons.pack(side=tk.RIGHT, padx=10)
        
        self.btn_first = ttk.Button(self.pagination_buttons, text="首页", command=self.go_to_first_page)
        self.btn_first.pack(side=tk.LEFT, padx=5)
        
        self.btn_prev = ttk.Button(self.pagination_buttons, text="上一页", command=self.go_to_prev_page)
        self.btn_prev.pack(side=tk.LEFT, padx=5)
        
        self.btn_next = ttk.Button(self.pagination_buttons, text="下一页", command=self.go_to_next_page)
        self.btn_next.pack(side=tk.LEFT, padx=5)
        
        self.btn_last = ttk.Button(self.pagination_buttons, text="末页", command=self.go_to_last_page)
        self.btn_last.pack(side=tk.LEFT, padx=5)
        
        # 初始化数据
        self.refresh_quote_list()
    
    def init_database(self):
        """初始化数据库"""
        try:
            self.status_var.set("正在初始化数据库...")
            self.root.update()
            
            init_db()
            
            messagebox.showinfo("成功", "数据库初始化完成")
            self.status_var.set("数据库初始化完成")
            self.refresh_quote_list()
        except Exception as e:
            messagebox.showerror("错误", f"初始化数据库失败: {str(e)}")
            self.status_var.set("就绪")
    
    def crawl_data(self):
        """爬取名言数据"""
        def crawl_thread():
            try:
                self.status_var.set("正在爬取名言数据...")
                self.root.update()
                
                crawl_quotes()
                
                self.root.after(0, lambda: messagebox.showinfo("成功", "爬取数据完成"))
                self.root.after(0, lambda: self.status_var.set("爬取数据完成"))
                self.root.after(0, self.refresh_quote_list)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("错误", f"爬取数据失败: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("就绪"))
        
        # 在新线程中执行爬取操作，避免阻塞UI
        thread = threading.Thread(target=crawl_thread)
        thread.daemon = True
        thread.start()
    
    def mass_generate_data(self):
        """批量生成名言数据"""
        def generate_thread():
            try:
                self.status_var.set("正在批量生成名言数据...")
                self.root.update()
                
                # 生成10000条数据
                generate_mass_quotes(10000)
                
                self.root.after(0, lambda: messagebox.showinfo("成功", "批量生成数据完成"))
                self.root.after(0, lambda: self.status_var.set("批量生成数据完成"))
                self.root.after(0, self.refresh_quote_list)
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("错误", f"批量生成数据失败: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("就绪"))
        
        # 在新线程中执行批量生成操作，避免阻塞UI
        thread = threading.Thread(target=generate_thread)
        thread.daemon = True
        thread.start()
    
    def clean_duplicates(self):
        """清理重复数据"""
        try:
            self.status_var.set("正在清理重复数据...")
            self.root.update()
            
            deleted_count = clean_duplicate_quotes()
            
            messagebox.showinfo("成功", f"清理完成，共删除 {deleted_count} 条重复数据")
            self.status_var.set(f"清理完成，删除 {deleted_count} 条重复数据")
            self.refresh_quote_list()
        except Exception as e:
            messagebox.showerror("错误", f"清理重复数据失败: {str(e)}")
            self.status_var.set("就绪")
    
    def refresh_quote_list(self):
        """刷新名言列表"""
        try:
            self.status_var.set("正在刷新名言列表...")
            self.root.update()
            
            # 重新构建表格
            self.rebuild_tree()
            
            self.status_var.set(f"就绪 - 共 {len(self.tree.get_children())} 条名言")
        except Exception as e:
            messagebox.showerror("错误", f"刷新列表失败: {str(e)}")
            self.status_var.set("就绪")
    
    def go_to_first_page(self):
        """前往首页"""
        if self.current_page != 1:
            self.current_page = 1
            self.refresh_quote_list()
    
    def go_to_prev_page(self):
        """前往上一页"""
        if self.current_page > 1:
            self.current_page -= 1
            self.refresh_quote_list()
    
    def go_to_next_page(self):
        """前往下一页"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.refresh_quote_list()
    
    def go_to_last_page(self):
        """前往末页"""
        if self.current_page != self.total_pages:
            self.current_page = self.total_pages
            self.refresh_quote_list()
    
    def on_tree_double_click(self, event):
        """双击表格行查看详情
        
        Args:
            event: 事件对象
        """
        # 获取选中的行
        item = self.tree.selection()[0]
        # 获取行数据
        values = self.tree.item(item, 'values')
        
        # 获取可见列
        visible_columns = self.tree['columns']
        
        # 构建详情信息
        detail_window = tk.Toplevel(self.root)
        detail_window.title("名言详情")
        detail_window.geometry("600x400")
        
        # 创建文本框显示详情
        detail_text = tk.Text(detail_window, wrap=tk.WORD, padx=10, pady=10)
        detail_text.pack(fill=tk.BOTH, expand=True)
        
        # 获取完整的名言数据
        # 这里需要根据ID获取完整数据，暂时使用表格中的数据
        # 实际项目中应该根据ID从数据库获取完整数据
        
        # 显示详情
        detail_text.insert(tk.END, "【名言详情】\n\n")
        for i, col in enumerate(visible_columns):
            if i < len(values):
                # 获取列显示名称
                column_names = {
                    'id': 'ID',
                    'content': '名言内容',
                    'author': '作者',
                    'dynasty': '朝代',
                    'meaning': '意义',
                    'created_at': '添加时间'
                }
                col_name = column_names.get(col, col)
                detail_text.insert(tk.END, f"{col_name}: {values[i]}\n")
        
        # 添加关闭按钮
        close_btn = ttk.Button(detail_window, text="关闭", command=detail_window.destroy)
        close_btn.pack(pady=10)
    
    def toggle_column(self, column):
        """切换列的显示/隐藏状态
        
        Args:
            column: 列名
        """
        # 重新构建表格
        self.rebuild_tree()
    
    def rebuild_tree(self):
        """根据列显示状态重新构建表格"""
        # 保存当前选择
        current_selection = self.tree.selection()
        
        # 获取当前排序
        order_by = self.sort_var.get()
        order_dir = self.order_var.get()
        
        # 清空表格
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 移除所有列
        for col in self.tree['columns']:
            self.tree.heading(col, text='')
        
        # 确定要显示的列
        visible_columns = [col for col, var in self.column_vars.items() if var.get()]
        
        # 重新配置列
        self.tree['columns'] = visible_columns
        
        # 设置列标题和宽度
        column_config = {
            'id': {'text': 'ID', 'minwidth': 50, 'width': 50, 'anchor': tk.CENTER, 'stretch': False},
            'content': {'text': '名言内容', 'minwidth': 300, 'width': 400, 'anchor': tk.W, 'stretch': True},
            'author': {'text': '作者', 'minwidth': 100, 'width': 120, 'anchor': tk.CENTER, 'stretch': False},
            'dynasty': {'text': '朝代', 'minwidth': 100, 'width': 120, 'anchor': tk.CENTER, 'stretch': False},
            'meaning': {'text': '意义', 'minwidth': 250, 'width': 300, 'anchor': tk.W, 'stretch': True},
            'created_at': {'text': '添加时间', 'minwidth': 150, 'width': 180, 'anchor': tk.CENTER, 'stretch': False}
        }
        
        for col in visible_columns:
            if col in column_config:
                config = column_config[col]
                self.tree.heading(col, text=config['text'])
                self.tree.column(col, 
                                minwidth=config['minwidth'],
                                width=config['width'], 
                                anchor=config['anchor'],
                                stretch=config['stretch'])
        
        # 调整行高以支持换行
        # Treeview控件不支持wrap选项，移除这个配置
        
        # 重新加载数据
        quotes, self.total_pages = get_quotes_by_page(
            page=self.current_page,
            page_size=self.page_size,
            order_by=order_by,
            order_dir=order_dir
        )
        
        # 更新分页信息
        self.page_info_var.set(f"第 {self.current_page} 页，共 {self.total_pages} 页")
        
        # 插入数据
        for quote in quotes:
            # 只插入可见列的数据
            values = []
            for col in visible_columns:
                # 确保文本不会过长
                value = quote[col]
                if isinstance(value, str):
                    # 根据列类型设置不同的截取长度
                    max_lengths = {
                        'content': 150,
                        'meaning': 120,
                        'author': 20,
                        'dynasty': 20
                    }
                    max_len = max_lengths.get(col, 50)
                    if len(value) > max_len:
                        # 对于长文本，截取并添加省略号
                        value = value[:max_len-3] + '...'
                values.append(value)
            # 插入数据
            self.tree.insert('', tk.END, values=values)
        
        # 禁用/启用分页按钮
        self.btn_first.config(state=tk.DISABLED if self.current_page == 1 else tk.NORMAL)
        self.btn_prev.config(state=tk.DISABLED if self.current_page == 1 else tk.NORMAL)
        self.btn_next.config(state=tk.DISABLED if self.current_page == self.total_pages else tk.NORMAL)
        self.btn_last.config(state=tk.DISABLED if self.current_page == self.total_pages else tk.NORMAL)
        
        # 刷新表格布局
        self.tree.update_idletasks()
        self.table_frame.update_idletasks()
    



def main():
    """主函数"""
    root = tk.Tk()
    app = QuotesApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
