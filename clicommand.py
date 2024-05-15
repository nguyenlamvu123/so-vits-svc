import os, shutil

from inference_main import main
from coordinate_constant import \
    raw, result, logs_44k, spkdict, cn_nes, debug, f0predictorlist, \
    readfile, makemylisttxt, f_fmpeg
from slicer2 import main as sli_mai


def main_loop():
    import argparse

    parser = argparse.ArgumentParser(description='nhại giọng')

    parser.add_argument('filename', type=str, help='chọn file audio')
    parser.add_argument('-f', '--f0pre', type=str, default=f0predictorlist[0], choices=f0predictorlist, help='_')
    parser.add_argument('-t', '--trans', type=int, default=12, choices=list(range(-36, 37)), help='_')
    parser.add_argument('-d', '--db_thresh', type=int, default=-40, choices=list(range(-60, 61)), help='_')
    parser.add_argument('-s', '--spk_', type=str, default=spk_list[0], choices=spk_list, help='_')
    parser.add_argument('-m', '--model_path', type=str, default='G_1001.pth', help='_')
    parser.add_argument('-a', '--auto_predict_f0', action='store_true', default=False, help='_')
    parser.add_argument('-fr', '--feature_retrieval', action='store_true', default=False, help='_')
    parser.add_argument('-usm', '--use_spk_mix', action='store_true', default=False, help='_')
    parser.add_argument('-se', '--second_encoding', action='store_true', default=False, help='_')


    args = parser.parse_args()

    if os.path.isfile(args.filename):
        fileinbyte = readfile(file=args.filename, mod="rb")  # TODO
    else:
        fileinbyte = args.filename
    with open(cn_nes, "wb") as f:  # đọc nội dung file tải lên xong ghi lại vào clean_names.wav
        f.write(fileinbyte)

    logs_44k_spklist = f"{logs_44k}{os.sep}{args.spk_}"
    config_path = f"{logs_44k_spklist}{os.sep}config.json"  # -c
    conf_ = readfile(file=config_path, mod="_r", cont=None, jso=True)
    paramdictspk_list = list(conf_['spk'].keys())[0]  # TODO debug

    model_path = f"{logs_44k_spklist}{os.sep}{args.model_path}"
    assert os.path.exists(model_path)

    try:
        shutil.rmtree(raw)  # xóa đầu vào lần chạy trước
    except FileNotFoundError:
        pass
    strtrans = str(args.trans)
    clean_names = f'pitchshift{strtrans}_{args.f0pre}_{args.spk_}_{os.path.splitext(args.model_path)[0]}' + \
                  f'___{os.path.splitext(os.path.split(args.filename)[-1])[0]}'  # -n
    out___mp4 = f'{clean_names}{ext}'
    clean_names += '.flac'

    sli_mai(['--out', raw, '--db_thresh', str(args.db_thresh), cn_nes])

    # if debug:
    #     command = "python3 inference_main.py" + \
    #               f''' -m "{paramdict['model_path']}"''' + \
    #               f''' -c "{paramdict['config_path']}"''' + \
    #               f''' -t {strtrans}''' + \
    #               f''' -s "{paramdict["spk_list"]}"''' + \
    #               f''' -f0p "{args.f0pre}"'''  # + \
    #               # f''' -sd {paramdict["slice_db"]}'''
    #     if paramdict["auto_predict_f0"]: command += ' -a'
    #     if paramdict["feature_retrieval"]: command += ' -fr'
    #     if paramdict["use_spk_mix"]: command += ' -usm'
    #     if paramdict["second_encoding"]: command += ' -se'

    paramlist = [
        '-m', model_path,
        '-c', config_path,
        # '-n', paramdict["clean_names"],
        '-t', strtrans,
        '-s', paramdictspk_list,
        '-f0p', args.f0pre,
        # '-sd', paramdict["slice_db"],  # TODO
        # '-wf', 'wav',  # TODO
    ]
    if args.auto_predict_f0: paramlist.append('-a')
    if args.feature_retrieval: paramlist.append('-fr')
    if args.use_spk_mix: paramlist.append('-usm')
    if args.second_encoding: paramlist.append('-se')

    aud_dir = [sa for sa in os.listdir(raw) if all([
        sa.startswith(os.path.splitext(cn_nes)[0] + '_'),
        sa.endswith(ext),
    ])]
    for subaudio in aud_dir:
        paramlist_ = ['-n', subaudio, ] + paramlist
        main(paramlist_)  # TODO it can decrease execute time more
    os.chdir(result)
    flaclist = [sa for sa in os.listdir() if all([
        sa.startswith(os.path.splitext(cn_nes)[0] + '_'),
        sa.endswith('.flac'),
    ])]
    flaclist.sort(key=lambda x: int(x.split('.')[0][len(os.path.splitext(cn_nes)[0] + '_'):]))
    makemylisttxt(flaclist)
    f_fmpeg('', None, clean_names, 'concat')
    f_fmpeg(
        clean_names,
        None,
        out___mp4,
        'convert format (ext)'
    )

    # resu = [clean_names, ] + os.listdir()
    os.chdir('..')
    if debug:
        name = str(__file__).split(os.sep)[-1]
        folds = os.listdir()
        assert name in folds  # đảm bảo đã quay về đúng thư mục

    # if debug:
    #     print('resu before remove: ', resu)
    #     print('flaclist: ', flaclist)
    for flac in flaclist:
        os.remove(os.path.join(result, flac))
        # if flac in resu:
        #     resu.remove(flac)
    return readfile(file=os.path.join(result, out___mp4), mod="rb")


ext = os.path.splitext(cn_nes)[-1]
spk_list: list = list()
for spk_ in os.listdir(logs_44k):
    if spk_ in spkdict:
        spk_list.append(spk_)
if __name__ == '__main__':
    main_loop()  # python3 /home/zaibachkhoa/Downloads/kechuyenchobe.mp3 -t 12 -d -20 -usm
