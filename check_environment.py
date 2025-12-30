#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境检查脚本 - 检查藏语翻译脚本所需的环境配置
"""

import sys
import subprocess
import shutil

def check_python_version():
    """检查Python版本"""
    print("=" * 60)
    print("1. 检查Python版本")
    print("=" * 60)
    
    version = sys.version_info
    print(f"当前Python版本: {sys.version}")
    
    if version.major >= 3 and version.minor >= 7:
        print("✓ Python版本符合要求 (3.7+)")
        return True
    else:
        print("✗ Python版本不符合要求，需要3.7或更高版本")
        print("请从 https://www.python.org/downloads/ 下载安装")
        return False

def check_pip_packages():
    """检查必要的Python包"""
    print("\n" + "=" * 60)
    print("2. 检查Python包")
    print("=" * 60)
    
    packages = ['selenium', 'webdriver-manager']
    all_installed = True
    
    for package in packages:
        try:
            if package == 'selenium':
                import selenium
                version = selenium.__version__
                print(f"✓ {package} 已安装 (版本: {version})")
            elif package == 'webdriver-manager':
                from webdriver_manager.chrome import ChromeDriverManager
                print(f"✓ {package} 已安装")
        except ImportError:
            print(f"✗ {package} 未安装")
            all_installed = False
    
    if not all_installed:
        print("\n安装命令:")
        print("pip install selenium webdriver-manager")
        print("或")
        print("pip install --user selenium webdriver-manager")
    
    return all_installed

def check_chrome_browser():
    """检查Chrome浏览器"""
    print("\n" + "=" * 60)
    print("3. 检查Chrome浏览器")
    print("=" * 60)
    
    # 检查macOS上的Chrome
    chrome_paths = [
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        '/usr/bin/google-chrome',
        '/usr/local/bin/chrome',
        shutil.which('google-chrome'),
        shutil.which('chrome')
    ]
    
    chrome_found = False
    for path in chrome_paths:
        if path and shutil.which(path):
            print(f"✓ Chrome浏览器找到: {path}")
            chrome_found = True
            break
    
    if not chrome_found:
        print("✗ Chrome浏览器未找到或未安装")
        print("请从 https://www.google.com/chrome/ 下载安装")
    
    return chrome_found

def check_chromedriver():
    """检查ChromeDriver"""
    print("\n" + "=" * 60)
    print("4. 检查ChromeDriver")
    print("=" * 60)
    
    try:
        # 尝试使用webdriver-manager检查
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        
        print("尝试使用webdriver-manager获取ChromeDriver...")
        driver_path = ChromeDriverManager().install()
        print(f"✓ ChromeDriver可用: {driver_path}")
        return True
    except Exception as e:
        print(f"✗ ChromeDriver检查失败: {e}")
        
        # 检查系统PATH中的chromedriver
        chromedriver_path = shutil.which('chromedriver')
        if chromedriver_path:
            print(f"系统PATH中找到chromedriver: {chromedriver_path}")
            return True
        else:
            print("未在系统PATH中找到chromedriver")
            print("\n解决方案:")
            print("1. 确保已安装webdriver-manager: pip install webdriver-manager")
            print("2. 或手动下载ChromeDriver: https://chromedriver.chromium.org/")
            print("3. 将chromedriver添加到系统PATH")
            return False

def check_network():
    """检查网络连接"""
    print("\n" + "=" * 60)
    print("5. 检查网络连接")
    print("=" * 60)
    
    import urllib.request
    import socket
    
    test_url = "https://nmt.utibet.edu.cn"
    
    try:
        # 设置超时
        socket.setdefaulttimeout(10)
        
        # 尝试访问网站
        response = urllib.request.urlopen(test_url)
        status = response.getcode()
        
        if status == 200:
            print(f"✓ 可以访问翻译网站: {test_url}")
            return True
        else:
            print(f"✗ 访问翻译网站失败，状态码: {status}")
            return False
    except Exception as e:
        print(f"✗ 网络连接检查失败: {e}")
        print("请检查:")
        print("1. 网络连接是否正常")
        print("2. 是否可以访问 https://nmt.utibet.edu.cn")
        print("3. 防火墙设置")
        return False

def run_quick_test():
    """运行快速测试"""
    print("\n" + "=" * 60)
    print("6. 运行快速测试")
    print("=" * 60)
    
    try:
        # 简单测试Selenium是否可以导入
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        
        print("✓ Selenium基本功能测试通过")
        
        # 尝试创建简单的WebDriver实例（不实际启动浏览器）
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            # 只是测试导入，不实际运行
            print("✓ WebDriver配置测试通过")
            return True
        except Exception as e:
            print(f"✗ WebDriver配置测试失败: {e}")
            return False
            
    except Exception as e:
        print(f"✗ 快速测试失败: {e}")
        return False

def main():
    """主函数"""
    print("藏语翻译脚本 - 环境检查工具")
    print("=" * 60)
    
    results = []
    
    # 执行各项检查
    results.append(check_python_version())
    results.append(check_pip_packages())
    results.append(check_chrome_browser())
    results.append(check_chromedriver())
    results.append(check_network())
    results.append(run_quick_test())
    
    # 总结
    print("\n" + "=" * 60)
    print("检查结果总结")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"通过检查: {passed}/{total}")
    
    if passed == total:
        print("\n✓ 所有检查通过！环境配置正确。")
        print("可以运行藏语翻译脚本了！")
        print("\n运行命令:")
        print('python3 藏语翻译脚本.py "གཙོ་ངོས།"')
    else:
        print("\n✗ 环境配置存在问题，请根据上面的提示修复。")
        print("\n修复步骤:")
        print("1. 安装缺失的Python包: pip install selenium webdriver-manager")
        print("2. 安装Chrome浏览器: https://www.google.com/chrome/")
        print("3. 确保网络可以访问 https://nmt.utibet.edu.cn")
        print("4. 重新运行此检查脚本验证修复结果")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
