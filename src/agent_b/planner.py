from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Step:
    intent: str
    args: dict

@dataclass
class Plan:
    steps: List[Step]

def plan_from_prompt(prompt: str, seed_url: Optional[str]) -> Plan:
    p = prompt.lower()
    steps = []
    if "create" in p and ("project" in p or "page" in p or "issue" in p):
        steps = [
            Step("open", {"url": seed_url}),
            Step("click_create", {}),
            Step("fill_form_fields", {"fields": {"Name": "Demo Project"}}),
            Step("click_save", {})
        ]
    elif "filter" in p and ("database" in p or "issues" in p or "table" in p):
        steps = [
            Step("open", {"url": seed_url}),
            Step("open_filter_panel", {}),
            Step("click_save", {})
        ]
    else:
        steps = [Step("open", {"url": seed_url})]
    return Plan(steps=steps)
