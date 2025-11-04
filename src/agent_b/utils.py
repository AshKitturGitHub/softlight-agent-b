import asyncio, hashlib, time
from slugify import slugify
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, max=4))
async def wait_js(page, expr: str, timeout_ms: int):
    return await page.wait_for_function(expr, timeout=timeout_ms)

def ts() -> str:
    return time.strftime("%Y%m%d-%H%M%S")

def digest(s: str) -> str:
    return hashlib.sha1(s.encode()).hexdigest()[:8]

def slug(s: str) -> str:
    return slugify(s)[:60]
