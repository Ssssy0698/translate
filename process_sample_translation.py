#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理sample翻译 - 读取sample.txt藏语文件，翻译并保存为JSON格式
使用muban.json作为模板
"""

import json
import os
import sys
import time
from datetime import datetime

def load_tibetan_text(file_path):
    """加载藏语文本文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"成功加载藏语文件: {file_path}")
        print(f"文件大小: {len(content)} 字符")
        return content
    except Exception as e:
        print(f"加载藏语文件失败: {e}")
        return None

def split_into_paragraphs(text, max_length=500):
    """
    将文本分割成段落
    简单的分割逻辑：按句号分割，然后合并成合适长度的段落
    """
    # 按句号、问号、感叹号分割
    sentences = []
    current_sentence = ""
    
    for char in text:
        current_sentence += char
        if char in ['།', '༎', '༏', '༐', '༑', '༔', '?', '!', '。', '？', '！']:
            sentences.append(current_sentence.strip())
            current_sentence = ""
    
    # 添加最后一句（如果没有结束标点）
    if current_sentence.strip():
        sentences.append(current_sentence.strip())
    
    # 合并句子成段落
    paragraphs = []
    current_paragraph = ""
    
    for sentence in sentences:
        if len(current_paragraph) + len(sentence) + 1 <= max_length:
            if current_paragraph:
                current_paragraph += " " + sentence
            else:
                current_paragraph = sentence
        else:
            if current_paragraph:
                paragraphs.append(current_paragraph)
            current_paragraph = sentence
    
    if current_paragraph:
        paragraphs.append(current_paragraph)
    
    print(f"将文本分割成 {len(paragraphs)} 个段落")
    return paragraphs

def create_template():
    """创建基于muban.json的模板"""
    template = {
        "leixing": "不明",  # 用户要求：metadata改为leixing，值是"不明"
        "entries": [],
        "统计信息": {
            "总条数": 0,
            "翻译时间": "2025-12-29"
        }
    }
    return template

def translate_paragraphs(paragraphs):
    """翻译段落列表（逐条翻译）"""
    try:
        from translate import TibetanTranslator
    except ImportError:
        print("错误: 无法导入TibetanTranslator类")
        print("请确保translate.py在同一目录下")
        return []
    
    translated_entries = []
    
    try:
        with TibetanTranslator(headless=True) as translator:
            total = len(paragraphs)
            
            # 逐条翻译，一条一条处理
            print(f"开始逐条翻译 {total} 个段落...")
            print("注意: 只访问一次网页，之后重复使用同一个页面进行翻译")
            print("=" * 60)
            
            for i, paragraph in enumerate(paragraphs, 1):
                print(f"\n[{i}/{total}] 翻译进度: {i/total*100:.1f}%")
                print(f"藏语原文 (前100字符): {paragraph[:100]}...")
                
                # 执行单条翻译
                result = translator.translate_single(paragraph)
                
                if result:
                    entry = {
                        "id": i,
                        "tibetan": paragraph,
                        "chinese": result
                        # 用户要求：不要"pinyin"和"notes"字段
                    }
                    translated_entries.append(entry)
                    print(f"✓ 翻译成功")
                    print(f"汉语结果: {result[:50]}...")
                else:
                    print("✗ 翻译失败，跳过此段落")
                
                # 添加延迟，避免请求过于频繁
                if i < total:
                    time.sleep(3)
            
            return translated_entries
            
    except Exception as e:
        print(f"翻译过程中出错: {e}")
        return []

def save_translation_result(template, entries, output_file):
    """保存翻译结果"""
    # 更新模板数据
    template["entries"] = entries
    template["统计信息"]["总条数"] = len(entries)
    template["统计信息"]["翻译时间"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(template, f, ensure_ascii=False, indent=2)
        print(f"\n翻译结果已保存到: {output_file}")
        return True
    except Exception as e:
        print(f"保存翻译结果失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("sample.txt藏语文件翻译处理")
    print("输出文件命名: '原藏语文件'_result.json")
    print("=" * 60)
    
    # 文件路径
    tibetan_file = "tibetan/sample.txt"
    
    # 根据输入文件名生成输出文件名
    # 格式: '原藏语文件'_result.json
    input_filename = os.path.basename(tibetan_file)
    # 移除扩展名
    if '.' in input_filename:
        base_name = input_filename.rsplit('.', 1)[0]
    else:
        base_name = input_filename
    
    # 生成输出文件名
    output_filename = f"{base_name}_result.json"
    output_file = f"results/{output_filename}"
    
    # 检查文件是否存在
    if not os.path.exists(tibetan_file):
        print(f"错误: 藏语文件 '{tibetan_file}' 不存在")
        print(f"当前目录: {os.getcwd()}")
        print(f"目录内容: {os.listdir('.')}")
        return False
    
    # 加载藏语文本
    tibetan_text = load_tibetan_text(tibetan_file)
    if not tibetan_text:
        return False
    
    # 分割成段落
    paragraphs = split_into_paragraphs(tibetan_text, max_length=300)
    
    if not paragraphs:
        print("错误: 无法分割文本成段落")
        return False
    
    print(f"\n准备翻译 {len(paragraphs)} 个段落")
    
    # 创建模板
    template = create_template()
    
    # 询问用户确认
    print("\n" + "=" * 60)
    print("翻译设置:")
    print(f"源文件: {tibetan_file}")
    print(f"段落数: {len(paragraphs)}")
    print(f"输出文件: {output_file}")
    print("类型: 不明")
    print("时间: 2025-12-29")
    print("=" * 60)
    
    confirm = input("\n是否开始翻译? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes', '是']:
        print("用户取消翻译")
        return False
    
    # 执行翻译
    print("\n开始翻译...")
    entries = translate_paragraphs(paragraphs)
    
    if not entries:
        print("错误: 没有成功翻译任何段落")
        return False
    
    print(f"\n翻译完成: 成功翻译 {len(entries)}/{len(paragraphs)} 个段落")
    
    # 保存结果
    success = save_translation_result(template, entries, output_file)
    
    if success:
        print("\n" + "=" * 60)
        print("翻译处理完成!")
        print(f"输入文件: {tibetan_file}")
        print(f"输出文件: {output_file}")
        print(f"总段落数: {len(paragraphs)}")
        print(f"成功翻译: {len(entries)}")
        print("=" * 60)
        
        # 显示前几个翻译结果
        print("\n前3个翻译结果示例:")
        for i, entry in enumerate(entries[:3], 1):
            print(f"\n条目 {i} (ID: {entry['id']}):")
            print(f"藏语: {entry['tibetan'][:50]}...")
            print(f"汉语: {entry['chinese'][:50]}...")
        
        return True
    else:
        print("\n翻译处理失败!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
