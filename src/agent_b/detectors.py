from dataclasses import dataclass
from PIL import Image
import imagehash
import orjson
import hashlib

@dataclass
class StateSignature:
    url_hash: str
    dom_hash: str
    img_phash: str

    def key(self) -> str:
        return f"{self.url_hash}-{self.dom_hash}-{self.img_phash}"

MUTATION_WATCHER = r"""
(() => {
  const target = document.body;
  const state = { last: Date.now(), deltas: 0 };
  const obs = new MutationObserver((muts) => {
    state.deltas += muts.length;
    window.__agentb_state = state;
  });
  obs.observe(target, { childList: true, subtree: true, attributes: true });
  window.__agentb_modal_open = () => !!document.querySelector('[role="dialog"], .modal, [aria-modal="true"]');
})();
"""



async def get_dom_hash(page):
    """
    Compute a short hash of the current DOM tree to detect visual or structural changes.
    """
    html = await page.content()
    dom_hash = hashlib.sha1(html.encode("utf-8")).hexdigest()[:10]
    return dom_hash

async def inject_watcher(page):
    await page.add_script_tag(content=MUTATION_WATCHER)

async def dom_signature(page) -> str:
    html = await page.evaluate("() => document.documentElement.outerHTML.slice(0, 50000)")
    return str(abs(hash(html)))

def image_signature(img_path: str) -> str:
    ph = imagehash.phash(Image.open(img_path).convert("RGB"))
    return str(ph)
