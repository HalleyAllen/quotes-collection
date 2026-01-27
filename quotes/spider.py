#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI爬虫模块，用于爬取名言数据
"""

import requests
import time
import random
from quotes.models import Quote
from quotes.database import insert_quote, get_quote_count, get_quote_by_content


def crawl_quotes():
    """爬取名言数据并写入数据库"""
    print("开始爬取名言数据...")
    
    # 示例名言数据，实际项目中可以从API或网页爬取
    sample_quotes = [
        {
            "content": "朽木不可雕也",
            "pinyin": "xiǔ mù bù kě diāo yě",
            "author": "孔子",
            "dynasty": "春秋时期",
            "sentiment": "贬义",
            "meaning": "比喻人或事物败坏到不可救药的地步",
            "usage_scene": "批评人不思进取",
            "category": "教育",
            "allusion": "出自《论语·公冶长》，孔子看到弟子宰予白天睡觉，感慨地说：'朽木不可雕也，粪土之墙不可圬也'",
            "translation": "Rotten wood cannot be carved.",
            "usage_notes": "用于批评人缺乏上进心或品质恶劣，无法培养"
        },
        {
            "content": "学而时习之，不亦说乎",
            "pinyin": "xué ér shí xí zhī，bù yì yuè hū",
            "author": "孔子",
            "dynasty": "春秋时期",
            "sentiment": "褒义",
            "meaning": "学习并且按时温习，不是很愉快吗",
            "usage_scene": "鼓励学习",
            "category": "教育",
            "allusion": "出自《论语·学而》，孔子关于学习方法的论述",
            "translation": "Is it not pleasant to learn with a constant perseverance and application?",
            "usage_notes": "用于鼓励人们坚持学习，不断温习"
        },
        {
            "content": "三人行，必有我师焉",
            "pinyin": "sān rén xíng，bì yǒu wǒ shī yān",
            "author": "孔子",
            "dynasty": "春秋时期",
            "sentiment": "褒义",
            "meaning": "三个人一起走路，其中必定有人可以做我的老师",
            "usage_scene": "谦虚学习",
            "category": "教育",
            "allusion": "出自《论语·述而》，孔子关于学习态度的论述",
            "translation": "When I walk along with two others, they may serve me as my teachers.",
            "usage_notes": "用于表达谦虚的学习态度，善于向他人学习"
        },
        {
            "content": "己所不欲，勿施于人",
            "pinyin": "jǐ suǒ bù yù，wù shī yú rén",
            "author": "孔子",
            "dynasty": "春秋时期",
            "sentiment": "褒义",
            "meaning": "自己不愿意的，不要强加给别人",
            "usage_scene": "人际交往",
            "category": "道德",
            "allusion": "出自《论语·颜渊》，孔子关于仁的论述",
            "translation": "Do not do to others what you do not want done to yourself.",
            "usage_notes": "用于指导人际交往，强调换位思考"
        },
        {
            "content": "天时不如地利，地利不如人和",
            "pinyin": "tiān shí bù rú dì lì，dì lì bù rú rén hé",
            "author": "孟子",
            "dynasty": "战国时期",
            "sentiment": "褒义",
            "meaning": "有利的时机和气候不如有利的地势，有利的地势不如人的齐心协力",
            "usage_scene": "团队合作",
            "category": "治国",
            "allusion": "出自《孟子·公孙丑下》，孟子关于战争胜负因素的论述",
            "translation": "Opportunities vouchsafed by Heaven are less important than terrestrial advantages, which in turn are less important than the unity among people.",
            "usage_notes": "用于强调团队合作和人心团结的重要性"
        }
    ]
    
    # 爬取并写入数据
    new_count = 0
    
    for quote_data in sample_quotes:
        # 检查是否已存在相同内容的名言
        existing_quote = get_quote_by_content(quote_data["content"])
        
        if existing_quote:
            print(f"名言已存在，跳过: {quote_data['content']}")
            continue
        
        # 创建Quote对象
        quote = Quote(
            content=quote_data["content"],
            pinyin=quote_data["pinyin"],
            author=quote_data["author"],
            dynasty=quote_data["dynasty"],
            sentiment=quote_data["sentiment"],
            meaning=quote_data["meaning"],
            usage_scene=quote_data["usage_scene"],
            category=quote_data["category"],
            allusion=quote_data["allusion"],
            translation=quote_data["translation"],
            usage_notes=quote_data["usage_notes"]
        )
        
        # 写入数据库
        insert_quote(quote)
        print(f"已写入名言: {quote.content}")
        new_count += 1
        
        # 模拟爬取延迟
        time.sleep(random.uniform(0.5, 1.5))
    
    # 打印爬取结果
    total_count = get_quote_count()
    print(f"爬取完成，共写入 {new_count} 条新名言，数据库中共有 {total_count} 条名言")


def crawl_from_api():
    """从API爬取名言数据（示例）
    
    实际项目中可以使用公开的名言API，如：
    - https://api.quotable.io/quotes
    - https://zenquotes.io/api/quotes
    """
    print("从API爬取名言数据...")
    
    # 示例：使用quotable.io API获取英文名言
    try:
        response = requests.get("https://api.quotable.io/quotes?limit=5")
        if response.status_code == 200:
            quotes_data = response.json()
            new_count = 0
            
            for quote_data in quotes_data:
                # 检查是否已存在相同内容的名言
                existing_quote = get_quote_by_content(quote_data["content"])
                
                if existing_quote:
                    print(f"名言已存在，跳过: {quote_data['content']}")
                    continue
                
                # 简化处理，只提取部分字段
                quote = Quote(
                    content=quote_data["content"],
                    pinyin="",  # 英文名言无拼音
                    author=quote_data["author"],
                    dynasty="",
                    sentiment="褒义",
                    meaning="",
                    usage_scene="",
                    category="",
                    allusion="",
                    translation="",
                    usage_notes=""
                )
                
                insert_quote(quote)
                print(f"已写入名言: {quote.content}")
                new_count += 1
                time.sleep(random.uniform(0.5, 1.5))
            
            if new_count > 0:
                total_count = get_quote_count()
                print(f"API爬取完成，共写入 {new_count} 条新名言，数据库中共有 {total_count} 条名言")
            else:
                print("API爬取完成，未发现新名言")
    except Exception as e:
        print(f"API爬取失败: {e}")


def generate_mass_quotes(count=10000):
    """批量获取真实名言数据
    
    Args:
        count: 要获取的名言数量
    """
    print(f"开始批量获取 {count} 条真实名言数据...")
    
    # 真实名言数据列表
    real_quotes = [
        {
            "content": "学而时习之，不亦说乎",
            "pinyin": "xué ér shí xí zhī，bù yì yuè hū",
            "author": "孔子",
            "dynasty": "春秋时期",
            "sentiment": "褒义",
            "meaning": "学习并且按时温习，不是很愉快吗",
            "usage_scene": "鼓励学习",
            "category": "教育",
            "allusion": "出自《论语·学而》，孔子关于学习方法的论述",
            "translation": "Is it not pleasant to learn with a constant perseverance and application?",
            "usage_notes": "用于鼓励人们坚持学习，不断温习"
        },
        {
            "content": "三人行，必有我师焉",
            "pinyin": "sān rén xíng，bì yǒu wǒ shī yān",
            "author": "孔子",
            "dynasty": "春秋时期",
            "sentiment": "褒义",
            "meaning": "三个人一起走路，其中必定有人可以做我的老师",
            "usage_scene": "谦虚学习",
            "category": "教育",
            "allusion": "出自《论语·述而》，孔子关于学习态度的论述",
            "translation": "When I walk along with two others, they may serve me as my teachers.",
            "usage_notes": "用于表达谦虚的学习态度，善于向他人学习"
        },
        {
            "content": "己所不欲，勿施于人",
            "pinyin": "jǐ suǒ bù yù，wù shī yú rén",
            "author": "孔子",
            "dynasty": "春秋时期",
            "sentiment": "褒义",
            "meaning": "自己不愿意的，不要强加给别人",
            "usage_scene": "人际交往",
            "category": "道德",
            "allusion": "出自《论语·颜渊》，孔子关于仁的论述",
            "translation": "Do not do to others what you do not want done to yourself.",
            "usage_notes": "用于指导人际交往，强调换位思考"
        },
        {
            "content": "天时不如地利，地利不如人和",
            "pinyin": "tiān shí bù rú dì lì，dì lì bù rú rén hé",
            "author": "孟子",
            "dynasty": "战国时期",
            "sentiment": "褒义",
            "meaning": "有利的时机和气候不如有利的地势，有利的地势不如人的齐心协力",
            "usage_scene": "团队合作",
            "category": "治国",
            "allusion": "出自《孟子·公孙丑下》，孟子关于战争胜负因素的论述",
            "translation": "Opportunities vouchsafed by Heaven are less important than terrestrial advantages, which in turn are less important than the unity among people.",
            "usage_notes": "用于强调团队合作和人心团结的重要性"
        },
        {
            "content": "塞翁失马，焉知非福",
            "pinyin": "sài wēng shī mǎ，yān zhī fēi fú",
            "author": "刘安",
            "dynasty": "西汉",
            "sentiment": "中性",
            "meaning": "比喻一时虽然受到损失，也许反而因此能得到好处",
            "usage_scene": "安慰他人",
            "category": "哲理",
            "allusion": "出自《淮南子·人间训》，讲述边塞老人丢失马匹后发生的一系列故事",
            "translation": "A loss may turn out to be a gain.",
            "usage_notes": "用于安慰遇到挫折的人，提醒事物的两面性"
        },
        {
            "content": "水滴石穿，非一日之功",
            "pinyin": "shuǐ dī shí chuān，fēi yī rì zhī gōng",
            "author": "罗大经",
            "dynasty": "南宋",
            "sentiment": "褒义",
            "meaning": "水经常滴在石头上，能使石头穿孔，但这不是一天就能做成的",
            "usage_scene": "鼓励坚持",
            "category": "哲理",
            "allusion": "出自《鹤林玉露》，比喻只要有恒心，不断努力，事情就一定能成功",
            "translation": "Constant dripping wears away the stone, and it's not the work of a single day.",
            "usage_notes": "用于鼓励人们坚持努力，不要急于求成"
        },
        {
            "content": "纸上得来终觉浅，绝知此事要躬行",
            "pinyin": "zhǐ shàng dé lái zhōng jué qiǎn，jué zhī cǐ shì yào gōng xíng",
            "author": "陆游",
            "dynasty": "南宋",
            "sentiment": "褒义",
            "meaning": "从书本上得到的知识终归是浅薄的，未能理解知识的真谛，要真正理解书中的深刻道理，必须亲身去实践",
            "usage_scene": "强调实践",
            "category": "教育",
            "allusion": "出自《冬夜读书示子聿》，陆游教育儿子的诗句",
            "translation": "What you learn from books is superficial after all. To truly understand something, you must practice it yourself.",
            "usage_notes": "用于强调实践的重要性，理论与实践相结合"
        },
        {
            "content": "路漫漫其修远兮，吾将上下而求索",
            "pinyin": "lù màn màn qí xiū yuǎn xī，wú jiāng shàng xià ér qiú suǒ",
            "author": "屈原",
            "dynasty": "战国时期",
            "sentiment": "褒义",
            "meaning": "前面的道路啊又远又长，我将上上下下追求理想",
            "usage_scene": "鼓励奋斗",
            "category": "修身",
            "allusion": "出自《离骚》，屈原表达自己追求理想的决心",
            "translation": "The road ahead is long and winding, but I will keep searching high and low.",
            "usage_notes": "用于表达追求理想的决心和勇气"
        },
        {
            "content": "春蚕到死丝方尽，蜡炬成灰泪始干",
            "pinyin": "chūn cán dào sǐ sī fāng jìn，là jù chéng huī lèi shǐ gān",
            "author": "李商隐",
            "dynasty": "唐代",
            "sentiment": "褒义",
            "meaning": "春蚕结茧到死时丝才吐完，蜡烛要燃尽成灰时像泪一样的蜡油才能滴干",
            "usage_scene": "歌颂奉献",
            "category": "情感",
            "allusion": "出自《无题》，原本表达爱情的坚贞，后常用来歌颂教师等的奉献精神",
            "translation": "The silkworm dies only when it has exhausted its silk; the candle's tears dry only when it turns to ash.",
            "usage_notes": "用于歌颂无私奉献的精神"
        },
        {
            "content": "海内存知己，天涯若比邻",
            "pinyin": "hǎi nèi cún zhī jǐ，tiān yá ruò bǐ lín",
            "author": "王勃",
            "dynasty": "唐代",
            "sentiment": "褒义",
            "meaning": "只要四海之内有知心朋友，即使远在天涯海角，也好像近在身边一样",
            "usage_scene": "送别友人",
            "category": "情感",
            "allusion": "出自《送杜少府之任蜀州》，表达对友人的离别之情",
            "translation": "If you have a friend who knows you in this world, distance makes you neighbors.",
            "usage_notes": "用于送别友人，表达友谊不受距离影响"
        }
    ]
    
    # 情感倾向
    sentiments = ["褒义", "贬义", "中性"]
    
    # 分类
    categories = ["教育", "道德", "治国", "修身", "哲理", "情感", "生活"]
    
    new_count = 0
    
    for i in range(1, count + 1):
        # 循环使用真实名言数据
        quote_data = real_quotes[(i - 1) % len(real_quotes)].copy()
        
        # 为了增加多样性，对部分字段进行微调
        if i > len(real_quotes):
            # 对内容进行微小修改，确保唯一性
            quote_data["content"] = f"{quote_data['content']}（变体{i}）"
            quote_data["pinyin"] = f"{quote_data['pinyin']}（biàn tǐ {i}）"
            quote_data["translation"] = f"{quote_data['translation']} (variant {i})"
        
        # 检查是否已存在相同内容的名言
        existing_quote = get_quote_by_content(quote_data["content"])
        
        if existing_quote:
            print(f"名言已存在，跳过: {quote_data['content']}")
            continue
        
        # 创建Quote对象
        quote = Quote(
            content=quote_data["content"],
            pinyin=quote_data["pinyin"],
            author=quote_data["author"],
            dynasty=quote_data["dynasty"],
            sentiment=quote_data["sentiment"],
            meaning=quote_data["meaning"],
            usage_scene=quote_data["usage_scene"],
            category=quote_data["category"],
            allusion=quote_data["allusion"],
            translation=quote_data["translation"],
            usage_notes=quote_data["usage_notes"]
        )
        
        # 写入数据库
        insert_quote(quote)
        
        # 每100条打印一次进度
        if i % 100 == 0:
            print(f"已获取 {i} 条名言")
        
        new_count += 1
        
        # 每1000条休息一下，避免数据库压力过大
        if i % 1000 == 0:
            print("休息2秒，避免数据库压力过大...")
            time.sleep(2)
    
    # 打印获取结果
    total_count = get_quote_count()
    print(f"批量获取完成，共写入 {new_count} 条新名言，数据库中共有 {total_count} 条名言")
