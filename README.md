# UI自动化测试框架

本框架基于Python、Selenium、Pytest和Allure，用于进行Web UI自动化测试。

## 环境需求

- Python 3.x
- pip
- 浏览器（如Chrome或Firefox）
- 对应浏览器的WebDriver（如chromedriver或geckodriver）

## 安装步骤

1. 克隆仓库到本地：

   `git clone https://your-repository-url.git`
2. 进入项目目录：

    `cd ui_test_framework`
3. 创建虚拟环境并激活（推荐）：

   ```
   python -m venv venv
   source venv/bin/activate # Unix-like
   venv\Scripts\activate # Windows
   ```
4. 安装依赖项：

   `pip install -r requirements.txt`
5. 将WebDriver可执行文件放置在`drivers/`目录下，并确保配置文件中设置了正确的路径。

## 运行测试

使用以下命令运行测试：

`pytest`

## 生成Allure报告

运行测试后，使用以下命令生成Allure报告：

`allure serve reports/allure_results`

## 项目结构

- `config/`：包含框架的配置文件。
- `data/`：存放测试数据的目录。
- `drivers/`：存放WebDriver的目录。
- `logs/`：存放日志文件的目录。
- `pages/`：应用页面对象模型的目录。
- `reports/`：存放测试报告的目录。
- `tests/`：存放测试用例的目录。
- `utils/`：存放工具函数和帮助类的目录。
- `pytest.ini`：Pytest的配置文件。
- `requirements.txt`：项目依赖项文件。
- `README.md`：项目说明文件。

### `/config/`
此文件夹包含所有的配置文件，用于定义测试环境和参数。

- `config.py` - 包含全局配置信息，例如测试的基础URL、登录信息等。
- `browsers.json` - 定义不同浏览器的配置，如驱动路径、浏览器选项等。

### `/data/`
用于存放测试数据文件，支持数据驱动测试。

- `test_data.json` - 存储测试用例可能使用的数据，如用户名、密码等。

### `/drivers/`
存放WebDriver的可执行文件，例如ChromeDriver或GeckoDriver。

### `/logs/`
存储测试执行过程和结果的日志文件。

### `/pages/`
应用页面对象模型（POM），每个页面对应一个类。

- `base_page.py` - 所有页面类的基类，包含通用方法和属性。
- `login_page.py` - 示例页面类，封装登录页面的元素和交互方法。

### `/reports/`
存放测试报告，尤其是Allure报告的输出目录。

### `/tests/`
包含所有测试用例的文件夹。

- `conftest.py` - 包含所有测试用例的共享fixtures，例如WebDriver实例。
- `test_login.py` - 示例测试模块，包含登录功能的测试用例。

###  `/utils/`
包含辅助函数和工具类，支持测试用例和页面对象。

- `logger.py` - 日志配置和工具，用于生成格式化日志输出。
- `helpers.py` - 其他通用辅助函数。

### 根目录文件
- `.gitignore` - 指定不需要添加到版本控制中的文件和目录。
- `pytest.ini` - Pytest的配置文件，定义默认测试行为，如添加命令行参数、标记等。
- `requirements.txt` - 列出所有依赖包，可通过`pip install -r requirements.txt`进行安装。
- `README.md` - 项目的说明文件，包含安装、使用及贡献指南。

### 文件说明

每个文件夹和文件都有特定的用途，确保测试框架的结构化和模块化。这有助于维护、扩展和测试用例的重用。

## 扩展框架

### 添加新的页面对象
在`pages/`目录下创建新的页面类，继承自`BasePage`，并封装特定页面的元素和交互方法。

### 添加新的测试用例
在`tests/`目录下创建新的测试文件，编写测试函数，并使用`pytest`标记进行组织。

### 添加新的工具函数
在`utils/`目录下添加新的帮助类或工具函数，以支持测试用例和页面对象的通用功能。

### 更新配置
在`config/config.py`中添加或修改配置项，以支持不同的测试环境和需求。

## 贡献指南

欢迎贡献！请通过Pull Requests提交你的代码，确保你的代码符合项目的编码标准。

## 许可证

[MIT License](https://www.baidu.com)