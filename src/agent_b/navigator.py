from playwright.async_api import async_playwright
from .detectors import inject_watcher, dom_signature
from .capture import Capturer
from .skills import click_create, click_save, fill_labeled, open_filter_panel

class Navigator:
    def __init__(self, dataset_dir: str):
        self.dataset_dir = dataset_dir

    async def run(self, plan, seed_url: str):
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)
            ctx = await browser.new_context(viewport={"width": 1440, "height": 900})
            page = await ctx.new_page()
            capt = Capturer(self.dataset_dir)
            try:
                await page.goto(seed_url, wait_until="domcontentloaded")
                await inject_watcher(page)
                dh = await dom_signature(page)
                await capt.capture(page, "open", dh)

                for step in plan.steps:
                    if step.intent == "open":
                        await page.goto(step.args.get("url", seed_url), wait_until="networkidle")
                    elif step.intent == "click_create":
                        await click_create(page)
                    elif step.intent == "click_save":
                        await click_save(page)
                    elif step.intent == "fill_form_fields":
                        for k, v in step.args.get("fields", {}).items():
                            await fill_labeled(page, k, v)
                    elif step.intent == "open_filter_panel":
                        await open_filter_panel(page)

                    dh = await dom_signature(page)
                    await capt.capture(page, step.intent, dh)

                capt.flush()
            finally:
                await ctx.close()
                await browser.close()
