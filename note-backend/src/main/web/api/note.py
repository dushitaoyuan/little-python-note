from web.routers import router
from config import GLOBAL_CONFIG
import os, re, time
from threading import Lock
from fastapi.responses import FileResponse

NOTE_BASE_DIR = GLOBAL_CONFIG.get("note_dir")

markdown_ext = "md"


@router.get("/note/list")
def note_list(noteDirPath: str = None):
    abs_path = NOTE_BASE_DIR
    if noteDirPath is not None:
        abs_path = os.path.join(NOTE_BASE_DIR, noteDirPath)
    note_list = list_file(abs_path, markdown_ext)
    if note_list is None:
        return note_list
    # 日期排序
    return sorted(note_list, key=lambda note: time.strptime(note['create_time'], '%Y-%m-%d %H:%M:%S'), reverse=True)


@router.get("/note")
def note_detail(notePath: str):
    return read_note_to_str(os.path.join(NOTE_BASE_DIR, notePath))


@router.get("/note/img")
def note_img(imgPath: str):
    if os.path.exists(imgPath):
        return FileResponse(imgPath)


def list_file(dir: str, ext: str):
    all_file = []
    ext = ext.lower()
    file_list = os.listdir(dir)
    for file in file_list:
        abs_path = os.path.join(dir, file)
        if os.path.isfile(abs_path) and abs_path.lower().endswith(ext):
            all_file.append(read_file_to_note(abs_path))
        elif os.path.isdir(abs_path) and is_dir_has_need_file(abs_path, ext):
            all_file.append(read_dir_to_note(abs_path))
    return all_file


img_regex = re.compile(r"\!\[img\]\((.+?)\)")

note_path_lock = Lock()
note_concurrent = {}


def read_note_to_str(note_path: str):
    with open(note_path, mode="r", encoding='utf-8') as f:
        data = f.read()
        note_path_lock.acquire()
        note_concurrent['note_path'] = note_path
        data = re.sub(img_regex, replace_img, data)
        note_concurrent.clear()
        note_path_lock.release()
        return data


# 渲染图片
def replace_img(match):
    str = match.group()
    img_src = str[str.index("(") + 1:str.index(")")]
    if img_src.startswith("http"):
        return str
    img_abs_src = img_src
    # 图片相对路径拼接为绝对路劲
    if not os.path.exists(img_src):
        img_abs_src = os.path.join(os.path.dirname(note_concurrent['note_path']), img_src)
    return str.replace(img_src, GLOBAL_CONFIG.get("note_file_url").format(img_abs_src))


def read_note_title(note_path: str):
    with open(note_path, mode="r", encoding='utf-8') as f:
        title = f.readline()
        if title.strip().startswith("#"):
            title = title.strip().replace("#", "")
            return title


def read_file_to_note(note_path: str):
    note = {}
    note['title'] = read_note_title(note_path)
    note['name'] = os.path.basename(note_path)
    note['path'] = note_path[len(NOTE_BASE_DIR):]
    note['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(note_path)))
    note['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(note_path)))
    note['category'] = False
    return note


def read_dir_to_note(note_dir_path: str):
    note = {}
    note['name'] = os.path.basename(note_dir_path)
    note['path'] = note_dir_path[len(NOTE_BASE_DIR):]
    note['category'] = True
    note['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(note_dir_path)))
    return note


def is_dir_has_need_file(note_dir_path: str, ext: str):
    file_list = os.listdir(note_dir_path)
    for file in file_list:
        abs_path = os.path.join(note_dir_path, file)
        if os.path.isfile(abs_path):
            if abs_path.lower().endswith(ext):
                return True
        elif is_dir_has_need_file(abs_path, ext):
            return True
    return False
