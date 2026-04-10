# Sentinel View Counter Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Create a custom Shields.io Endpoint Badge for page views hosted on Vercel with Upstash Redis.

**Architecture:** A Vercel Serverless Function serves a JSON response to Shields.io after incrementing a view count in Upstash Redis.

**Tech Stack:** Node.js, Vercel Functions, Upstash Redis REST API.

---

### Task 1: Initialize Vercel Project Structure

**Files:**
- Create: `sentinel-badge/package.json`
- Create: `sentinel-badge/vercel.json`
- Create: `sentinel-badge/.gitignore`

**Step 1: Create directory and package.json**
Create `sentinel-badge/package.json` with:
```json
{
  "name": "sentinel-view-counter",
  "version": "1.0.0",
  "main": "api/views.js",
  "dependencies": {
    "node-fetch": "^2.6.7"
  }
}
```

**Step 2: Create vercel.json**
Create `sentinel-badge/vercel.json` with:
```json
{
  "version": 2,
  "rewrites": [
    { "source": "/api/views", "destination": "/api/views.js" }
  ]
}
```

**Step 3: Create .gitignore**
Create `sentinel-badge/.gitignore` with:
```text
node_modules
.vercel
.env
```

**Step 4: Commit**
```bash
git add sentinel-badge/
git commit -m "feat: initialize sentinel-badge project structure"
```

---

### Task 2: Implement the View Counter API

**Files:**
- Create: `sentinel-badge/api/views.js`

**Step 1: Write the implementation**
Create `sentinel-badge/api/views.js` with logic to hit Upstash and return Shields JSON.
```javascript
const fetch = require('node-fetch');

module.exports = async (req, res) => {
  const UPSTASH_URL = process.env.UPSTASH_REDIS_REST_URL;
  const UPSTASH_TOKEN = process.env.UPSTASH_REDIS_REST_TOKEN;

  if (!UPSTASH_URL || !UPSTASH_TOKEN) {
    return res.status(500).json({ error: 'Database credentials missing' });
  }

  try {
    // Increment the view count in Redis
    const response = await fetch(`${UPSTASH_URL}/incr/portfolio_views`, {
      headers: { Authorization: `Bearer ${UPSTASH_TOKEN}` }
    });
    const { result: count } = await response.json();

    // Return the Shields.io JSON schema
    res.status(200).json({
      schemaVersion: 1,
      label: 'SENTINEL VIEWS',
      message: count.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","),
      color: parseInt(count) > 1000 ? 'ff9e64' : '7aa2f7',
      labelColor: '1a1b26',
      style: 'for-the-badge'
    });
  } catch (err) {
    res.status(500).json({ error: 'Failed to update view count' });
  }
};
```

**Step 2: Commit**
```bash
git add sentinel-badge/api/views.js
git commit -m "feat: implement view counter logic with Tokyonight colors"
```

---

### Task 3: Portfolio README Integration

**Files:**
- Modify: `_portfolio_repo/README.md`

**Step 1: Update the badge link**
Find the existing hits.se badge and replace it with:
```markdown
![Views](https://img.shields.io/endpoint?url=https://YOUR_VERCEL_URL.vercel.app/api/views)
```

**Step 2: Commit**
```bash
git add _portfolio_repo/README.md
git commit -m "feat: integrate custom Sentinel View badge into README"
```
