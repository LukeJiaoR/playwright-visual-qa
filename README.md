# Playwright Visual QA Framework 🚀

> A lightweight, highly decoupled, and project-agnostic visual QA & screenshot automation testing framework built on top of Playwright.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org)
[![Playwright](https://img.shields.io/badge/playwright-tested-green.svg)](https://playwright.dev/python/)
[![License](https://img.shields.io/badge/license-MIT-purple.svg)](LICENSE)

[简体中文](README.zh-CN.md) | **English**

---

## 🌟 Key Features

* **Project-Agnostic Core (`BaseQA`)**: Abstracted Playwright session setups, device/viewport configs, smart wait handling, and image capture capabilities.
* **Smart Anti-Shake Snapshotting**: Integrated dynamic rendering waits (`1500ms` debounce) ensuring charts, WebGL animations, and layout flows stabilize before capturing.
* **Automatic Device Simulation**: Toggles desktop views or simulated mobile profiles (iPhone viewports, Safari/WebKit User-Agent injection).
* **Loosely Coupled Architecture**: Keeps the framework codebase clean and publish-ready, completely separating it from project-specific code and output images.

---

## 📂 Recommended Codebase Architecture

For clean scaling, we recommend separating this framework library from your specific project testing configurations:

```text
your-root-workspace/
├── universal-qa/         # [This Repository] Only contains core helper libraries
│   ├── README.md
│   ├── README.zh-CN.md
│   └── base_qa.py        # Generic BaseQA parent class
│
└── QA/                   # [Your Testing Workspace] Untracked scripts & image outputs
    └── <your-project>/   # e.g., ziwei
        ├── project_qa.py # Inherits BaseQA, overrides project-specific UI flow
        ├── pc-web/       # Desktop QA test directory & screenshots
        └── mobile/       # Mobile QA test directory & screenshots
```

---

## 🚀 Quick Start

Here is how you can implement visual QA for a project named `GoodTeam` in 3 simple steps.

### Step 1: Create your project-specific class `goodteam_qa.py`
Create a folder named `goodteam/` under your `QA/` workspace, and define the custom selector mappings and flow:

```python
import sys
# 1. Add the path to universal-qa directory
sys.path.append("/absolute/path/to/universal-qa")

from base_qa import BaseQA

class GoodTeamQA(BaseQA):
    def __init__(self, base_url="http://localhost:3000", out_dir="qa-screenshots", is_mobile=False, viewport=None):
        super().__init__(base_url, out_dir, is_mobile, viewport)

    def login(self, page, username, password):
        """Project-specific login workflow"""
        page.fill("input[name='username']", username)
        page.fill("input[name='password']", password)
        page.click("button[type='submit']")
        self.wait(page, 1000) # Utilizes BaseQA wait helper

    def navigate_to_dashboard(self, page):
        page.click("text=Go to Dashboard")
        self.wait(page, 800)
```

### Step 2: Write your execution script `run_goodteam.py`
In `QA/goodteam/`, write a script to orchestrate the test:

```python
import sys
sys.path.append("/absolute/path/to/universal-qa")
sys.path.append("/absolute/path/to/QA/goodteam")

from goodteam_qa import GoodTeamQA
from playwright.sync_api import sync_playwright

# Setup for desktop visual QA
qa = GoodTeamQA(
    base_url="http://localhost:3000",
    out_dir="/absolute/path/to/QA/goodteam/screenshots-desktop",
    is_mobile=False
)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = qa.create_context(browser)
    page = ctx.new_page()

    # 1. Capture landing page
    page.goto(qa.base_url)
    qa.shot(page, "01_landing_page")

    # 2. Capture dashboard
    qa.login(page, "admin", "password123")
    qa.shot(page, "02_dashboard")

    ctx.close()
    browser.close()
    
    # List generated screenshots
    qa.list_results()
```

### Step 3: Install dependencies and run
```bash
pip install playwright
playwright install
python run_goodteam.py
```

---

## 🛠️ BaseQA API Reference

You can access the following helper methods directly inside your subclass:

| API Method | Parameters | Description |
| :--- | :--- | :--- |
| `__init__` | `base_url`, `out_dir`, `is_mobile`, `viewport` | Initializes target URL, output folders, responsive setups, and UA injections. |
| `create_context(browser)` | `browser` | Returns a Playwright BrowserContext populated with custom viewports and User-Agents. |
| `shot(page, name, full=True)` | `page` (Page), `name` (str), `full` (bool) | Takes a screenshot after a short debounce to allow layout/render settling. Supports full-page scrolling. |
| `wait(page, ms=800)` | `page` (Page), `ms` (int) | Synchronously pauses the flow for the specified milliseconds to control page pacing. |
| `list_results()` | None | Scans the output directory and logs all `.png` files along with their file sizes in KB. |

---

## ⚠️ Safety & Environment Requirements

Automated visual QA scripts simulate actual click events and form submissions. Please ensure the following constraints are followed to avoid **unintentional billing charges** or **security leaks**:

### 1. 💰 API Cost & LLM Protection
* **Avoid High-Cost Billing APIs in CI**: If your UI workflows trigger backend calls to costly Third-Party APIs (such as Large Language Model APIs, paid geocoders, etc.), running these QA suites on high-frequency CI pipelines might quickly exhaust your API quotas and cause unexpectedly high bills.
* **Mock Responses in Development**: For local visual/UI regressions, strongly consider mocking expensive API endpoints on the server/network-interceptor layer or switching to cheaper test-only credentials.

### 2. 🔒 Sandbox Credentials & Auth
* **Use Dedicated Test Credentials**: When testing authenticated states (e.g., Clerk, Auth0, Okta), configure mock accounts in your test database. **Never hardcode real administrator or customer passwords**.
* **Bypass Defensive Guardrails**: Executing raw Playwright scripts on real production setups might trigger Cloudflare Rate Limiting, CAPTCHAs, or IP bans. These scripts are exclusively recommended for **local development servers or Staging sandboxes**.

### 3. 🚫 No Write Operations in Production
* If your subclass flows trigger write operations (such as deleting items, submitting real order invoices, etc.), always implement a domain check. If a production URL is detected, raise an exception to halt the script instantly.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
