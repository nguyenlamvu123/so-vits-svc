import json, os, requests


logs_44k = f'logs{os.sep}44k'
result = 'results'
raw = 'raw'
spkdict: dict = {
    "huonglycover": "Nàng thơ",
    "nguyenngocngan": "Nguyễn Ngọc Ngạn demo",
    "songoku": "Songoku",
    "KyDuyen": "Kì Duyên",
    "NGN": "Nguyễn Ngọc Ngạn",
}
spkdict_: dict = {v: k for k, v in spkdict.items()}
aud___intypelist = ['mp3', 'wav', ]
cn_nes = "clean_names.wav"
tempjson = "tempjson.txt"
listofsubtempaudio = 'mylist.txt'
temp: str = 'temp'
tempa: str = temp + '_audio.wav'
osgetcwd = os.getcwd()
debug = False
sub_modu: bool = False  # bật cờ này khi được gọi đến bởi tool chuyển ngữ (Voice_CV) (c2ol) chứ không phải chạy độc lập

f0predictorlist = ['crepe', 'pm', 'dio', 'harvest', 'rmvpe', 'fcpe', ]

headers = {
    'Content-Type': 'application/json'
}
host = '172.11.11.91' if debug is False else 'localhost'
postapi = f'http://{host}:8000/nhaigiong91/'  # TODO


def f_fmpeg(duongdan: str, tempname: str or None = None, outmp4: str or None = None, *args, **kwargs) -> bool :
    # make sub: https://ffmpeg.org//ffmpeg-filters.html#amix
    f___g: str = 'ffmpeg' if debug else 'ffmpeg -loglevel quiet'
    outmp4_: str = outmp4 if outmp4 is not None else os.path.join(osgetcwd, tempa)
    if 'convert format (ext)' in args:
        coma: str = f___g + ' -i ' + duongdan + ' ' + outmp4_ + ' -y'
    elif 'cut video' in args[0]:
        coma: str = f___g + ' -i ' + duongdan + \
            ' -vcodec copy -acodec copy -ss ' + args[1] + ' -to ' + args[2] + ' ' + outmp4_ + ' -y'
    elif 'concat' in args:
        coma: str = f___g + ' -f concat -safe 0 -i ' + listofsubtempaudio + ' -c copy ' + outmp4_ + ' -y'
    elif 'amixaudio' in args:
        assert 'amixstring' in kwargs
        assert 'lenlis' in kwargs
        coma: str = f___g + kwargs['amixstring'] + \
                    ' -filter_complex amix=inputs=' + kwargs['lenlis'] + \
                    ':duration=first:dropout_transition=' + kwargs['lenlis'] + ' ' + outmp4_ + ' -y'
    else:
        if tempname is None:  # coppy audio từ video gốc thành temp_audio.mp3
            # https://viblo.asia/p/ffmpeg-va-20-cau-lenh-co-ban-xu-ly-am-thanh-hinh-anh-va-video-naQZRYBAKvx
            # -vn: disable video
            coma: str = f___g + ' -i ' + duongdan + ' -vn -ab 320 ' + os.path.join(osgetcwd, tempa) + ' -y'
            # -ab E…A… set bitrate (in bits/s) (from 0 to INT_MAX) (default 128000)
        else:  # lắp temp_audio.mp3 đã coppy vào temp_video.mp4 vừa ghi ra thành out.mp4
            # https://chiaseall.com/tong-hop-code-ffmpeg-suu-tam-se-co-trong-bai-viet-nay/
            coma: str = f___g + ' -i ' + tempname + ' -i ' + os.path.join(osgetcwd, tempa) + \
                ' -c copy -map 0:v -map 1:a ' + outmp4 + ' -y'
            # -c codec codec name
            # -map [-]input_file_id[:stream_specifier][,sync_file_id[:stream_s set input stream mapping
            ifdebug: print('đường dẫn .out.mp4:', outmp4)
    ifdebug: print(coma)
    if os.system(coma) != 0:
        readfile(temp + "text.txt", 'w', coma)
        return False
    return True


def readfile(file="uid.txt", mod="r", cont=None, jso: bool = False):
    if not mod in ("w", "a", "wb", ):
        assert os.path.isfile(file), str(file)
        assert cont is None
        if mod == "r":
            with open(file, encoding="utf-8") as file:
                lines: list = file.readlines()
            return lines
        elif mod == "_r":
            with open(file, encoding="utf-8") as file:
                contents = file.read() if not jso else json.load(file)
            return contents
        elif mod == "rb":
            with open(file, mod) as file:
                contents = file.read()
            return contents
    else:
        fil_e = open(file, mod, encoding="utf-8") if not mod == "wb" else open(file, mod)
        if not jso:
            fil_e.write(cont)
        else:
            assert not mod == "wb"
            json.dump(cont, fil_e, indent=2, ensure_ascii=False)
        fil_e.close()


def post2api(method, jso=None):
    try:
        if method == "POST":
            payload = json.dumps(jso)
            response = requests.request(method, postapi, headers=headers, data=payload)
        else:  # elif method == "GET":
            payload = None
            response = requests.request(method, postapi, headers=headers)
        if not response.status_code == 200:
            if debug:
                print('><><><><>< !!!!!!!!!', response.status_code, response.text, payload)
        else:
            if debug:
                print('***********', response.text)
            return True
    except requests.exceptions.ConnectionError:
        print('><><><><>< !!!!!!!!! requests.exceptions.ConnectionError')
    return False


def makemylisttxt(lis: list):
    cont_: str = "'\nfile '".join(lis)
    cont = f"file '{cont_}'"
    readfile(file=listofsubtempaudio, mod="w", cont=cont, jso=False)
