import asyncio
from playwright.async_api import async_playwright
from tenacity import retry, stop_after_attempt, wait_fixed
from .capture import Capturer
from .detectors import get_dom_hash


class Navigator:
    """
    Executes a plan in a real browser (Chromium) using Playwright.
    Handles UI actions, waits for stability, and triggers capture events.
    """

    def __init__(self, writer):
        self.writer = writer
        self.dataset_dir = writer.dir

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    async def safe_goto(self, page, url: str):
        """Navigate to a URL with retry logic."""
        print(f"[AgentB] Navigating to {url}")
        await page.goto(url, timeout=20000)
        await page.wait_for_load_state("networkidle")
        print(f"[AgentB] Page loaded: {url}")

    async def run(self, plan, seed_url: str):
        """Run through all steps of the generated plan."""
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)
            page = await browser.new_page()

            await self.safe_goto(page, seed_url)

            capt = Capturer(self.dataset_dir)

            for step in plan.steps:
                label = step.label
                print(f"[AgentB] Executing step: {label}")

                try:
                    dom_hash = await get_dom_hash(page)

                    await capt.capture(page, label, dom_hash)

                    await asyncio.sleep(1.5)  
                except Exception as e:
                    print(f"[AgentB] Step '{label}' failed: {e}")

            await browser.close()
            print("[AgentB] Navigation and capture complete.")

