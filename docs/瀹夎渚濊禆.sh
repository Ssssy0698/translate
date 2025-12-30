#!/bin/bash
# 藏语翻译脚本 - 依赖安装脚本

echo "=========================================="
echo "藏语翻译脚本 - 依赖安装"
echo "=========================================="

# 检查Python
echo "1. 检查Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Python已安装: $PYTHON_VERSION"
else
    echo "✗ Python未安装"
    echo "请从 https://www.python.org/downloads/ 下载安装Python 3.7+"
    exit 1
fi

# 检查pip
echo ""
echo "2. 检查pip..."
if command -v pip3 &> /dev/null; then
    echo "✓ pip3已安装"
    PIP_CMD="pip3"
elif python3 -m pip --version &> /dev/null; then
    echo "✓ pip已安装 (通过python3 -m pip)"
    PIP_CMD="python3 -m pip"
else
    echo "✗ pip未安装"
    echo "尝试安装pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    rm get-pip.py
    PIP_CMD="pip3"
fi

# 安装Python包
echo ""
echo "3. 安装Python包..."
echo "安装selenium..."
$PIP_CMD install selenium

echo "安装webdriver-manager..."
$PIP_CMD install webdriver-manager

# 检查安装结果
echo ""
echo "4. 验证安装..."
python3 -c "import selenium; print('✓ selenium版本:', selenium.__version__)" 2>/dev/null || echo "✗ selenium安装失败"
python3 -c "from webdriver_manager.chrome import ChromeDriverManager; print('✓ webdriver-manager已安装')" 2>/dev/null || echo "✗ webdriver-manager安装失败"

# 检查Chrome浏览器
echo ""
echo "5. 检查Chrome浏览器..."
if [ -d "/Applications/Google Chrome.app" ]; then
    echo "✓ Chrome浏览器已安装"
else
    echo "⚠ Chrome浏览器未找到"
    echo "请从 https://www.google.com/chrome/ 下载安装Chrome浏览器"
fi

# 创建测试脚本
echo ""
echo "6. 创建环境测试脚本..."
cat > test_environment.py << 'EOF'
#!/usr/bin/env python3
import sys

try:
    import selenium
    print(f"✓ selenium: {selenium.__version__}")
except ImportError:
    print("✗ selenium未安装")
    sys.exit(1)

try:
    from webdriver_manager.chrome import ChromeDriverManager
    print("✓ webdriver-manager: 已安装")
except ImportError:
    print("✗ webdriver-manager未安装")
    sys.exit(1)

print("✓ 所有依赖检查通过！")
print("可以运行藏语翻译脚本了！")
EOF

chmod +x test_environment.py

echo ""
echo "=========================================="
echo "安装完成！"
echo "=========================================="
echo ""
echo "运行环境测试:"
echo "  python3 test_environment.py"
echo ""
echo "运行藏语翻译脚本:"
echo "  python3 藏语翻译脚本.py"
echo ""
echo "或使用命令行参数:"
echo '  python3 藏语翻译脚本.py "གཙོ་ངོས།"'
echo ""
echo "更多信息请查看:"
echo "  使用说明.txt"
echo "  环境要求.md"
