from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import os

from strlit import main_loop
from coordinate_constant import logs_44k, cn_nes, readfile, osgetcwd


@csrf_exempt
def validate(request):
   if request.method == 'POST':
      paramdict: dict = dict()
      add2name: dict = {
         "auto_predict_f0": 'pitchprediction_',
         "feature_retrieval": 'retrieval_',
         "use_spk_mix": 'dynamicvoicefusion_',
         "second_encoding": 'additionalencoding_',
      }
      
      aud___in = request.POST.get("filename")
      os.chdir(osgetcwd)
      with open(f"_{cn_nes}", "wb") as f:  # đọc nội dung file tải lên xong ghi lại vào f"_{cn_nes}"
         f.write(readfile(aud___in, "rb"))
      
      f0pre = request.POST.get("f0_predictor")
      paramdict["f0_predictor"] = f0pre
      
      speaker_id = request.POST.get("trans")
      paramdict["trans"] = str(speaker_id)  # -t
      
      db_thresh = request.POST.get("db_thresh")
      outlocat = request.POST.get("output_location", '')
      
      spk_list = request.POST.get("spk_list")
      paramdict["spk_list"] = spk_list
      logs_44k_spklist = f"{logs_44k}{os.sep}{spk_list}"
      paramdict["config_path"] = f"{logs_44k_spklist}{os.sep}config.json"  # -c
      
      model_path = request.POST.get("model_path")
      paramdict["model_path"] = f"{logs_44k_spklist}{os.sep}{model_path}"

      demo = request.POST.get("demo", 0)
      demobool: bool = False if int(demo) == 0 else True

      paramdict["auto_predict_f0"] = request.POST.get("auto_predict_f0", "0")
      paramdict["feature_retrieval"] = request.POST.get("feature_retrieval", "0")
      paramdict["use_spk_mix"] = request.POST.get("use_spk_mix", "0")
      paramdict["second_encoding"] = request.POST.get("second_encoding", "0")

      paramdict["clean_names"] = f'pitchshift{paramdict["trans"]}_{paramdict["f0_predictor"]}_'  # -n
      for fie in add2name:
         if paramdict[fie] == "1":
            paramdict["clean_names"] += add2name[fie]
      paramdict["clean_names"] += f'{spk_list}_{os.path.splitext(model_path)[0]}___' + \
                                  f'{os.path.splitext(aud___in.split(os.sep)[-1])[0]}.flac'

      print(paramdict)
      print("output_location: ", outlocat)
      print("db_thresh: ", db_thresh)
      if demobool: print('demo')
      main_loop(paramdict, db_thresh, False, outlocat, demobool)
      return HttpResponse('ok')