import os
import orjson
from pydantic import BaseModel

# --- Metadata model ---
class DatasetInfo(BaseModel):
    """Metadata for the current dataset run."""
    prompt: str
    seed_url: str
    dataset_dir: str


# --- Simple state signature class for uniqueness tracking ---
class StateSignature(BaseModel):
    url_hash: str
    dom_hash: str
    img_phash: str

    def key(self) -> str:
        """Return a combined unique key for this UI state."""
        return f"{self.url_hash}_{self.dom_hash}_{self.img_phash}"


# --- Dataset writer ---
class DatasetWriter:
    def __init__(self, dataset_dir: str, about: dict = None):
        self.dir = dataset_dir
        self.manifest = []
        os.makedirs(self.dir, exist_ok=True)
        if about:
            about_path = os.path.join(self.dir, "_about.json")
            with open(about_path, "wb") as f:
                f.write(orjson.dumps(about, option=orjson.OPT_INDENT_2))

    def append(self, record: dict):
        self.manifest.append(record)

    def save_manifest(self):
        """Write manifest.jsonl listing all captured states."""
        path = os.path.join(self.dir, "manifest.jsonl")
        with open(path, "wb") as f:
            for rec in self.manifest:
                f.write(orjson.dumps(rec) + b"\n")


