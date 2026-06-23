import os

class BaseQA:
    """
    Universal Base QA class for Playwright-based screenshot automation.
    Handles device/viewport setup, screenshot capture, wait management, and results listing.
    """
    def __init__(self, base_url, out_dir="qa-screenshots", is_mobile=False, viewport=None):
        self.base_url = base_url
        self.out_dir = out_dir
        self.is_mobile = is_mobile
        
        if viewport:
            self.viewport = viewport
        else:
            self.viewport = {"width": 390, "height": 844} if is_mobile else {"width": 1280, "height": 800}
            
        self.user_agent = (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
            if is_mobile else None
        )
        os.makedirs(self.out_dir, exist_ok=True)

    def create_context(self, browser):
        context_args = {"viewport": self.viewport}
        if self.user_agent:
            context_args["user_agent"] = self.user_agent
        return browser.new_context(**context_args)

    def wait(self, page, ms=800):
        page.wait_for_timeout(ms)

    def shot(self, page, name, full=True):
        path = f"{self.out_dir}/{name}.png"
        page.screenshot(path=path, full_page=full)
        print(f"  ✓  {name}.png")

    def list_results(self):
        files = sorted(f for f in os.listdir(self.out_dir) if f.endswith(".png"))
        print(f"\n✅  Done — {len(files)} screenshots saved to {self.out_dir}/")
        for f in files:
            size_kb = os.path.getsize(f"{self.out_dir}/{f}") // 1024
            print(f"     {f}  ({size_kb}KB)")
