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
        import time
        timestamp = int(time.time())
        for f in files:
            size_kb = os.path.getsize(f"{self.out_dir}/{f}") // 1024
            html_content += f"""            <div class="card">
                <div class="image-wrapper">
                    <img src="{f}?t={timestamp}" alt="{f}" onclick="openModal('{f}?t={timestamp}')" style="cursor: zoom-in;">
                </div>
                <div class="card-details">
                    <div class="info-header">
                        <span class="title">{f}</span>
                        <span class="size">{size_kb} KB</span>
                    </div>
                    <div class="actions">
                        <a href="{f}?t={timestamp}" target="_blank" class="btn btn-primary">在新标签页打开</a>
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
        
        # Automatically refresh the global history index portal
        self.generate_index_report()
        return report_path

    def generate_index_report(self):
        """
        Scans parent directory for all run_* directories containing report.html
        and scaffolds/updates a global index.html dashboard portal.
        """
        # Ensure we work with absolute path to locate parent dir
        abs_out_dir = os.path.abspath(self.out_dir)
        parent_dir = os.path.dirname(abs_out_dir)
        
        # If parent_dir is empty or same, fallback
        if not parent_dir or parent_dir == abs_out_dir:
            return None
            
        # Scan all subdirectories that contain report.html
        run_dirs = []
        try:
            for entry in os.scandir(parent_dir):
                if entry.is_dir() and entry.name.startswith("run_"):
                    report_file = os.path.join(entry.path, "report.html")
                    if os.path.exists(report_file):
                        # Get creation/modification time of the folder or report
                        mtime = os.path.getmtime(report_file)
                        import time
                        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mtime))
                        run_dirs.append({
                            "name": entry.name,
                            "path": entry.name,
                            "report_url": f"{entry.name}/report.html",
                            "time": formatted_time,
                            "mtime": mtime
                        })
        except Exception as e:
            print(f"⚠️  Failed to scan history directories for index.html: {e}")
            return None
            
        if not run_dirs:
            return None
            
        # Sort runs by modification time, newest first
        run_dirs.sort(key=lambda x: x["mtime"], reverse=True)
        
        # Render dynamic runs list items
        runs_html = ""
        for idx, run in enumerate(run_dirs):
            active_class = "active" if idx == 0 else ""
            runs_html += f"""            <li class="run-item {active_class}" onclick="loadRun(this, '{run['report_url']}')">
                <div class="run-name">{run['name']}</div>
                <div class="run-date">运行于: {run['time']}</div>
            </li>
"""
            
        # Build global index HTML
        index_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visual QA Test Runs Index Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #0b0f19;
            --sidebar-bg: #111827;
            --card-bg: rgba(22, 28, 45, 0.6);
            --text-primary: #f3f4f6;
            --text-secondary: #9ca3af;
            --accent: #6366f1;
            --accent-hover: #4f46e5;
            --border: rgba(255, 255, 255, 0.08);
        }}
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        body {{
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg);
            color: var(--text-primary);
            display: flex;
            height: 100vh;
            overflow: hidden;
        }}
        .sidebar {{
            width: 320px;
            background: var(--sidebar-bg);
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            padding: 24px;
            overflow-y: auto;
        }}
        .sidebar h2 {{
            font-size: 1.4rem;
            font-weight: 700;
            margin-bottom: 24px;
            background: linear-gradient(to right, #a5b4fc, #6366f1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .run-list {{
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}
        .run-item {{
            padding: 14px 16px;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border);
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        .run-item:hover {{
            border-color: rgba(99, 102, 241, 0.4);
            background: rgba(99, 102, 241, 0.05);
            transform: translateY(-2px);
        }}
        .run-item.active {{
            background: var(--accent);
            border-color: var(--accent);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.35);
        }}
        .run-item.active .run-name {{
            color: white;
        }}
        .run-item.active .run-date {{
            color: rgba(255, 255, 255, 0.7);
        }}
        .run-name {{
            font-weight: 600;
            font-size: 0.95rem;
            color: var(--text-primary);
            margin-bottom: 4px;
            word-break: break-all;
        }}
        .run-date {{
            font-size: 0.8rem;
            color: var(--text-secondary);
        }}
        .main-content {{
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            height: 100%;
        }}
        iframe {{
            border: none;
            width: 100%;
            height: 100%;
            background: var(--bg);
        }}
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>📷 Runs History</h2>
        <ul class="run-list">
{runs_html}
        </ul>
    </div>
    <div class="main-content">
        <iframe id="reportFrame" src=""></iframe>
    </div>
    <script>
        function loadRun(element, reportUrl) {{
            document.querySelectorAll('.run-item').forEach(el => el.classList.remove('active'));
            element.classList.add('active');
            document.getElementById('reportFrame').src = reportUrl;
        }}
        
        // Auto select first run
        window.onload = () => {{
            const firstRun = document.querySelector('.run-item');
            if (firstRun) {{
                firstRun.click();
            }}
        }}
    </script>
</body>
</html>
"""
        index_path = os.path.join(parent_dir, "index.html")
        try:
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(index_content)
            print(f"  ✓  Global Runs Index updated: {index_path}")
        except Exception as e:
            print(f"⚠️  Failed to write global index.html: {e}")
            
        return index_path
        return report_path
