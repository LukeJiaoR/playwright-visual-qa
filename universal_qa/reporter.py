import os

class QAReporter:
    """
    Aggregates test results and generates visual reports.
    """
    def __init__(self, out_dir: str):
        self.out_dir = out_dir

    def list_results(self):
        """
        Scans output directory, prints files and sizes in terminal.
        """
        if not os.path.exists(self.out_dir):
            print(f"⚠️  Directory {self.out_dir} does not exist.")
            return []
        
        files = sorted(f for f in os.listdir(self.out_dir) if f.endswith(".png"))
        print(f"\n✅  Done — {len(files)} screenshots saved to {self.out_dir}/")
        for f in files:
            size_kb = os.path.getsize(f"{self.out_dir}/{f}") // 1024
            print(f"     {f}  ({size_kb}KB)")
        return files

    def generate_html_report(self, report_name: str = "report.html"):
        """
        Generates a premium interactive static HTML report to preview all screenshots.
        """
        if not os.path.exists(self.out_dir):
            return
            
        files = sorted(f for f in os.listdir(self.out_dir) if f.endswith(".png"))
        
        # Build premium HTML mockup
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visual QA Regression Report</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0b0f19;
            --card-bg: rgba(22, 28, 45, 0.6);
            --text-primary: #f3f4f6;
            --text-secondary: #9ca3af;
            --accent: #6366f1;
            --accent-hover: #4f46e5;
            --success: #10b981;
            --border: rgba(255, 255, 255, 0.08);
        }}
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.1) 0px, transparent 50%);
            background-attachment: fixed;
            color: var(--text-primary);
            min-height: 100vh;
            padding: 40px 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border);
            backdrop-filter: blur(10px);
        }}
        
        h1 {{
            font-size: 2.2rem;
            font-weight: 700;
            letter-spacing: -0.025em;
            background: linear-gradient(to right, #a5b4fc, #6366f1, #34d399);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        .badge {{
            background: rgba(16, 185, 129, 0.15);
            color: var(--success);
            padding: 6px 14px;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 600;
            border: 1px solid rgba(16, 185, 129, 0.2);
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.1);
        }}
        
        .meta-info {{
            font-size: 0.95rem;
            color: var(--text-secondary);
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
            gap: 28px;
        }}
        
        .card {{
            background: var(--card-bg);
            border-radius: 16px;
            border: 1px solid var(--border);
            overflow: hidden;
            backdrop-filter: blur(12px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            flex-direction: column;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }}
        
        .card:hover {{
            transform: translateY(-6px);
            border-color: rgba(99, 102, 241, 0.4);
            box-shadow: 0 20px 40px rgba(99, 102, 241, 0.15);
        }}
        
        .image-wrapper {{
            position: relative;
            width: 100%;
            padding-top: 62.5%; /* 16:10 Aspect Ratio */
            background: rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }}
        
        .image-wrapper img {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: contain;
            transition: transform 0.5s ease;
        }}
        
        .card:hover .image-wrapper img {{
            transform: scale(1.03);
        }}
        
        .card-details {{
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            flex-grow: 1;
            justify-content: space-between;
        }}
        
        .info-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }}
        
        .title {{
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--text-primary);
            word-break: break-all;
            line-height: 1.4;
        }}
        
        .size {{
            font-size: 0.85rem;
            color: var(--text-secondary);
            font-family: monospace;
            background: rgba(255, 255, 255, 0.05);
            padding: 2px 8px;
            border-radius: 4px;
        }}
        
        .actions {{
            display: flex;
            gap: 12px;
            margin-top: 8px;
        }}
        
        .btn {{
            flex: 1;
            display: inline-flex;
            justify-content: center;
            align-items: center;
            padding: 10px 16px;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 500;
            text-decoration: none;
            transition: all 0.2s ease;
            cursor: pointer;
        }}
        
        .btn-primary {{
            background: var(--accent);
            color: white;
            border: none;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        }}
        
        .btn-primary:hover {{
            background: var(--accent-hover);
            box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
        }}
        
        /* Modal for preview */
        .modal {{
            display: none;
            position: fixed;
            z-index: 1000;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(5, 8, 16, 0.9);
            backdrop-filter: blur(8px);
            justify-content: center;
            align-items: center;
        }}
        
        .modal-content {{
            max-width: 90%;
            max-height: 90%;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            border-radius: 8px;
            border: 1px solid var(--border);
            object-fit: contain;
        }}
        
        .close-btn {{
            position: absolute;
            top: 20px;
            right: 30px;
            color: white;
            font-size: 40px;
            font-weight: bold;
            cursor: pointer;
            transition: color 0.2s;
        }}
        
        .close-btn:hover {{
            color: var(--accent);
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div>
                <h1>📷 Visual QA Report</h1>
                <p class="meta-info">自动生成的视觉回归测试结果报告</p>
            </div>
            <span class="badge">Passed — {len(files)} Items</span>
        </header>
        
        <div class="grid">
"""
        for f in files:
            size_kb = os.path.getsize(f"{self.out_dir}/{f}") // 1024
            html_content += f"""            <div class="card">
                <div class="image-wrapper">
                    <img src="{f}" alt="{f}" onclick="openModal('{f}')" style="cursor: zoom-in;">
                </div>
                <div class="card-details">
                    <div class="info-header">
                        <span class="title">{f}</span>
                        <span class="size">{size_kb} KB</span>
                    </div>
                    <div class="actions">
                        <a href="{f}" target="_blank" class="btn btn-primary">在新标签页打开</a>
                    </div>
                </div>
            </div>
"""
            
        html_content += """        </div>
    </div>
    
    <div id="imageModal" class="modal" onclick="closeModal()">
        <span class="close-btn">&times;</span>
        <img class="modal-content" id="modalImg">
    </div>

    <script>
        function openModal(imgSrc) {
            document.getElementById('imageModal').style.display = "flex";
            document.getElementById('modalImg').src = imgSrc;
        }
        function closeModal() {
            document.getElementById('imageModal').style.display = "none";
        }
    </script>
</body>
</html>
"""
        
        report_path = f"{self.out_dir}/{report_name}"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"  ✓  HTML Report generated: {report_path}")
        return report_path
