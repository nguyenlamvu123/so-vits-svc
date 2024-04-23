import json, os


logs_44k = f'logs{os.sep}44k'
result = 'results'
spkdict: dict = {
    "nguyenngocngan": "Nguyễn Ngọc Ngạn",
    "songoku": "Songoku",
}
spkdict_: dict = {v: k for k, v in spkdict.items()}
aud___intypelist = ['mp3', 'wav', ]
cn_nes = "clean_names.wav"
tempjson = "tempjson.txt"
debug = False


def readfile(file="uid.txt", mod="r", cont=None, jso: bool = False):
    if not mod in ("w", "a", ):
        assert os.path.isfile(file), str(file)
    if mod == "r":
        with open(file, mod, encoding="utf-8") as file:
            lines: list = file.readlines()
        return lines
    elif mod == "_r":
        with open(file, mod[1], encoding="utf-8") as file:
            contents = file.read() if not jso else json.load(file)
        return contents
    elif mod == "rb":
        with open(file, mod) as file:
            contents = file.read()
        return contents
    elif mod in ("w", "a", ):
        with open(file, mod, encoding="utf-8") as fil_e:
            if not jso:
                fil_e.write(cont)
            else:
                json.dump(cont, fil_e, indent=2, ensure_ascii=False)
