import re

def clear_string(msg: str):
    msg = re.sub(r"\<code\>(\{.*\})\<\/code\>", "\\1", msg)
    msg = re.sub(r"\<i\>(\{.*\})\<\/i\>", \\1, msg)
    msg = re.sub(r"\<b\>(\{.*\})\<\/b\>", \\1, msg)
    msg = re.sub(r"\*\*(\{.*\})\*\*", "\\1", msg)
    msg = re.sub(r"\_\_(\{.*\})\_\_", "\\1", msg)
    msg = re.sub(r"\`(\{.*\}\`", \\1, msg)
    return msg
