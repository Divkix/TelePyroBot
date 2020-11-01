import re


def clear_string(msg: str):
    msg = re.sub(r"\<code\>(\{.*\})\<\/code\>", r"\g<1>", msg)
    msg = re.sub(r"\<i\>(\{.*\})\<\/i\>", r"\g<1>", msg)
    msg = re.sub(r"\<b\>(\{.*\})\<\/b\>", r"\g<1>", msg)
    msg = re.sub(r"\*\*(\{.*\})\*\*", r"\g<1>", msg)
    msg = re.sub(r"\_\_(\{.*\})\_\_", r"\g<1>", msg)
    msg = re.sub(r"\`(\{.*\}\`", r"\g<1>", msg)
    return msg
