import os
from playwright.sync_api import sync_playwright
from .config import QAConfig

class QARunner:
    """
    Context manager that automatically manages Playwright, Browser, and Context lifecycles.
    """
    def __init__(self, config: QAConfig, headless: bool = True):
        self.config = config
        self.headless = headless
        self._playwright = None
        self._browser = None
        self._context = None
        os.makedirs(self.config.out_dir, exist_ok=True)

    def __enter__(self):
        # Start Playwright sync driver
        self._playwright = sync_playwright().start()
        
        # Launch chromium browser
        self._browser = self._playwright.chromium.launch(headless=self.headless)
        
        context_args = {}
        
        # 1. Load device preset if specified, or default to iPhone 12 for is_mobile
        if self.config.device:
            device_preset = self._playwright.devices.get(self.config.device)
            if device_preset:
                context_args.update(device_preset)
            else:
                print(f"⚠️  Warning: Device preset '{self.config.device}' not found.")
        elif self.config.is_mobile:
            device_preset = self._playwright.devices.get("iPhone 12")
            if device_preset:
                context_args.update(device_preset)
        
        # 2. Manual configs override presets
        if self.config.viewport:
            context_args["viewport"] = self.config.viewport
        if self.config.user_agent:
            context_args["user_agent"] = self.config.user_agent

        # Fallback viewport
        if "viewport" not in context_args:
            context_args["viewport"] = {"width": 1280, "height": 800}
            
        self._context = self._browser.new_context(**context_args)
        
        # Create a default page and return it for user action
        page = self._context.new_page()
        return page

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Safely tear down all Playwright resources
        if self._context:
            self._context.close()
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()
