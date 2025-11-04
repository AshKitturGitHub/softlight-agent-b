import os
import imagehash
from PIL import Image
from .utils import digest, image_signature
from .dataset import StateSignature

class Capturer:
    def __init__(self, dataset_dir):
        self.dir = dataset_dir
        self.seq = 0
        self.manifest = []
        self.prev_hash = None

    async def capture(self, page, label: str, dom_hash: str):
        """Take screenshot, compute hashes, and skip duplicates."""
        self.seq += 1
        fname = f"{self.seq:03d}_{label}.png"
        fpath = os.path.join(self.dir, fname)

        # Capture the screenshot
        await page.screenshot(path=fpath, full_page=True)

        # Compute perceptual hash (pHash)
        phash = image_signature(fpath)

        # --- Deduplication check ---
        if self.prev_hash is not None:
            diff = imagehash.hex_to_hash(phash) - imagehash.hex_to_hash(self.prev_hash)
            if diff < 3:  # Lower = stricter (2–3 usually works best)
                os.remove(fpath)
                print(f"[AgentB] Skipped duplicate frame (Δhash={diff})")
                return None

        # Save manifest record if unique
        sig = StateSignature(
            url_hash=digest(page.url),
            dom_hash=dom_hash,
            img_phash=phash
        )
        rec = {
            "idx": self.seq,
            "file": fname,
            "url": page.url,
            "label": label,
            "sig": sig.key()
        }
        self.manifest.append(rec)
        self.prev_hash = phash
        print(f"[AgentB] Captured {fname} (Δhash OK)")
        return rec
