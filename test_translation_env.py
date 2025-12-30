#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试翻译环境 - 验证翻译功能是否正常工作
"""

import os
import sys

def test_environment():
    """测试环境"""
    print("=" * 60)
    print("测试翻译环境")
    print("=" * 60)
    
    # 1. 检查Python包
    print("\n1. 检查Python包...")
    try:
        import selenium
        print(f"✓ selenium已安装 (版本: {selenium.__version__})")
    except ImportError:
        print("✗ selenium未安装")
        print("请运行: pip install selenium")
        return False
    
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        print("✓ webdriver-manager已安装")
    except ImportError:
        print("✗ webdriver-manager未安装")
        print("请运行: pip install webdriver-manager")
        return False
    
    # 2. 检查translate.py
    print("\n2. 检查translate.py...")
    if not os.path.exists("translate.py"):
        print("✗ translate.py不存在")
        print("当前目录文件:", os.listdir('.'))
        return False
    
    try:
        from translate import TibetanTranslator
        print("✓ 成功导入TibetanTranslator类")
    except ImportError as e:
        print(f"✗ 导入TibetanTranslator失败: {e}")
        return False
    
    # 3. 测试简单翻译
    print("\n3. 测试简单翻译...")
    try:
        from translate import TibetanTranslator
        
        # 测试翻译器初始化
        print("正在初始化翻译器...")
        translator = TibetanTranslator(headless=True)
        
        # 测试setup_driver
        print("正在设置WebDriver...")
        if translator.setup_driver():
            print("✓ WebDriver初始化成功")
            
            # 测试简单翻译
            test_text = "གཙོ་ངོས།"
            print(f"测试翻译文本: {test_text}")
            
            result = translator.translate(test_text)
            if result:
                print(f"✓ 翻译成功: {result}")
            else:
                print("✗ 翻译失败")
            
            # 关闭浏览器
            translator.close()
            print("✓ 浏览器已关闭")
            return True
        else:
            print("✗ WebDriver初始化失败")
            return False
            
    except Exception as e:
        print(f"✗ 测试过程中出错: {e}")
        print("\n常见问题解决方案:")
        print("1. 确保已安装Chrome浏览器")
        print("2. 运行: pip install selenium webdriver-manager")
        print("3. 确保网络可以访问 https://nmt.utibet.edu.cn")
        return False

def main():
    """主函数"""
    print("藏语翻译环境测试")
    print("=" * 60)
    
    success = test_environment()
    
    if success:
        print("\n" + "=" * 60)
        print("✓ 环境测试通过!")
        print("=" * 60)
        print("\n现在可以运行:")
        print("1. 单句翻译: python3 translate.py")
        print('2. 批量翻译: python3 simple_to_json.py')
        print("\n注意: 首次运行可能会自动下载ChromeDriver")
        return True
    else:
        print("\n" + "=" * 60)
        print("✗ 环境测试失败!")
        print("=" * 60)
        print("\n请根据上面的错误信息修复问题")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
