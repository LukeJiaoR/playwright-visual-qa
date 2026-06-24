import os

class QASnapshotter:
    """
    Handles screenshot capture with anti-shake pacing and wait mechanism.
    """
    def __init__(self, out_dir: str):
        self.out_dir = out_dir
        os.makedirs(self.out_dir, exist_ok=True)

    def shot(self, page, name: str, full: bool = True, wait_ms: int = 1500):
        """
        Takes a screenshot after a debounce wait to allow layouts, widgets, or animations to settle.
        """
        if wait_ms > 0:
            page.wait_for_timeout(wait_ms)
            
        path = f"{self.out_dir}/{name}.png"
        page.screenshot(path=path, full_page=full)
        print(f"  ✓  {name}.png")
        return path
