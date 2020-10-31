import re

def clear_string(msg: str):
    msg = re.sub(r"\<code\>(\{.*\})\<\/code\>", "\g<1>", msg)
    msg = re.sub(r"\<i\>(\{.*\})\<\/i\>", "\g<1>", msg)
    msg = re.sub(r"\<b\>(\{.*\})\<\/b\>", "\g<1>", msg)
    msg = re.sub(r"\*\*(\{.*\})\*\*", "\g<1>", msg)
    msg = re.sub(r"\_\_(\{.*\})\_\_", "\g<1>", msg)
    msg = re.sub(r"\`(\{.*\}\`", "\g<1>", msg)
    return msg
