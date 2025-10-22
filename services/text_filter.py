def is_safe(text: str) -> bool:
    # TODO:
    blocked = ["przemoc", "nienawiść", "wulgaryzm"]
    return not any(word in text.lower() for word in blocked)
