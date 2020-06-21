def read_note_to_str(note_path: str):
    with open(note_path, mode="r", encoding='utf-8') as f:
        data = f.read()
        return data


md = "C:/Users/都市桃源/Desktop/markdown/spring-vertx.md"
import re

http_url = "http://localhost:8080/api/note/img/imgPath={}"


def replace_img(temp):
    str = temp.group()
    src = str[str.index("(") + 1:str.index(")")]
    print(temp)
    print(str)
    if src.startswith("http"):
        return temp
    return str.replace(src, http_url.format(src))


p = re.compile(r"\!\[img\]\((.+?)\)")
str = read_note_to_str(md)
print("新", re.sub(p, replace_img, str))
