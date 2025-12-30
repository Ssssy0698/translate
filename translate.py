#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
藏语翻译脚本 - 自动化访问 http://222.19.82.141:5002/index-Final.html 进行藏汉翻译
使用Selenium WebDriver模拟浏览器操作
新页面流程：输入文本 -> 点击智能翻译 -> 获取翻译结果
"""

import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class TibetanTranslator:
    """藏语翻译器类"""
    
    def __init__(self, headless=False):
        """
        初始化翻译器
        
        Args:
            headless: 是否使用无头模式（不显示浏览器界面）
        """
        self.url = "http://222.19.82.141:5002/index-Final.html"
        self.headless = headless
        self.driver = None
        self.wait = None
        self.is_initialized = False  # 标记是否已初始化页面
        self.first_translation_done = False  # 标记第一次翻译是否已完成
        
    def setup_driver(self):
        """设置WebDriver"""
        try:
            # 首先检查必要的包
            print("检查必要的Python包...")
            
            # 检查selenium
            try:
                import selenium
                print(f"✓ selenium已安装 (版本: {selenium.__version__})")
            except ImportError:
                print("✗ selenium未安装")
                print("请运行: pip install selenium")
                return False
            
            # 尝试使用webdriver-manager（推荐）
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                from selenium.webdriver.chrome.service import Service
                
                print("✓ webdriver-manager已安装")
                print("正在自动下载和管理ChromeDriver...")
                
                # 配置Chrome选项
                options = webdriver.ChromeOptions()
                if self.headless:
                    options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu')
                options.add_argument('--window-size=1920,1080')
                options.add_argument('--disable-blink-features=AutomationControlled')
                options.add_experimental_option("excludeSwitches", ["enable-automation"])
                options.add_experimental_option('useAutomationExtension', False)
                
                # 自动下载和管理ChromeDriver
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
                
                print("✓ ChromeDriver自动配置成功")
                
            except ImportError:
                # 如果webdriver-manager不可用，尝试系统ChromeDriver
                print("⚠ webdriver-manager未安装，尝试使用系统ChromeDriver")
                print("建议安装webdriver-manager以获得更好的体验: pip install webdriver-manager")
                
                options = webdriver.ChromeOptions()
                if self.headless:
                    options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                
                try:
                    self.driver = webdriver.Chrome(options=options)
                    print("✓ 系统ChromeDriver初始化成功")
                except Exception as chrome_error:
                    print(f"✗ 系统ChromeDriver初始化失败: {chrome_error}")
                    print("\n解决方案:")
                    print("1. 安装webdriver-manager: pip install webdriver-manager")
                    print("2. 或手动下载ChromeDriver: https://chromedriver.chromium.org/")
                    print("3. 将chromedriver添加到系统PATH")
                    return False
            
            # 设置等待时间
            self.driver.implicitly_wait(15)
            self.wait = WebDriverWait(self.driver, 30)
            
            print("✓ WebDriver初始化成功")
            return True
            
        except Exception as e:
            print(f"✗ WebDriver初始化失败: {e}")
            print("\n详细解决方案:")
            print("=" * 60)
            print("1. 安装必要的Python包:")
            print("   pip install selenium webdriver-manager")
            print("")
            print("2. 确保已安装Chrome浏览器:")
            print("   下载地址: https://www.google.com/chrome/")
            print("")
            print("3. 如果已安装但仍有问题，尝试:")
            print("   - 更新Chrome浏览器到最新版本")
            print("   - 手动下载ChromeDriver: https://chromedriver.chromium.org/")
            print("   - 将chromedriver添加到系统PATH")
            print("=" * 60)
            return False
    
    def initialize(self):
        """初始化翻译页面（只执行一次）"""
        if self.is_initialized:
            print("页面已初始化，跳过初始化步骤")
            return True
            
        try:
            print(f"正在访问: {self.url}")
            self.driver.get(self.url)
            
            # 等待页面加载完成 - 新页面等待输入框加载
            self.wait.until(
                EC.presence_of_element_located((By.ID, "inputText"))
            )
            print("翻译页面加载成功")
            
            # 新页面默认就是藏语->汉语翻译，不需要点击交换按钮
            self.is_initialized = True
            print("页面初始化完成")
            return True
            
        except TimeoutException:
            print("错误: 页面加载超时")
            return False
        except Exception as e:
            print(f"初始化页面时出错: {e}")
            return False
    
    def input_tibetan_text(self, text):
        """输入藏语文本"""
        try:
            # 查找输入文本框: id="inputText" (新页面)
            input_box = self.wait.until(
                EC.presence_of_element_located((By.ID, "inputText"))
            )
            
            # 清空并输入文本
            input_box.clear()
            input_box.send_keys(text)
            print(f"已输入藏语文本: {text}")
            return True
            
        except Exception as e:
            print(f"输入文本时出错: {e}")
            return False
    
    def click_translate_button(self):
        """点击翻译按钮"""
        try:
            # 查找翻译按钮: id="translateBtn" (新页面)
            translate_button = self.wait.until(
                EC.element_to_be_clickable((By.ID, "translateBtn"))
            )
            translate_button.click()
            print("已点击智能翻译按钮")
            return True
            
        except Exception as e:
            print(f"点击翻译按钮时出错: {e}")
            return False
    
    def get_translation_result(self):
        """获取翻译结果"""
        try:
            # 等待结果加载，查找结果区域: id="result" (新页面是div)
            result_div = self.wait.until(
                EC.presence_of_element_located((By.ID, "result"))
            )
            
            # 获取结果文本 - 新页面是div的innerText
            result = result_div.text
            print(f"翻译结果: {result}")
            return result
            
        except TimeoutException:
            print("错误: 等待翻译结果超时")
            return None
        except Exception as e:
            print(f"获取翻译结果时出错: {e}")
            return None
    
    def translate_single(self, tibetan_text, max_retries=2):
        """
        在已初始化的页面上执行单次翻译
        
        Args:
            tibetan_text: 藏语文本
            max_retries: 最大重试次数（针对第一句翻译问题）
            
        Returns:
            汉语翻译结果或None
        """
        for attempt in range(max_retries):
            try:
                # 确保页面已初始化
                if not self.is_initialized:
                    print("页面未初始化，正在初始化...")
                    if not self.initialize():
                        print("页面初始化失败")
                        return None
                
                print(f"\n开始翻译流程 (尝试 {attempt + 1}/{max_retries}):")
                print("=" * 40)
                
                # 1. 输入文本（确保输入框完全清空）
                print(f"步骤1: 输入藏语文本...")
                if not self.input_tibetan_text(tibetan_text):
                    print("✗ 输入文本失败")
                    continue
                print("✓ 文本输入成功")
                
                # 2. 点击翻译
                print("步骤2: 点击智能翻译按钮...")
                if not self.click_translate_button():
                    print("✗ 点击翻译按钮失败")
                    continue
                print("✓ 翻译按钮点击成功")
                
                # 3. 等待翻译完成（根据是否是第一次成功翻译决定等待时间）
                if not self.first_translation_done:
                    wait_time = 4  # 第一次翻译等待4秒
                    wait_reason = "第一次翻译，等待更长时间确保成功"
                else:
                    wait_time = 0.5  # 后续翻译等待0.5秒（用户要求）
                    wait_reason = "后续翻译，等待0.5秒"
                
                print(f"步骤3: 等待翻译处理 ({wait_time}秒) - {wait_reason}...")
                time.sleep(wait_time)
                print("✓ 翻译处理完成")
                
                # 4. 获取结果
                print("步骤4: 获取翻译结果...")
                result = self.get_translation_result()
                
                if result:
                    # 验证结果：检查是否是藏语（包含藏语标点符号）
                    if any(char in result for char in ['།', '༎', '༏', '༐', '༑', '༔']):
                        print(f"⚠ 警告: 翻译结果包含藏语字符，可能是错误的翻译")
                        print(f"   结果: {result[:50]}...")
                        if attempt < max_retries - 1:
                            print(f"   将重试...")
                            continue
                        else:
                            print("✗ 经过多次尝试后翻译结果仍然包含藏语字符")
                            return ""
                    else:
                        print("✓ 翻译结果获取成功")
                        # 标记第一次翻译已完成
                        if not self.first_translation_done:
                            self.first_translation_done = True
                            print("✓ 第一次翻译成功完成，后续翻译将使用正常等待时间")
                        print("=" * 40)
                        return result
                else:
                    print("✗ 翻译结果获取失败")
                    if attempt < max_retries - 1:
                        print(f"   将重试...")
                    continue
                
            except Exception as e:
                print(f"翻译过程中出错: {e}")
                if attempt < max_retries - 1:
                    print(f"   将重试...")
                continue
        
        print("=" * 40)
        return None
    
    def translate(self, tibetan_text, max_retries=2):
        """
        执行翻译（兼容旧接口）
        
        Args:
            tibetan_text: 藏语文本
            max_retries: 最大重试次数
            
        Returns:
            汉语翻译结果或None
        """
        # 使用新的translate_single方法
        return self.translate_single(tibetan_text, max_retries)
    
    def translate_multiple(self, tibetan_texts, delay_between=2):
        """
        批量翻译多个文本
        
        Args:
            tibetan_texts: 藏语文本列表
            delay_between: 每次翻译之间的延迟（秒）
            
        Returns:
            翻译结果列表，失败的项目为None
        """
        results = []
        
        # 确保页面已初始化
        if not self.is_initialized:
            print("页面未初始化，正在初始化...")
            if not self.initialize():
                print("页面初始化失败")
                return [None] * len(tibetan_texts)
        
        total = len(tibetan_texts)
        for i, text in enumerate(tibetan_texts, 1):
            print(f"\n[{i}/{total}] 翻译进度: {i/total*100:.1f}%")
            print(f"藏语原文: {text[:50]}..." if len(text) > 50 else f"藏语原文: {text}")
            
            result = self.translate_single(text)
            results.append(result)
            
            # 添加延迟，避免请求过于频繁
            if i < total:
                print(f"等待 {delay_between} 秒...")
                time.sleep(delay_between)
        
        return results
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            print("浏览器已关闭")
    
    def __enter__(self):
        """上下文管理器入口"""
        if self.setup_driver():
            return self
        else:
            raise Exception("无法初始化WebDriver")
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()


def main():
    """主函数"""
    print("=" * 60)
    print("藏语翻译脚本 - 自动化藏汉翻译")
    print("=" * 60)
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        tibetan_text = sys.argv[1]
        print(f"使用命令行参数中的藏语文本: {tibetan_text}")
    else:
        # 如果没有命令行参数，提示用户输入
        print("\n使用方法:")
        print("1. 命令行参数: python3 藏语翻译脚本.py \"གཙོ་ངོས།\"")
        print("2. 交互式输入: 直接运行脚本，然后在提示处输入")
        print("\n" + "-" * 60)
        
        # 交互式输入
        tibetan_text = input("请输入藏语文本 (直接回车使用示例文本 'གཙོ་ངོས།'): ").strip()
        
        if not tibetan_text:
            tibetan_text = "གཙོ་ངོས།"
            print(f"使用示例文本: {tibetan_text}")
    
    try:
        # 使用上下文管理器确保资源正确释放
        with TibetanTranslator(headless=False) as translator:
            print(f"\n开始翻译: {tibetan_text}")
            result = translator.translate(tibetan_text)
            
            if result:
                print("\n" + "=" * 60)
                print(f"藏语原文: {tibetan_text}")
                print(f"汉语翻译: {result}")
                print("=" * 60)
                
                # 询问是否保存结果
                save_choice = input("\n是否保存翻译结果到文件? (y/n): ").strip().lower()
                if save_choice == 'y' or save_choice == 'yes':
                    filename = f"翻译结果_{time.strftime('%Y%m%d_%H%M%S')}.txt"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"藏语原文: {tibetan_text}\n")
                        f.write(f"汉语翻译: {result}\n")
                        f.write(f"翻译时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    print(f"结果已保存到: {filename}")
                
                return result
            else:
                print("\n翻译失败")
                return None
                
    except Exception as e:
        print(f"\n程序执行出错: {e}")
        print("\n请检查:")
        print("1. 是否已安装Chrome浏览器")
        print("2. 是否已安装Python包: pip install selenium webdriver-manager")
        print("3. 网络连接是否正常")
        return None


if __name__ == "__main__":
    main()
