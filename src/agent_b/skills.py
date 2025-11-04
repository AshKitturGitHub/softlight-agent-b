from playwright.async_api import Page

COMMON_CREATE_WORDS = ["Create", "New", "Add", "+", "Start", "Make"]
COMMON_SAVE_WORDS   = ["Save", "Submit", "Done", "Create", "OK", "Apply"]

async def click_create(page: Page) -> bool:
    for word in COMMON_CREATE_WORDS:
        try:
            btn = page.get_by_role("button", name=word)
            if await btn.count():
                await btn.first.click()
                return True
        except Exception:
            pass
    for word in COMMON_CREATE_WORDS:
        loc = page.get_by_text(word, exact=False)
        if await loc.count():
            await loc.first.click()
            return True
    return False

async def click_save(page: Page) -> bool:
    for word in COMMON_SAVE_WORDS:
        loc = page.get_by_role("button", name=word)
        if await loc.count():
            await loc.first.click()
            return True
    for word in COMMON_SAVE_WORDS:
        loc = page.get_by_text(word)
        if await loc.count():
            await loc.first.click()
            return True
    return False

async def fill_labeled(page: Page, label: str, value: str) -> bool:
    try:
        ctl = page.get_by_label(label)
        if await ctl.count():
            await ctl.first.fill(value)
            return True
    except Exception:
        pass
    try:
        ctl = page.get_by_placeholder(label)
        if await ctl.count():
            await ctl.first.fill(value)
            return True
    except Exception:
        pass
    return False

async def open_filter_panel(page: Page) -> bool:
    for key in ["Filter", "Add filter", "Filters", "Filter by"]:
        if await page.get_by_role("button", name=key).count():
            await page.get_by_role("button", name=key).first.click()
            return True
        if await page.get_by_text(key).count():
            await page.get_by_text(key).first.click()
            return True
    return False
