from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class QAConfig:
    """
    Configuration model for Playwright Visual QA runs.
    """
    base_url: str
    out_dir: str = "qa-screenshots"
    is_mobile: bool = False
    viewport: Optional[Dict[str, int]] = None
    user_agent: Optional[str] = None
    device: Optional[str] = None  # Playwright device preset name, e.g., "iPhone 12"

    def __post_init__(self):
        # Define friendly presets for commonly tested screen sizes and devices
        device_presets = {
            "iphone": "iPhone 12",
            "iphone_se": "iPhone SE",
            "iphone_pro_max": "iPhone 14 Pro Max",
            "android": "Pixel 5",
            "android_large": "Galaxy S9+",
            "ipad": "iPad Mini",
            "ipad_pro": "iPad Pro 11"
        }
        
        # 1. Resolve screen size/device presets
        if self.device:
            preset_lower = self.device.lower()
            if preset_lower == "desktop_1080p":
                self.viewport = {"width": 1920, "height": 1080}
                self.device = None
                self.is_mobile = False
            elif preset_lower == "desktop":
                self.viewport = {"width": 1280, "height": 800}
                self.device = None
                self.is_mobile = False
            elif preset_lower in device_presets:
                self.device = device_presets[preset_lower]
                self.is_mobile = True
        
        # 2. Apply standard defaults for responsive viewports if not specified
        if not self.viewport and not self.device:
            self.viewport = {"width": 390, "height": 844} if self.is_mobile else {"width": 1280, "height": 800}
        
        # 3. Standard mobile iPhone user agent to trigger responsive layout styles
        if not self.user_agent and self.is_mobile and not self.device:
            self.user_agent = (
                "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
            )
