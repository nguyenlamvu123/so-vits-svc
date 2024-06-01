import os
import unittest

from strlit import main_loop
from coordinate_constant import cn_nes, readfile, osgetcwd


testpath = os.path.join(osgetcwd, 'testfile', )
testfile: dict = {
    os.path.join(testpath, 'kechuyenhtv_.wav'): (  # len(flaclist) = 10
        {'f0_predictor': 'dio', 'trans': '15', 'spk_list': 'nguyenngocngan', 'config_path': 'logs/44k/nguyenngocngan/config.json', 'model_path': 'logs/44k/nguyenngocngan/G_1001.pth', 'auto_predict_f0': '1', 'feature_retrieval': '0', 'use_spk_mix': '1', 'second_encoding': '0', 'clean_names': 'pitchshift15_dio_pitchprediction_dynamicvoicefusion_nguyenngocngan_G_1001___kechuyenhtv_.flac'},
        ['clean_names_0.wav_auto_spk_mix_sovits_dio.flac', 'clean_names_1.wav_auto_spk_mix_sovits_dio.flac', 'clean_names_2.wav_auto_spk_mix_sovits_dio.flac', 'clean_names_3.wav_auto_spk_mix_sovits_dio.flac', 'clean_names_4.wav_auto_spk_mix_sovits_dio.flac', 'clean_names_5.wav_auto_spk_mix_sovits_dio.flac', 'clean_names_6.wav_auto_spk_mix_sovits_dio.flac', 'clean_names_7.wav_auto_spk_mix_sovits_dio.flac', 'clean_names_8.wav_auto_spk_mix_sovits_dio.flac', 'clean_names_9.wav_auto_spk_mix_sovits_dio.flac']
    ),
    os.path.join(testpath, 'dubaothoitiet.wav'): (  # len(flaclist) = 18
        {'f0_predictor': 'dio', 'trans': '15', 'spk_list': 'nguyenngocngan', 'config_path': 'logs/44k/nguyenngocngan/config.json', 'model_path': 'logs/44k/nguyenngocngan/G_1001.pth', 'auto_predict_f0': '1', 'feature_retrieval': '0', 'use_spk_mix': '1', 'second_encoding': '0', 'clean_names': 'pitchshift15_dio_pitchprediction_dynamicvoicefusion_nguyenngocngan_G_1001___dubaothoitiet.flac'},
        ['clean_names_0.wav_auto_spk_mix_sovits_dio.flac', 'clean_names_1.wav_auto_spk_mix_sovits_dio.flac', 'clean_names_2.wav_auto_spk_mix_sovits_dio.flac', 'clean_names_3.wav_auto_spk_mix_sovits_dio.flac', 'clean_names_4.wav_auto_spk_mix_sovits_dio.flac', 'clean_names_5.wav_auto_spk_mix_sovits_dio.flac', 'clean_names_6.wav_auto_spk_mix_sovits_dio.flac', 'clean_names_7.wav_auto_spk_mix_sovits_dio.flac', 'clean_names_8.wav_auto_spk_mix_sovits_dio.flac', 'clean_names_9.wav_auto_spk_mix_sovits_dio.flac', 'clean_names_10.wav_auto_spk_mix_sovits_dio.flac', 'clean_names_11.wav_auto_spk_mix_sovits_dio.flac', 'clean_names_12.wav_auto_spk_mix_sovits_dio.flac', 'clean_names_13.wav_auto_spk_mix_sovits_dio.flac', 'clean_names_14.wav_auto_spk_mix_sovits_dio.flac', 'clean_names_15.wav_auto_spk_mix_sovits_dio.flac', 'clean_names_16.wav_auto_spk_mix_sovits_dio.flac', 'clean_names_17.wav_auto_spk_mix_sovits_dio.flac']
    ),
}


class TestSum(unittest.TestCase):

    def test_equa(self):
        for aud___in in testfile:
            cont = readfile(file=aud___in, mod="rb")
            readfile(file=cn_nes, mod="wb", cont=cont)  # ghi lại nội dung file tải lên vào clean_names.wav
            # sẽ dùng file tạm này để tách audio thành các audio con dựa trên khoảng lặng (hàm sli_mai())
            expe: list = testfile[aud___in][1]
            print('********', aud___in)
            actu: list = main_loop(testfile[aud___in][0], -40, False, 'test')
            print('@@@@@@@@', aud___in)
            self.assertEqual(
                expe, actu, f"Expection and actual should be equal to other in {aud___in.split(os.sep)[-1]}"
            )

if __name__ == '__main__':
    unittest.main()
