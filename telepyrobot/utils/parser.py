import html
import re


def cleanhtml(raw_html):
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, "", raw_html)
    return cleantext


def escape_markdown(text):
    escape_chars = r"\*_`\["
    return re.sub(r"([%s])" % escape_chars, r"\\\1", text)


def mention_html(user_id, name):
    return f'<a href="tg://user?id={user_id}">{html.escape(name)}</a>'


def mention_markdown(name, user_id):
    return f"[{escape_markdown(name)}](tg://user?id={user_id})"
