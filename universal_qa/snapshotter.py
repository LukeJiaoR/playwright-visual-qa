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
        Automatically removes sticky/fixed element overlapping ghosting when full=True.
        """
        if wait_ms > 0:
            page.wait_for_timeout(wait_ms)
            
        path = f"{self.out_dir}/{name}.png"
        
        # If full page screenshot, temporarily change fixed/sticky to absolute to prevent overlay ghosting
        has_deghosted = False
        if full:
            try:
                page.evaluate("""() => {
                    window._stickyElems = [];
                    document.querySelectorAll('*').forEach(el => {
                        const pos = window.getComputedStyle(el).position;
                        if (pos === 'fixed' || pos === 'sticky') {
                            window._stickyElems.push({el: el, org: el.style.position});
                            el.style.setProperty('position', 'absolute', 'important');
                        }
                    });
                }""")
                has_deghosted = True
            except Exception as e:
                # Silently ignore if JS evaluation fails
                pass
                
        try:
            page.screenshot(path=path, full_page=full)
        finally:
            # Restore original styles
            if has_deghosted:
                try:
                    page.evaluate("""() => {
                        if (window._stickyElems) {
                            window._stickyElems.forEach(x => {
                                x.el.style.position = x.org;
                            });
                            delete window._stickyElems;
                        }
                    }""")
                except Exception:
                    pass
                    
        print(f"  ✓  {name}.png")
        return path
