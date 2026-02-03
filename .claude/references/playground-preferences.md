# Playground Preferences (Local Override)

**Purpose:** Override default playground plugin settings for Charlie's projects.

**Load this before building any playground.**

---

## Theme: Warm Sand / Notion Aesthetic

Replace the default dark theme with this warm, light palette:

```css
:root {
  --bg: #f5f0e8;           /* Warm cream background */
  --bg-card: #ffffff;       /* White cards */
  --bg-hover: #faf7f2;      /* Subtle hover state */
  --border: #e8e2d9;        /* Soft borders */
  --text: #37352f;          /* Notion-style dark text */
  --text-muted: #9b9a97;    /* Secondary text */
  --accent: #2eaadc;        /* Blue accent */
  --green: #0f7b6c;         /* Success/positive */
  --orange: #d9730d;        /* Warning/attention */
  --red: #e03e3e;           /* Error/negative */
  --purple: #9065b0;        /* Special/highlight */
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.5;
}
```

**Never use:** Dark backgrounds, high-contrast neon colors, or aggressive styling.

---

## Data Persistence: Local Python Server

Instead of copy/paste prompts, use a local Python server for real-time persistence.

### Pattern: serve_[name].py

```python
#!/usr/bin/env python3
"""
[Name] Dashboard Server - Auto-saves changes to [data].json

Run: python3 serve_[name].py
Open: http://localhost:8000
"""

import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

PORT = 8000
DATA_FILE = Path(__file__).parent / "[data].json"

class DashboardHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/dashboard":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(self.generate_dashboard().encode())
        elif self.path == "/[data].json":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            with open(DATA_FILE, 'r') as f:
                self.wfile.write(f.read().encode())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/save":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data)
                with open(DATA_FILE, 'w') as f:
                    json.dump(data, f, indent=2)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "saved"}).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def generate_dashboard(self):
        # Load data and embed in HTML
        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
        except:
            data = {}

        return f'''<!DOCTYPE html>
<html>
<!-- Dashboard HTML with embedded data -->
<script>
let data = {json.dumps(data)};
// ... rest of dashboard
</script>
</html>'''

def main():
    os.chdir(Path(__file__).parent)
    server = HTTPServer(('localhost', PORT), DashboardHandler)
    print(f"Running at http://localhost:{PORT}")
    server.serve_forever()

if __name__ == "__main__":
    main()
```

### Key Benefits
- Claude can read changes directly from JSON file
- No copy/paste workflow needed
- State persists between sessions
- User says "check my changes" and Claude reads the file

---

## UI Components: Consistent Patterns

### Buttons

```css
.btn {
  padding: 6px 10px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 4px;
  color: var(--text);
  cursor: pointer;
  font-size: 0.75rem;
}
.btn:hover { background: var(--border); }

.btn-primary {
  background: var(--green);
  border-color: var(--green);
  color: #fff;
}

.save-btn {
  padding: 8px 16px;
  background: var(--green);
  border: none;
  border-radius: 6px;
  color: #fff;
  font-weight: 500;
}
```

### Cards

```css
.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 12px 16px;
}
```

### Badges

```css
.badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.65rem;
  font-weight: 500;
  text-transform: uppercase;
}
.badge-success { background: #dbeddb; color: var(--green); }
.badge-warning { background: #fdecc8; color: var(--orange); }
.badge-muted { background: #e8e2d9; color: var(--text-muted); }
```

### Modals

```css
.modal-overlay {
  display: none;
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  z-index: 1000;
  align-items: center;
  justify-content: center;
}
.modal-overlay.active { display: flex; }

.modal {
  background: var(--bg-card);
  border-radius: 12px;
  padding: 24px;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}
```

---

## Workflow Actions: Star/Used/Skip Pattern

For curation/review workflows, use this consistent pattern:

```javascript
// Three-state workflow
// ★ Star = save for later (stays in system)
// ✓ Used = processed/published (can be cleared)
// ✗ Skip = rejected (optionally with reason for learning)

function toggleStar(id) {
  data.items[id].starred = !data.items[id].starred;
  markChanged();
  render();
}

function mark(id, status) {
  data.items[id].status = status;
  markChanged();
  render();
}

function markChanged() {
  hasChanges = true;
  document.getElementById('save-btn').textContent = '💾 Save *';
}
```

### Reject with Reason (for learning)

When rejecting items, optionally capture the reason to improve future filtering:

```javascript
function openRejectModal(id, title) {
  rejectingId = id;
  document.getElementById('reject-title').textContent = title;
  document.getElementById('reject-modal').classList.add('active');
}

function submitRejectWithReason() {
  const reason = document.getElementById('reject-reason').value.trim();
  data.items[rejectingId].status = 'rejected';
  data.items[rejectingId].rejectReason = reason;
  markChanged();
  closeRejectModal();
  render();
}
```

---

## Summary: Override Defaults

| Default Plugin | Charlie's Preference |
|----------------|---------------------|
| Dark theme | Warm sand/Notion aesthetic |
| Copy/paste prompt | Local Python server with /save endpoint |
| Static HTML file | serve_[name].py with embedded dashboard |
| Prompt output only | JSON persistence for Claude to read directly |

---

*Created: 2026-02-02*
*Based on: RSS Curation Dashboard workflow*
