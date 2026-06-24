# Playwright 视觉 QA 自动化测试框架 🚀

> 基于 Playwright 的轻量级、高度解耦且项目无关的 Web 视觉回归测试与截图自动化框架。

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org)
[![Playwright](https://img.shields.io/badge/playwright-tested-green.svg)](https://playwright.dev/python/)
[![License](https://img.shields.io/badge/license-MIT-purple.svg)](LICENSE)

**简体中文** | [English](README.md)

---

## 🌟 核心特性

* **通用基础类 (`BaseQA`)**：封装了 Playwright 的浏览器启动、上下文配置、多端响应式仿真、防抖截图和日志汇总等基础底座能力。
* **智能防抖快照 (`shot`)**：内置页面渲染微等待机制（默认 `1500ms`），确保复杂的图表、WebGL 动画以及布局重排完全稳定后再执行捕获，防止生成空白或错位的图片。
* **多分辨率/设备自适应**：轻松支持 PC 端分辨率配置及移动端仿真（自动调整视口宽高，注入标准的 Safari/WebKit 移动端 User-Agent）。
* **完全松耦合架构**：将自动化框架库本身与特定项目的业务测试脚本、生成的测试图片完全分离开，保持框架仓库代码纯净。

---

## 📂 推荐的代码库组织结构

为了使框架本身的仓库保持干净，方便持续维护和跨项目复用，建议在工作区中采用如下的代码结构设计：

```text
your-root-workspace/
├── universal-qa/         # 【本框架仓库】只包含通用的底层驱动和基础类
│   ├── README.md
│   ├── README.zh-CN.md
│   └── base_qa.py        # 通用基础基类
│
└── QA/                   # 【你的 QA 测试工作区】存放项目专属脚本及生成的截图
    └── <your-project>/   # 以紫微项目为例
        ├── project_qa.py # 继承 BaseQA 的业务子类，定义专属 Selector 和操作
        ├── pc-web/       # PC 端测试运行脚本与截图输出目录
        └── mobile/       # 移动端测试运行脚本与截图输出目录
```

---

## 🚀 快速上手

以在 `QA/` 工作区下为 `GoodTeam` 项目快速编写一套视觉测试为例，仅需 3 步：

### 第一步：创建项目专属业务类 `goodteam_qa.py`
在 `QA/` 目录下创建 `goodteam` 文件夹，并编写专属的交互元素定位和操作流：

```python
import sys
# 1. 引入通用框架目录的绝对路径
sys.path.append("/absolute/path/to/universal-qa")

from base_qa import BaseQA

class GoodTeamQA(BaseQA):
    def __init__(self, base_url="http://localhost:3000", out_dir="qa-screenshots", is_mobile=False, viewport=None):
        super().__init__(base_url, out_dir, is_mobile, viewport)

    def login(self, page, username, password):
        """项目特有的登录业务流"""
        page.fill("input[name='username']", username)
        page.fill("input[name='password']", password)
        page.click("button[type='submit']")
        self.wait(page, 1000) # 调用基类自带的等待方法

    def navigate_to_dashboard(self, page):
        page.click("text=Go to Dashboard")
        self.wait(page, 800)
```

### 第二步：编写测试执行脚本 `run_goodteam.py`
在 `QA/goodteam/` 下创建启动脚本进行串联：

```python
import sys
sys.path.append("/absolute/path/to/universal-qa")
sys.path.append("/absolute/path/to/QA/goodteam")

from goodteam_qa import GoodTeamQA
from playwright.sync_api import sync_playwright

# 实例化 PC 端视觉 QA 配置
qa = GoodTeamQA(
    base_url="http://localhost:3000",
    out_dir="/absolute/path/to/QA/goodteam/screenshots-desktop",
    is_mobile=False
)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = qa.create_context(browser)
    page = ctx.new_page()

    # 1. 截取 Landing 页面
    page.goto(qa.base_url)
    qa.shot(page, "01_landing_page")

    # 2. 截取登录后的仪表盘
    qa.login(page, "admin", "password123")
    qa.shot(page, "02_dashboard")

    ctx.close()
    browser.close()
    
    # 统计并打印最终生成的截图结果
    qa.list_results()
```

### 第三步：安装依赖并运行
```bash
pip install playwright
playwright install
python run_goodteam.py
```

---

## 🛠️ BaseQA API 参考文档

子类可以直接继承并调用 `BaseQA` 的以下高复用方法：

| API 方法 | 接收参数 | 详细说明 |
| :--- | :--- | :--- |
| `__init__` | `base_url`, `out_dir`, `is_mobile`, `viewport` | 初始化测试的目标域名、截图输出文件夹、响应式视口大小以及 UA 移动端注入。 |
| `create_context(browser)` | `browser` (Browser) | 传入 Playwright 浏览器实例，返回配置好分辨率和移动端伪装的 `BrowserContext`。 |
| `shot(page, name, full=True)` | `page` (Page), `name` (str), `full` (bool) | 进行网页截图。内置渲染防抖，支持长网页滚动截屏。 |
| `wait(page, ms=800)` | `page` (Page), `ms` (int) | 控制交互节奏的暂停等待（单位：毫秒）。 |
| `list_results()` | 无 | 扫描输出文件夹，统计生成的 `.png` 文件个数并在控制台输出包含文件大小（KB）的列表。 |

---

## ⚠️ 运行前置安全与环境要求 (Safety & Environment)

自动化测试脚本因为会模拟真实的点击和表单提交，在运行前请务必确认满足以下安全要求，以防止**高昂的 API 费用账单**或**敏感数据泄露**：

### 1. 💰 接口成本保护与额度防护 (LLM & Billing Cost Protection)
* **避免对高成本 API 或大语言模型接口进行高频并发测试**：如果交互脚本中涉及调用大语言模型（LLM）接口、复杂云计算或其他按量计费的第三方 API，在持续集成（CI）的高频触发或并发脚本中运行测试可能在短时间内消耗大量的 API 额度，产生高昂账单。
* **开发环境推荐进行 Mock 拦截**：在本地开发验证或日常 UI 测试时，强烈建议在后端服务或网络拦截层将这些高成本接口的响应进行 Mock，或者在测试环境中切换到低成本的开发模型（如小参数本地模型）作为出口。

### 2. 🔒 认证与验证码规避 (Auth & Security)
* **使用专属的 QA/Test 账号**：进行第三方认证登录（如 Clerk/Auth0）的自动化测试时，请在测试数据库中为其注册专门的 QA 账号。**严禁使用任何真实的生产管理员/用户账号**进行自动化模拟。
* **规避防刷机制（Rate Limit / CAPTCHA）**：在生产环境中运行此脚本可能会因为高频点击或无 Cookie 访问，直接触发 Cloudflare 等安全防护机制或 IP 封禁。因此，此脚本**仅建议在不受防御限制的本地开发机或专用 Staging 环境中执行**。

### 3. 🚫 严禁对生产环境执行写操作
* 在编写子类逻辑时，如果涉及付款支付、删除数据、修改设置等敏感写入动作，**必须在执行前判断是否处于生产域名**。如果检测到生产 URL，应立即中止并抛出异常，防止污染真实生产业务。

---

## 📄 开源许可证

本项目基于 MIT 许可证开源 - 详见 [LICENSE](LICENSE) 文件。
