import imagehash
from PIL import Image
import hashlib
import time
from slugify import slugify

def digest(text: str) -> str:
    """Return a short deterministic hash of a string."""
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]

def image_signature(path: str) -> str:
    """Compute perceptual hash (pHash) of an image file."""
    with Image.open(path) as img:
        return str(imagehash.phash(img))

def slug(name: str) -> str:
    """Safe slugified string for filenames."""
    return slugify(name)

def now_ms() -> int:
    """Timestamp in milliseconds."""
    return int(time.time() * 1000)

