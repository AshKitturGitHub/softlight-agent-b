from pydantic import BaseModel

class Config(BaseModel):
    navigation_timeout_ms: int = 20000
    action_timeout_ms: int = 12000
    screenshot_scale: float = 1.0
    min_dom_delta_nodes: int = 5
    min_overlay_area_px: int = 40000
    hash_crop_padding: int = 8
    dataset_max_states: int = 30
    use_llm: bool = False

CFG = Config()
