#!/usr/bin/env python3
"""
RSS Dashboard Server - Auto-saves changes to tracking.json

Run: python3 serve_dashboard.py
Open: http://localhost:8000
"""

import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

PORT = 8000
TRACKING_FILE = Path(__file__).parent / "tracking.json"

class DashboardHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/dashboard":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(self.generate_dashboard().encode())
        elif self.path == "/tracking.json":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            with open(TRACKING_FILE, 'r') as f:
                self.wfile.write(f.read().encode())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/save":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data)
                with open(TRACKING_FILE, 'w') as f:
                    json.dump(data, f, indent=2)

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "saved"}).encode())
                print(f"✓ Saved {len(data.get('items', {}))} items to tracking.json")
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def generate_dashboard(self):
        # Load current tracking data
        try:
            with open(TRACKING_FILE, 'r') as f:
                data = json.load(f)
        except:
            data = {"lastRun": None, "items": {}, "stats": {}}

        return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RSS Curation Dashboard</title>
  <style>
    :root {{
      --bg: #f5f0e8;
      --bg-card: #ffffff;
      --bg-hover: #faf7f2;
      --border: #e8e2d9;
      --text: #37352f;
      --text-muted: #9b9a97;
      --accent: #2eaadc;
      --green: #0f7b6c;
      --orange: #d9730d;
      --red: #e03e3e;
      --purple: #9065b0;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      padding: 24px;
      line-height: 1.5;
    }}
    h1 {{ font-size: 1.5rem; font-weight: 600; margin-bottom: 4px; }}
    h2 {{ font-size: 0.875rem; font-weight: 400; color: var(--text-muted); margin-bottom: 20px; }}
    .dashboard {{ max-width: 900px; margin: 0 auto; }}
    .stats-row {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(90px, 1fr));
      gap: 12px;
      margin-bottom: 20px;
    }}
    .stat-card {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px;
      text-align: center;
    }}
    .stat-card .label {{ color: var(--text-muted); font-size: 0.7rem; text-transform: uppercase; }}
    .stat-card .value {{ font-size: 1.5rem; font-weight: 600; }}
    .stat-card.definitely .value {{ color: var(--green); }}
    .stat-card.probably .value {{ color: var(--orange); }}
    .stat-card.new .value {{ color: var(--accent); }}
    .toolbar {{
      display: flex;
      gap: 12px;
      margin-bottom: 16px;
      flex-wrap: wrap;
      align-items: center;
    }}
    .toolbar select {{
      padding: 8px 12px;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 6px;
      color: var(--text);
      font-size: 0.85rem;
    }}
    .showing {{ color: var(--text-muted); font-size: 0.8rem; margin-left: auto; }}
    .save-btn {{
      padding: 8px 16px;
      background: var(--green);
      border: none;
      border-radius: 6px;
      color: #fff;
      font-size: 0.85rem;
      font-weight: 500;
      cursor: pointer;
    }}
    .save-btn:hover {{ opacity: 0.9; }}
    .save-btn.saving {{ background: var(--orange); }}
    .save-btn.saved {{ background: var(--purple); }}
    .item-list {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 8px;
    }}
    .item {{
      padding: 12px 16px;
      border-bottom: 1px solid var(--border);
      display: flex;
      gap: 12px;
      align-items: flex-start;
    }}
    .btn-star {{
      background: transparent;
      border: 1px solid var(--border);
      font-size: 1rem;
      padding: 4px 8px;
    }}
    .btn-star.starred {{
      background: #fff8e6;
      border-color: #f5c518;
    }}
    .item.starred {{
      background: #fffdf5;
    }}
    .item:last-child {{ border-bottom: none; }}
    .item:hover {{ background: var(--bg-hover); }}
    .item-main {{ flex: 1; min-width: 0; }}
    .item-title {{
      color: var(--text);
      font-size: 0.9rem;
      font-weight: 500;
      text-decoration: none;
      display: block;
      margin-bottom: 4px;
    }}
    .item-title:hover {{ color: var(--accent); }}
    .item-meta {{
      color: var(--text-muted);
      font-size: 0.75rem;
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }}
    .item-summary {{
      color: var(--text-muted);
      font-size: 0.8rem;
      line-height: 1.4;
      margin-top: 4px;
      max-height: 2.8em;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .item-summary.expanded {{
      max-height: none;
    }}
    .engagement {{
      display: inline-flex;
      gap: 6px;
      font-size: 0.7rem;
      color: var(--text-muted);
    }}
    .engagement span {{
      background: var(--bg);
      padding: 1px 5px;
      border-radius: 3px;
    }}
    .badge {{
      display: inline-block;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 0.65rem;
      font-weight: 500;
      text-transform: uppercase;
    }}
    .badge-definitely {{ background: #dbeddb; color: var(--green); }}
    .badge-probably {{ background: #fdecc8; color: var(--orange); }}
    .badge-no {{ background: #e8e2d9; color: var(--text-muted); }}
    .badge-new {{ background: #d3e5ef; color: var(--accent); }}
    .badge-published {{ background: #e8deee; color: var(--purple); }}
    .badge-rejected {{ background: #e8e2d9; color: var(--text-muted); }}
    .item-actions {{ display: flex; gap: 6px; flex-shrink: 0; }}
    .btn {{
      padding: 6px 10px;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 4px;
      color: var(--text);
      cursor: pointer;
      font-size: 0.75rem;
    }}
    .btn:hover {{ background: var(--border); }}
    .btn-publish {{ background: var(--green); border-color: var(--green); color: #fff; }}
    .btn-publish:hover {{ opacity: 0.9; background: var(--green); }}
    .empty {{ padding: 40px; text-align: center; color: var(--text-muted); }}
    .status-bar {{
      margin-top: 16px;
      padding: 12px 16px;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 8px;
      font-size: 0.8rem;
      color: var(--text-muted);
    }}
    .btn-clear {{
      padding: 8px 16px;
      background: var(--text-muted);
      border: none;
      border-radius: 6px;
      color: #fff;
      font-size: 0.85rem;
      cursor: pointer;
    }}
    .btn-clear:hover {{ opacity: 0.9; }}
    .modal-overlay {{
      display: none;
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0,0,0,0.5);
      z-index: 1000;
      align-items: center;
      justify-content: center;
    }}
    .modal-overlay.active {{ display: flex; }}
    .modal {{
      background: var(--bg-card);
      border-radius: 12px;
      padding: 24px;
      max-width: 500px;
      width: 90%;
      box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }}
    .modal h3 {{ margin-bottom: 8px; font-size: 1rem; }}
    .modal p {{ color: var(--text-muted); font-size: 0.85rem; margin-bottom: 16px; }}
    .modal textarea {{
      width: 100%;
      min-height: 100px;
      padding: 12px;
      border: 1px solid var(--border);
      border-radius: 6px;
      font-family: inherit;
      font-size: 0.85rem;
      resize: vertical;
      margin-bottom: 16px;
    }}
    .modal-actions {{ display: flex; gap: 8px; justify-content: flex-end; }}
    .modal .btn {{ padding: 8px 16px; }}
  </style>
</head>
<body>
  <div class="dashboard">
    <h1>📡 RSS Curation Dashboard</h1>
    <h2>Last run: <span id="last-run">Loading...</span></h2>

    <div class="stats-row">
      <div class="stat-card"><div class="label">Total</div><div class="value" id="stat-total">0</div></div>
      <div class="stat-card definitely"><div class="label">Definitely</div><div class="value" id="stat-definitely">0</div></div>
      <div class="stat-card probably"><div class="label">Probably</div><div class="value" id="stat-probably">0</div></div>
      <div class="stat-card new"><div class="label">New</div><div class="value" id="stat-new">0</div></div>
      <div class="stat-card"><div class="label">Used</div><div class="value" id="stat-published">0</div></div>
      <div class="stat-card"><div class="label">Skipped</div><div class="value" id="stat-rejected">0</div></div>
      <div class="stat-card" style="border-color: #f5c518;"><div class="label">Starred</div><div class="value" id="stat-starred" style="color: #d4a000;">0</div></div>
    </div>

    <div class="tabs" style="display:flex;gap:0;margin-bottom:16px;border-bottom:2px solid var(--border);">
      <button class="tab active" id="tab-triage" onclick="switchTab('triage')" style="padding:10px 20px;border:none;background:none;font-size:0.9rem;font-weight:600;cursor:pointer;border-bottom:2px solid var(--accent);margin-bottom:-2px;color:var(--accent);">Triage</button>
      <button class="tab" id="tab-curated" onclick="switchTab('curated')" style="padding:10px 20px;border:none;background:none;font-size:0.9rem;font-weight:500;cursor:pointer;border-bottom:2px solid transparent;margin-bottom:-2px;color:var(--text-muted);">Curated (★)</button>
    </div>

    <div class="toolbar" id="toolbar-triage">
      <select id="filter-status" onchange="render()">
        <option value="new">New only</option>
        <option value="all">All statuses</option>
        <option value="starred">Starred only</option>
        <option value="published">Used</option>
        <option value="rejected">Skipped</option>
      </select>
      <select id="filter-score" onchange="render()">
        <option value="all">All scores</option>
        <option value="definitely">DEFINITELY</option>
        <option value="probably">PROBABLY</option>
        <option value="no">NO</option>
      </select>
      <select id="filter-source" onchange="render()">
        <option value="all">All sources</option>
      </select>
      <select id="filter-channel" onchange="render()">
        <option value="all">All channels</option>
        <option value="rss">RSS Feeds</option>
        <option value="reddit">Reddit</option>
        <option value="x">X/Twitter</option>
        <option value="hn">Hacker News</option>
      </select>
      <span class="showing" id="showing"></span>
      <button class="btn-clear" onclick="clearProcessed()">🗑 Clear Done</button>
      <button class="save-btn" id="save-btn" onclick="saveToServer()">💾 Save</button>
    </div>

    <div class="toolbar" id="toolbar-curated" style="display:none;">
      <span style="font-size:0.85rem;color:var(--text-muted);">Starred items for newsletter curation. Drag to reorder. Click to expand.</span>
      <span class="showing" id="showing-curated"></span>
      <button class="save-btn" onclick="saveToServer()">💾 Save</button>
    </div>

    <div class="item-list" id="items"></div>

    <div class="status-bar" id="status-bar">
      Ready. Changes auto-save to tracking.json when you click Save.
    </div>
  </div>

  <div class="modal-overlay" id="reject-modal">
    <div class="modal">
      <h3>Why skip this item?</h3>
      <p id="reject-title"></p>
      <textarea id="reject-reason" placeholder="e.g., Off-topic policy article, not relevant to homeschooling..."></textarea>
      <div class="modal-actions">
        <button class="btn" onclick="closeRejectModal()">Cancel</button>
        <button class="btn" onclick="submitReject()">Skip without reason</button>
        <button class="btn btn-publish" style="background: var(--red); border-color: var(--red);" onclick="submitRejectWithReason()">Skip with reason</button>
      </div>
    </div>
  </div>

  <script>
    let data = {json.dumps(data)};
    let hasChanges = false;
    let currentTab = 'triage';

    function switchTab(tab) {{
      currentTab = tab;
      document.querySelectorAll('.tab').forEach(t => {{
        t.style.borderBottomColor = 'transparent';
        t.style.color = 'var(--text-muted)';
        t.style.fontWeight = '500';
      }});
      const active = document.getElementById('tab-' + tab);
      active.style.borderBottomColor = 'var(--accent)';
      active.style.color = 'var(--accent)';
      active.style.fontWeight = '600';
      document.getElementById('toolbar-triage').style.display = tab === 'triage' ? 'flex' : 'none';
      document.getElementById('toolbar-curated').style.display = tab === 'curated' ? 'flex' : 'none';
      render();
    }}

    function getChannel(url, source) {{
      if (source === 'X/Twitter') return 'x';
      if (source === 'Hacker News') return 'hn';
      if (url.includes('reddit.com') || (source && source.startsWith('r/'))) return 'reddit';
      return 'rss';
    }}

    function init() {{
      document.getElementById('last-run').textContent = data.lastRun
        ? new Date(data.lastRun).toLocaleString()
        : 'Never';
      const sources = [...new Set(Object.values(data.items).map(i => i.source))].sort();
      const sel = document.getElementById('filter-source');
      sources.forEach(s => sel.innerHTML += `<option value="${{s}}">${{s}}</option>`);
      render();
    }}

    function render() {{
      const status = document.getElementById('filter-status').value;
      const score = document.getElementById('filter-score').value;
      const source = document.getElementById('filter-source').value;

      const items = Object.values(data.items);
      document.getElementById('stat-total').textContent = items.length;
      document.getElementById('stat-definitely').textContent = items.filter(i => i.score === 'definitely').length;
      document.getElementById('stat-probably').textContent = items.filter(i => i.score === 'probably').length;
      document.getElementById('stat-new').textContent = items.filter(i => i.status === 'new').length;
      document.getElementById('stat-published').textContent = items.filter(i => i.status === 'published').length;
      document.getElementById('stat-rejected').textContent = items.filter(i => i.status === 'rejected').length;
      document.getElementById('stat-starred').textContent = items.filter(i => i.starred).length;

      const channel = document.getElementById('filter-channel') ? document.getElementById('filter-channel').value : 'all';

      let filtered;
      if (currentTab === 'curated') {{
        // Curated tab: only starred items
        filtered = Object.entries(data.items).filter(([url, item]) => item.starred);
        const curatedCount = document.getElementById('showing-curated');
        if (curatedCount) curatedCount.textContent = `${{filtered.length}} starred items`;
      }} else {{
        filtered = Object.entries(data.items)
          .filter(([url, item]) => {{
            if (status === 'starred') {{
              if (!item.starred) return false;
            }} else if (status === 'new') {{
              if (item.status !== 'new') return false;
            }} else if (status !== 'all' && item.status !== status) return false;
            if (score !== 'all' && item.score !== score) return false;
            if (source !== 'all' && item.source !== source) return false;
            if (channel !== 'all' && getChannel(url, item.source) !== channel) return false;
            return true;
          }});
      }}

      filtered = filtered.sort((a, b) => {{
          const scoreOrder = {{ definitely: 0, probably: 1, no: 2 }};
          const sA = scoreOrder[a[1].score] ?? 99;
          const sB = scoreOrder[b[1].score] ?? 99;
          if (sA !== sB) return sA - sB;
          return (b[1].firstSeen || '').localeCompare(a[1].firstSeen || '');
        }});

      document.getElementById('showing').textContent = `${{filtered.length}} items`;

      const container = document.getElementById('items');
      if (!filtered.length) {{
        container.innerHTML = '<div class="empty">No items match filters</div>';
        return;
      }}

      container.innerHTML = filtered.map(([url, item]) => `
        <div class="item ${{item.starred ? 'starred' : ''}}">
          <div class="item-main">
            <a class="item-title" href="${{url}}" target="_blank">${{item.title || url}}</a>
            <div class="item-meta">
              <span style="background:${{
                getChannel(url, item.source) === 'x' ? '#1DA1F2' :
                getChannel(url, item.source) === 'reddit' ? '#FF4500' :
                getChannel(url, item.source) === 'hn' ? '#FF6600' : 'var(--text-muted)'
              }};color:#fff;padding:1px 6px;border-radius:3px;font-size:0.65rem;">${{
                getChannel(url, item.source) === 'x' ? 'X' :
                getChannel(url, item.source) === 'reddit' ? 'Reddit' :
                getChannel(url, item.source) === 'hn' ? 'HN' : 'RSS'
              }}</span>
              <span>${{item.source || '?'}}</span>
              ${{item.author ? `<span>${{item.author}}</span>` : ''}}
              <span>${{item.firstSeen || '?'}}</span>
              <span class="badge badge-${{item.score}}">${{(item.score || '?').toUpperCase()}}</span>
              ${{item.upvotes ? `<span class="engagement"><span>♥ ${{item.upvotes}}</span>${{item.retweets ? `<span>🔁 ${{item.retweets}}</span>` : ''}}<span>💬 ${{item.num_comments || 0}}</span></span>` : ''}}
            </div>
            ${{item.summary ? `<div class="item-summary" onclick="this.classList.toggle('expanded')">${{item.summary.replace(/</g, '&lt;').replace(/>/g, '&gt;')}}</div>` : ''}}
          </div>
          <div class="item-actions">
            <button class="btn btn-star ${{item.starred ? 'starred' : ''}}" onclick="toggleStar('${{encodeURIComponent(url)}}')">${{item.starred ? '★' : '☆'}}</button>
            ${{item.status === 'new' ? `
              <button class="btn btn-publish" onclick="mark('${{encodeURIComponent(url)}}','published')">✓ Used</button>
              <button class="btn" onclick="openRejectModal('${{encodeURIComponent(url)}}', '${{(item.title || url).replace(/'/g, "\\\\'")}}')" >✗ Skip</button>
            ` : `
              <button class="btn" onclick="mark('${{encodeURIComponent(url)}}','new')">↩ Reset</button>
              ${{item.rejectReason ? `<span style="font-size:0.7rem;color:var(--text-muted);" title="${{item.rejectReason}}">📝</span>` : ''}}
            `}}
          </div>
        </div>
      `).join('');
    }}

    function toggleStar(encodedUrl) {{
      const url = decodeURIComponent(encodedUrl);
      if (data.items[url]) {{
        data.items[url].starred = !data.items[url].starred;
        markChanged();
        render();
      }}
    }}

    let rejectingUrl = null;

    function openRejectModal(encodedUrl, title) {{
      rejectingUrl = decodeURIComponent(encodedUrl);
      document.getElementById('reject-title').textContent = title;
      document.getElementById('reject-reason').value = '';
      document.getElementById('reject-modal').classList.add('active');
    }}

    function closeRejectModal() {{
      document.getElementById('reject-modal').classList.remove('active');
      rejectingUrl = null;
    }}

    function submitReject() {{
      if (rejectingUrl && data.items[rejectingUrl]) {{
        data.items[rejectingUrl].status = 'rejected';
        markChanged();
        closeRejectModal();
        render();
      }}
    }}

    function submitRejectWithReason() {{
      if (rejectingUrl && data.items[rejectingUrl]) {{
        const reason = document.getElementById('reject-reason').value.trim();
        data.items[rejectingUrl].status = 'rejected';
        data.items[rejectingUrl].rejectReason = reason || 'No reason given';
        markChanged();
        closeRejectModal();
        render();
      }}
    }}

    function clearProcessed() {{
      if (!confirm('Remove all items marked as Used or Skipped (without reason)?\\n\\nItems with reject reasons will be kept for prompt learning.')) return;
      const toRemove = [];
      for (const [url, item] of Object.entries(data.items)) {{
        if (item.status === 'published' || (item.status === 'rejected' && !item.rejectReason)) {{
          toRemove.push(url);
        }}
      }}
      toRemove.forEach(url => delete data.items[url]);
      markChanged();
      document.getElementById('status-bar').textContent = `Cleared ${{toRemove.length}} items. Don't forget to Save!`;
      render();
    }}

    function markChanged() {{
      hasChanges = true;
      document.getElementById('save-btn').textContent = '💾 Save *';
      document.getElementById('status-bar').textContent = 'Unsaved changes...';
    }}

    function mark(encodedUrl, status) {{
      const url = decodeURIComponent(encodedUrl);
      if (data.items[url]) {{
        data.items[url].status = status;
        if (status === 'new') delete data.items[url].rejectReason;
        markChanged();
        render();
      }}
    }}

    async function saveToServer() {{
      const btn = document.getElementById('save-btn');
      const statusBar = document.getElementById('status-bar');

      btn.textContent = '⏳ Saving...';
      btn.classList.add('saving');

      try {{
        const response = await fetch('/save', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify(data)
        }});

        if (response.ok) {{
          btn.textContent = '✓ Saved!';
          btn.classList.remove('saving');
          btn.classList.add('saved');
          statusBar.textContent = `Saved at ${{new Date().toLocaleTimeString()}}. Claude can now read tracking.json to see your changes.`;
          hasChanges = false;

          setTimeout(() => {{
            btn.textContent = '💾 Save';
            btn.classList.remove('saved');
          }}, 2000);
        }} else {{
          throw new Error('Save failed');
        }}
      }} catch (e) {{
        btn.textContent = '❌ Error';
        statusBar.textContent = 'Save failed: ' + e.message;
        setTimeout(() => btn.textContent = '💾 Save *', 2000);
      }}
    }}

    init();
  </script>
</body>
</html>'''

def main():
    os.chdir(Path(__file__).parent)
    server = HTTPServer(('localhost', PORT), DashboardHandler)
    print(f"🚀 RSS Dashboard running at http://localhost:{PORT}")
    print(f"📁 Saving to: {TRACKING_FILE}")
    print("Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Stopped")

if __name__ == "__main__":
    main()
