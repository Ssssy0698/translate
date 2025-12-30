#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
藏语文件翻译工具 - 支持两种格式：
1. 文本文件 (.txt): 普通藏语文本文件
2. JSON文件 (.json): oral_kham格式JSON文件，格式为 {"type": "oral_kham", "data": ["句子1", "句子2", ...]}
"""

import json
import os
import sys
import time
from datetime import datetime

def load_tibetan_file(file_path):
    """
    智能加载藏语文件，支持两种格式：
    1. 文本文件 (.txt): 直接读取文本内容，leixing字段为"不明"
    2. JSON文件 (.json): 读取oral_kham格式的JSON文件，提取type和data
    """
    try:
        # 检查文件扩展名
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.json':
            # 尝试作为JSON文件加载
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"成功加载JSON文件: {file_path}")
            
            # 提取type字段
            file_type = data.get('type', '未知')
            print(f"文件类型: {file_type}")
            
            if 'data' not in data:
                print("错误: JSON文件中缺少'data'字段")
                return None, None
            
            sentences = data['data']
            print(f"藏语句子数量: {len(sentences)}")
            
            # 统计字符数
            total_chars = sum(len(s) for s in sentences)
            print(f"总字符数: {total_chars}")
            
            return sentences, file_type
            
        else:
            # 作为普通文本文件加载
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            print(f"成功加载文本文件: {file_path}")
            print(f"文件大小: {len(content)} 字符")
            
            # 按行分割
            lines = content.split('\n')
            non_empty_lines = [line.strip() for line in lines if line.strip()]
            print(f"按行分割得到 {len(non_empty_lines)} 个非空行")
            
            # 文本文件的type为"不明"
            return non_empty_lines, "不明"
            
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        print("尝试作为普通文本文件加载...")
        # 尝试作为普通文本文件加载
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            print(f"成功作为文本文件加载: {file_path}")
            print(f"文件大小: {len(content)} 字符")
            
            lines = content.split('\n')
            non_empty_lines = [line.strip() for line in lines if line.strip()]
            print(f"按行分割得到 {len(non_empty_lines)} 个非空行")
            
            return non_empty_lines, "不明"
        except Exception as e2:
            print(f"加载文件失败: {e2}")
            return None, None
    except Exception as e:
        print(f"加载文件失败: {e}")
        return None, None

def create_json_template(file_type="不明"):
    """创建JSON模板，基于muban.json结构"""
    template = {
        "leixing": file_type,  # 用户要求：文本文件为"不明"，JSON文件使用原type
        "entries": [],  # 条目列表
        "统计信息": {
            "总条数": 0,  # 用户要求：统计条数
            "最后更新": "2025-12-29"  # 用户要求：时间统一写2025-12-29
        }
    }
    return template

def translate_lines_with_instant_save(lines, template, output_file):
    """
    翻译行列表并即时保存（逐条翻译，逐条保存）
    
    Args:
        lines: 要翻译的藏语句子列表
        template: JSON模板
        output_file: 输出文件路径
        
    Returns:
        翻译结果条目列表
    """
    try:
        # 从translate.py导入TibetanTranslator类
        from translate import TibetanTranslator
    except ImportError:
        print("错误: 无法导入TibetanTranslator类")
        print("请确保translate.py在同一目录下")
        print("当前目录文件:", os.listdir('.'))
        return []
    
    translated_entries = []
    
    try:
        print("初始化翻译器...")
        with TibetanTranslator(headless=True) as translator:
            total_lines = len(lines)
            
            # 逐条翻译，一条一条处理
            print(f"开始逐条翻译 {total_lines} 行...")
            print("注意: 只访问一次网页，之后重复使用同一个页面进行翻译")
            print("即时保存: 每翻译一条就保存一条到文件")
            print("=" * 60)
            
            for i, line in enumerate(lines, 1):
                print(f"\n[{i}/{total_lines}] 翻译进度: {i/total_lines*100:.1f}%")
                print(f"藏语原文: {line[:50]}..." if len(line) > 50 else f"藏语原文: {line}")
                
                # 执行单条翻译
                result = translator.translate_single(line)
                
                if result:
                    # 用户要求：自动加id，藏语原文是tibetan字段，翻译结果是chinese字段
                    # 用户要求：不要"pinyin"和"notes"字段
                    entry = {
                        "id": i,  # 自动加id
                        "tibetan": line,  # 藏语原文
                        "chinese": result  # 翻译结果
                        # 不要"pinyin"和"notes"字段
                    }
                    translated_entries.append(entry)
                    print(f"✓ 翻译成功")
                    print(f"汉语结果: {result[:50]}..." if len(result) > 50 else f"汉语结果: {result}")
                else:
                    print("✗ 翻译失败，跳过此行")
                    # 即使翻译失败也添加条目，chinese字段为空
                    entry = {
                        "id": i,
                        "tibetan": line,
                        "chinese": ""  # 翻译失败，chinese字段为空
                        # 不要"pinyin"和"notes"字段
                    }
                    translated_entries.append(entry)
                
                # 即时保存：更新模板并保存到文件
                template["entries"] = translated_entries
                template["统计信息"]["总条数"] = len(translated_entries)
                template["统计信息"]["最后更新"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                try:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(template, f, ensure_ascii=False, indent=2)
                    print(f"✓ 已保存到文件: {len(translated_entries)}/{total_lines} 条")
                except Exception as save_error:
                    print(f"⚠ 保存文件时出错: {save_error}")
                    print("将继续翻译，但文件可能未更新")
                
                # 添加延迟，避免请求过于频繁
                if i < total_lines:
                    time.sleep(2)  # 2秒延迟
            
            return translated_entries
            
    except Exception as e:
        print(f"翻译过程中出错: {e}")
        print("\n请确保:")
        print("1. 已安装必要的Python包: pip install selenium webdriver-manager")
        print("2. 已安装Chrome浏览器")
        print("3. 网络连接正常")
        return []

def save_json_result(template, entries, output_file):
    """保存JSON结果"""
    # 更新模板数据
    template["entries"] = entries
    template["统计信息"]["总条数"] = len(entries)
    template["统计信息"]["最后更新"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(template, f, ensure_ascii=False, indent=2)
        print(f"\n✓ 翻译结果已保存到: {output_file}")
        return True
    except Exception as e:
        print(f"✗ 保存翻译结果失败: {e}")
        return False

def print_help():
    """打印帮助信息"""
    print("=" * 60)
    print("藏语文件翻译工具 - 使用说明")
    print("=" * 60)
    print("")
    print("使用方法:")
    print("  python final_translate.py [藏语文件路径]")
    print("")
    print("参数说明:")
    print("  [藏语文件路径] - 要翻译的藏语文件路径")
    print("                  支持两种格式:")
    print("                  1. 文本文件 (.txt): 普通藏语文本文件")
    print("                  2. JSON文件 (.json): oral_kham格式JSON文件")
    print("                  可以是相对路径或绝对路径")
    print("")
    print("示例:")
    print("  1. 翻译默认文件 (tibetan/1.txt):")
    print("     python final_translate.py")
    print("")
    print("  2. 翻译文本文件:")
    print("     python final_translate.py tibetan/1.txt")
    print("     python final_translate.py tibetan/sample.txt")
    print("     python final_translate.py /path/to/your/file.txt")
    print("")
    print("  3. 翻译JSON文件 (oral_kham格式):")
    print("     python final_translate.py tibetan/oral_kham.json")
    print("     python final_translate.py /path/to/oral_kham.json")
    print("")
    print("  4. 显示帮助信息:")
    print("     python final_translate.py --help")
    print("     python final_translate.py -h")
    print("     python final_translate.py help")
    print("")
    print("输出文件:")
    print("  翻译结果保存在 results/ 文件夹中")
    print("  文件命名规则: '原藏语文件'_result.json")
    print("  例如:")
    print("    tibetan/1.txt -> results/1_result.json")
    print("    tibetan/oral_kham.json -> results/oral_kham_result.json")
    print("")
    print("支持的文件格式:")
    print("  1. 文本文件格式: 普通藏语文本，按行分割")
    print("  2. JSON文件格式: {\"type\": \"oral_kham\", \"data\": [\"句子1\", \"句子2\", ...]}")
    print("")
    print("功能特点:")
    print("  - 自动访问 http://222.19.82.141:5002/index-Final.html 翻译网站")
    print("  - 智能文件格式识别（自动检测文本或JSON格式）")
    print("  - 逐条翻译，一条一条处理")
    print("  - 自动重试失败的翻译")
    print("  - 详细的翻译进度和日志")
    print("  - 保存为JSON格式，与muban.json结构相同")
    print("  - JSON文件的type字段会保存到输出文件的leixing字段")
    print("  - 即时保存功能：每翻译一条就保存一条到文件")
    print("")
    print("注意事项:")
    print("  1. 首次运行会自动下载ChromeDriver")
    print("  2. 需要安装Chrome浏览器")
    print("  3. 需要网络连接")
    print("  4. 翻译过程可能需要较长时间")
    print("  5. JSON文件较大时（如oral_kham.json），翻译时间会很长")
    print("=" * 60)

def main():
    """主函数"""
    
    # 处理命令行参数
    if len(sys.argv) > 1:
        # 检查是否请求帮助
        if sys.argv[1] in ['-h', '--help', 'help']:
            print_help()
            return True
        
        # 使用命令行参数指定的文件
        tibetan_file = sys.argv[1]
        
        # 显示帮助信息（如果文件不存在）
        if not os.path.exists(tibetan_file):
            print(f"错误: 藏语文件 '{tibetan_file}' 不存在")
            print_help()
            return False
    else:
        # 默认使用tibetan/1.txt
        tibetan_file = "tibetan/1.txt"
        
        # 检查默认文件是否存在
        if not os.path.exists(tibetan_file):
            print(f"错误: 默认文件 '{tibetan_file}' 不存在")
            print_help()
            return False
    
    # 显示程序标题和设置
    print("=" * 60)
    print("藏语文件翻译处理")
    print("严格按照用户需求:")
    print("1. 读取藏语文件（支持文本和JSON格式）")
    print("2. 使用muban.json作为翻译结果保存格式")
    print("3. leixing字段：文本文件为'不明'，JSON文件使用原type")
    print("4. 自动加id")
    print("5. 藏语原文是tibetan字段，翻译结果是chinese字段")
    print("6. 统计条数，时间统一写2025-12-29")
    print("7. 保存为JSON格式，和muban.json一样")
    print("8. 输出文件命名: '原藏语文件'_result.json")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        print(f"使用命令行参数指定的文件: {tibetan_file}")
    else:
        print(f"未指定文件，使用默认文件: {tibetan_file}")
    
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
    
    # 加载藏语文件
    print(f"\n加载文件: {tibetan_file}")
    lines, file_type = load_tibetan_file(tibetan_file)
    
    if not lines:
        print("错误: 文件加载失败")
        return False
    
    print(f"文件类型: {file_type}")
    print(f"找到 {len(lines)} 行需要翻译")
    
    # 创建JSON模板（使用文件类型）
    print("\n创建JSON模板...")
    template = create_json_template(file_type)
    
    # 一开始就创建文件（即时保存的初始文件）
    print("创建初始文件...")
    try:
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # 创建初始文件（空条目）
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(template, f, ensure_ascii=False, indent=2)
        print(f"✓ 初始文件已创建: {output_file}")
        print(f"  文件位置: {os.path.abspath(output_file)}")
    except Exception as e:
        print(f"✗ 创建初始文件失败: {e}")
        return False
    
    # 执行翻译（使用即时保存功能）
    print("\n开始翻译...")
    print("注意: 翻译过程可能需要较长时间，请耐心等待")
    print("首次运行可能会自动下载ChromeDriver")
    print("即时保存: 每翻译一条就保存一条到文件")
    print("=" * 60)
    
    entries = translate_lines_with_instant_save(lines, template, output_file)
    
    if not entries:
        print("错误: 翻译过程失败，没有生成任何条目")
        return False
    
    print(f"\n✓ 翻译完成: 处理 {len(entries)} 个条目")
    
    # 最终保存（确保文件是最新状态）
    print("\n最终保存...")
    success = save_json_result(template, entries, output_file)
    
    if success:
        print("\n" + "=" * 60)
        print("翻译处理完成!")
        print("=" * 60)
        print(f"输入文件: {tibetan_file}")
        print(f"输出文件: {output_file}")
        print(f"总条目数: {len(entries)}")
        print(f"leixing字段: {file_type}")
        print(f"时间: 2025-12-29")
        print("=" * 60)
        
        # 显示统计信息
        success_count = sum(1 for entry in entries if entry.get("chinese", "").strip())
        fail_count = len(entries) - success_count
        
        print(f"\n翻译统计:")
        print(f"成功翻译: {success_count} 条")
        print(f"翻译失败: {fail_count} 条")
        print(f"成功率: {success_count/len(entries)*100:.1f}%" if len(entries) > 0 else "成功率: 0%")
        
        # 显示前几个条目
        print(f"\n前3个条目示例:")
        for i, entry in enumerate(entries[:3], 1):
            print(f"\n条目 {entry['id']}:")
            print(f"  藏语: {entry['tibetan'][:30]}..." if len(entry['tibetan']) > 30 else f"  藏语: {entry['tibetan']}")
            if entry['chinese']:
                print(f"  汉语: {entry['chinese'][:30]}..." if len(entry['chinese']) > 30 else f"  汉语: {entry['chinese']}")
            else:
                print(f"  汉语: [翻译失败]")
        
        print(f"\n完整结果已保存到: {output_file}")
        print("可以使用文本编辑器或JSON查看器打开该文件")
        print("\n即时保存功能:")
        print("  - 一开始就创建了文件")
        print("  - 每翻译一条就保存一条")
        print("  - 即使程序中断，已翻译的内容也不会丢失")
        return True
    else:
        print("\n✗ 翻译处理失败!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
