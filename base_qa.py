import os
from universal_qa.config import QAConfig
from universal_qa.snapshotter import QASnapshotter
from universal_qa.reporter import QAReporter

class BaseQA:
    """
    Universal Base QA class for Playwright-based screenshot automation.
    Delegates implementation to universal_qa package modules for backward compatibility.
    """
    def __init__(self, base_url, out_dir="qa-screenshots", is_mobile=False, viewport=None):
        # Delegate initialization to the modular QAConfig
        self.config = QAConfig(
            base_url=base_url,
            out_dir=out_dir,
            is_mobile=is_mobile,
            viewport=viewport
        )
        
        # Expose properties to ensure full backward compatibility
        self.base_url = self.config.base_url
        self.out_dir = self.config.out_dir
        self.is_mobile = self.config.is_mobile
        self.viewport = self.config.viewport
        self.user_agent = self.config.user_agent
        
        # Instantiate modular components
        self._snapshotter = QASnapshotter(self.out_dir)
        self._reporter = QAReporter(self.out_dir)
        self._shot_count = 0

    def create_context(self, browser):
        """
        Creates context using current viewport and user_agent config.
        """
        context_args = {"viewport": self.viewport}
        if self.user_agent:
            context_args["user_agent"] = self.user_agent
        if self.is_mobile:
            context_args["is_mobile"] = True
            context_args["has_touch"] = True
        return browser.new_context(**context_args)

    def wait(self, page, ms=800):
        """
        Performs pacing wait.
        """
        page.wait_for_timeout(ms)

    def shot(self, page, name, full=True, wait_ms=1500):
        """
        Takes screenshot. Automatically prepends sequential counter prefix if not already present.
        """
        self._shot_count += 1
        
        import re
        if not re.match(r"^\d+[-_]", name):
            formatted_name = f"{self._shot_count:02d}_{name}"
        else:
            formatted_name = name
            
        self._snapshotter.shot(page, formatted_name, full=full, wait_ms=wait_ms)

    def list_results(self):
        """
        Lists screenshots in terminal and generates HTML interactive report.
        """
        self._reporter.list_results()
        # Generates premium HTML preview report alongside
        self._reporter.generate_html_report()
