# Recon SaaS — Bug Bounty Dashboard

Real-time subdomain enumeration and HTTP probing dashboard for Attack Surface Management.

## Features
- 🔍 Subdomain enumeration via async DNS resolution
- 🌐 HTTP/HTTPS probing with status codes
- 📊 Live dashboard with WebSocket updates
- 📥 Export results as JSON

## Stack
- **Backend:** FastAPI + WebSocket + httpx + asyncio
- **Frontend:** Tailwind CSS + Vanilla JS
- **Container:** Docker + docker-compose

## Running

```bash
docker-compose up --build
```

Access: http://localhost:8000

## Usage
1. Enter target domain (e.g. `example.com`)
2. Click **Run Recon**
3. Watch results in real-time
4. Export JSON for Bug Bounty report

> ⚠️ Use only on authorized targets.
