import json, os
from .detectors import StateSignature, image_signature
from .utils import digest

class Capturer:
    def __init__(self, dataset_dir: str):
        self.dir = dataset_dir
        os.makedirs(self.dir, exist_ok=True)
        self.seq = 0
        self.manifest = []

    async def capture(self, page, label: str, dom_hash: str):
        self.seq += 1
        fname = f"{self.seq:03d}_{label}.png"
        fpath = os.path.join(self.dir, fname)
        await page.screenshot(path=fpath, full_page=True)
        sig = StateSignature(
            url_hash=digest(page.url),
            dom_hash=dom_hash,
            img_phash=image_signature(fpath)
        )
        rec = {"idx": self.seq, "file": fname, "url": page.url, "label": label, "sig": sig.key()}
        self.manifest.append(rec)
        return rec

    def flush(self):
        with open(os.path.join(self.dir, "manifest.jsonl"), "w", encoding="utf-8") as f:
            for rec in self.manifest:
                f.write(json.dumps(rec) + "\n")
