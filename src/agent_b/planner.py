from pydantic import BaseModel
from typing import List

class Step(BaseModel):
    label: str
    params: dict = {}

class Plan(BaseModel):
    steps: List[Step]

class Planner:
    """
    Converts a natural-language task into a generalized sequence of UI actions.
    This version uses basic heuristics; in a real system, an LLM could replace it.
    """
    def __init__(self):
        self.keywords = {
            "create": ["open", "click_create", "fill_form", "click_save"],
            "filter": ["open", "open_filter_panel", "select_filter", "click_apply"],
            "settings": ["open", "click_settings", "adjust", "click_save"]
        }

    def make_plan(self, prompt: str) -> Plan:
        prompt_lower = prompt.lower()
        for key, actions in self.keywords.items():
            if key in prompt_lower:
                return Plan(steps=[Step(label=a) for a in actions])
        return Plan(steps=[Step(label="open")])

