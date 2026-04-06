import asyncio
import socket
import httpx
from typing import AsyncGenerator

WORDLIST = [
    "www", "mail", "ftp", "api", "dev", "staging", "admin",
    "portal", "app", "test", "vpn", "remote", "cdn", "assets",
    "static", "blog", "shop", "auth", "login", "dashboard",
    "beta", "old", "new", "secure", "m", "mobile", "support",
    "docs", "status", "monitor", "grafana", "prometheus", "jenkins"
]

async def resolve_subdomain(subdomain: str, domain: str) -> dict | None:
    fqdn = f"{subdomain}.{domain}"
    try:
        ip = await asyncio.get_event_loop().run_in_executor(
            None, socket.gethostbyname, fqdn
        )
        return {"subdomain": fqdn, "ip": ip, "status": "resolved"}
    except socket.gaierror:
        return None

async def probe_http(fqdn: str, client: httpx.AsyncClient) -> dict:
    for scheme in ["https", "http"]:
        try:
            r = await client.get(f"{scheme}://{fqdn}", timeout=5.0, follow_redirects=True)
            return {
                "subdomain": fqdn,
                "url": str(r.url),
                "status_code": r.status_code,
                "alive": True
            }
        except Exception:
            continue
    return {"subdomain": fqdn, "url": None, "status_code": None, "alive": False}

async def run_recon(domain: str) -> AsyncGenerator[dict, None]:
    tasks = [resolve_subdomain(sub, domain) for sub in WORDLIST]
    resolved = []

    for coro in asyncio.as_completed(tasks):
        result = await coro
        if result:
            resolved.append(result)
            yield {"type": "resolved", "data": result}

    async with httpx.AsyncClient(verify=False) as client:
        probe_tasks = [probe_http(r["subdomain"], client) for r in resolved]
        for coro in asyncio.as_completed(probe_tasks):
            result = await coro
            yield {"type": "probed", "data": result}

    yield {"type": "done", "data": {"total": len(resolved)}}
