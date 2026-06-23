# Universal Web Visual QA & Screenshot Automation Framework

这套框架基于 **Playwright (Python)** 构建，旨在帮助开发人员及 AI 代理快速在新项目中实现多分辨率、多终端（Desktop/Mobile）的 UI 视觉快照测试和自动化交互验证。

框架采用了 **“通用基类 (BaseQA) + 项目专属子类 (ProjectQA)”** 的模块化设计，将底层的浏览器控制、视口模拟、防抖截图等基础设施与上层的项目业务逻辑完全解耦。

---

## 📂 推荐的代码组织结构

为了保持通用框架代码仓库的纯净，建议在项目群的共享根目录下（如 `codeAi/`）将框架与具体项目的自动化脚本分离：

```text
codeAi/
├── universal-qa/         # 【本框架仓库】只包含通用核心组件，无任何项目业务代码
│   ├── README.md
│   └── base_qa.py        # 通用核心基类
│
└── QA/                   # 【你的 QA 工作区】存放各个项目的实际测试脚本与截图输出
    └── ziwei/            # 以紫微项目为例
        ├── ziwei_qa.py   # 继承 BaseQA 的业务子类
        ├── ziwei-pc-web/ # PC 端截图运行目录（包含截图输出）
        └── ziwei-mobile/# 移动端端截图运行目录（包含截图输出）
```

---

## 🚀 其它项目如何快速接入？

假设你需要为同级目录下的 `GoodTeam` 项目在 `QA/` 工作区下编写自动化截图测试：

### 第一步：创建项目 QA 目录并编写子类 `goodteam_qa.py`
在 `QA/` 之下新建 `goodteam` 目录，并创建 `goodteam_qa.py`。继承 `base_qa.py` 中的 `BaseQA`，并在开头引入通用框架的路径：

```python
import sys
# 1. 引入通用框架的绝对路径
sys.path.append("/Users/luke/WorkSpace/codeAi/universal-qa")

from base_qa import BaseQA

class GoodTeamQA(BaseQA):
    def __init__(self, base_url="http://localhost:3000", out_dir="qa-screenshots", is_mobile=False, viewport=None):
        # 2. 初始化基类参数
        super().__init__(base_url, out_dir, is_mobile, viewport)

    def login(self, page, username, password):
        """定义专属的登录交互"""
        page.fill("input[name='username']", username)
        page.fill("input[name='password']", password)
        page.click("button[type='submit']")
        self.wait(page, 1000)
```

### 第二步：编写执行脚本 `run_goodteam.py`
在 `QA/goodteam/` 下创建执行脚本（如 `run_goodteam.py`）：

```python
import sys
# 1. 引入通用框架路径与本项目业务逻辑路径
sys.path.append("/Users/luke/WorkSpace/codeAi/universal-qa")
sys.path.append("/Users/luke/WorkSpace/codeAi/QA/goodteam")

from goodteam_qa import GoodTeamQA
from playwright.sync_api import sync_playwright

qa = GoodTeamQA(
    base_url="http://localhost:3000",
    out_dir="/Users/luke/WorkSpace/codeAi/QA/goodteam/qa-screenshots", # 指定输出路径到专属工作区
    is_mobile=False
)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = qa.create_context(browser)
    page = ctx.new_page()

    # 2. 执行截图和验证
    page.goto(qa.base_url)
    qa.shot(page, "01_landing")

    ctx.close()
    browser.close()
    qa.list_results()
```

---

## 🛠️ 核心基类 (BaseQA) 常用 API 介绍

在子类中，你可以直接使用 `BaseQA` 提供的以下高复用方法：

* **`self.shot(page, name, full=True)`**
  * **作用**：对当前页面截图。
  * **特性**：对渲染动作执行了微等待，确保图表、AI 动画等完全稳定后再截图，支持生成长网页全景图 (`full_page=True`)。
* **`self.wait(page, ms=800)`**
  * **作用**：控制交互节奏，休眠指定毫秒。
* **`self.create_context(browser)`**
  * **作用**：自动根据 `is_mobile` 参数决定是否注入移动端特定的 `User Agent` 和 `viewport` 尺寸。
* **`self.list_results()`**
  * **作用**：自动统计目标文件夹中生成的 `.png` 文件，并在控制台以列表形式打印各截图的大小（KB），方便快速校验结果。

---

## ⚠️ 运行前置安全与环境要求 (Safety & Environment)

自动化测试脚本因为会模拟真实的点击和表单提交，在运行前请务必确认满足以下安全要求，以防止**高昂的 API 费用账单**或**敏感数据泄露**：

### 1. 💰 LLM 成本保护与防刷 (LLM Cost Protection)
* **不要在高价值模型上跑高频并发测试**：部分交互（如 AI 聊天、星盘排盘等）会向 OpenAI/Gemini 发送真实的 API 请求。在高并发 CI 或循环脚本中运行此测试可能在短时间内耗尽你的模型额度或产生巨大账单。
* **开发环境推荐 Mock/本地沙箱**：在本地开发验证时，建议在后端配置中将 LLM 的响应 Mock 掉（如使用本地预设回复），或使用价格廉价的模型（如 GPT-4o-mini 或本地 Llama）作为测试出口。

### 2. 🔒 认证与验证码规避 (Auth & Security)
* **使用专属的 QA/Test 账号**：进行第三方认证登录（如 Clerk/Auth0）的自动化测试时，请在测试数据库中为其注册专门的 QA 账号。**严禁使用任何真实的生产管理员/用户账号**进行自动化模拟。
* **规避防刷机制（Rate Limit / CAPTCHA）**：在生产环境中运行此脚本可能会因为高频点击或无 Cookie 访问，直接触发 Cloudflare 等安全防护机制或 IP 封禁。因此，此脚本**仅建议在不受防御限制的本地开发机或专用 Staging 环境中执行**。

### 3. 🚫 严禁对生产环境执行写操作
* 在 `goodteam_qa.py` 或 `ziwei_qa.py` 子类中编写流程时，如果涉及付款支付、删除数据、修改设置等敏感动作，**必须在执行前判断是否处于生产域名**。如果检测到生产 URL，应立即中止并抛出异常，防止污染真实生产业务。

---

## 📦 环境依赖

使用前请确保安装了 Playwright 驱动：
```bash
pip install playwright
playwright install
```
```
