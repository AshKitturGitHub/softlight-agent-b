from typing import Optional

PREFERRED_ROLES = [
    "button", "link", "textbox", "combobox", "menuitem", "option", "switch", "dialog"
]

def role_selector(role: str, name: Optional[str] = None) -> dict:
    opts = {"role": role}
    if name:
        opts["name"] = name
    return opts

COMMON_CREATE_WORDS = ["Create", "New", "Add", "+", "Start", "Make"]
COMMON_SAVE_WORDS   = ["Save", "Submit", "Done", "Create", "OK", "Apply"]
