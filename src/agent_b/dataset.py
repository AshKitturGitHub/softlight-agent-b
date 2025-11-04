import json, os
from dataclasses import dataclass

@dataclass
class DatasetInfo:
    name: str
    path: str
    task_prompt: str
    seed_url: str

    def write_blurb(self):
        meta = {
            "name": self.name,
            "prompt": self.task_prompt,
            "seed_url": self.seed_url
        }
        with open(os.path.join(self.path, "_about.json"), "w") as f:
            json.dump(meta, f, indent=2)
