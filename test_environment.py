#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试环境 - 检查selenium和webdriver-manager是否安装
"""

import sys

def test_imports():
    """测试导入"""
    print("=" * 60)
    print("测试Python环境")
    print("=" * 60)
    
    # 测试selenium
    try:
        import selenium
        print(f"✓ selenium 已安装 (版本: {selenium.__version__})")
    except ImportError:
        print("✗ selenium 未安装")
        print("安装命令: pip install selenium")
        return False
    
    # 测试webdriver-manager
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        print("✓ webdriver-manager 已安装")
    except ImportError:
        print("✗ webdriver-manager 未安装")
        print("安装命令: pip install webdriver-manager")
        return False
    
    # 测试其他必要模块
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        print("✓ selenium 组件导入成功")
    except Exception as e:
        print(f"✗ selenium 组件导入失败: {e}")
        return False
    
    return True

def test_simple_translation():
    """测试简单翻译功能"""
    print("\n" + "=" * 60)
    print("测试简单翻译功能")
    print("=" * 60)
    
    # 这里不实际运行翻译，只测试导入
    try:
        # 测试是否能导入翻译脚本
        import 藏语翻译脚本
        print("✓ 藏语翻译脚本导入成功")
        
        # 测试是否能创建翻译器类
        from 藏语翻译脚本 import TibetanTranslator
        print("✓ TibetanTranslator类导入成功")
        
        return True
    except Exception as e:
        print(f"✗ 翻译脚本测试失败: {e}")
        return False

def main():
    """主函数"""
    print("藏语翻译环境测试")
    print("=" * 60)
    
    # 测试导入
    imports_ok = test_imports()
    
    if not imports_ok:
        print("\n环境测试失败: 必要的Python包未安装")
        print("\n请运行以下命令安装:")
        print("pip install selenium webdriver-manager")
        print("或")
        print("pip install --user selenium webdriver-manager")
        return False
    
    # 测试翻译脚本
    script_ok = test_simple_translation()
    
    if not script_ok:
        print("\n翻译脚本测试失败")
        print("请确保藏语翻译脚本.py在当前目录下")
        return False
    
    print("\n" + "=" * 60)
    print("✓ 环境测试通过!")
    print("=" * 60)
    print("\n现在可以运行:")
    print("1. 单句翻译: python3 藏语翻译脚本.py")
    print('2. 批量翻译: python3 批量翻译脚本.py')
    print("\n注意: 首次运行可能会自动下载ChromeDriver")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
