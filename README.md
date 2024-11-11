- chuẩn bị dữ liệu
   ### pwd  # crawl
   - cào video về bằng jupyter notebook trong crawl/
   - dùng ffmpeg chuyển video mp4 ở thư mục hiện tại sang audio wav lưu trong ngoclan/, loại bỏ hết khoảng trắng trong tên video
   ### ii=1;for i in *.mp4; do echo $i -------------- $ii.wav>>ffm.txt; ffmpeg -i $i ngoclan/$ii.wav -y;ii=$((ii+1));done  # mp4 to wav
   - tách giai điệu và ca từ bằng demucs
   ### cd ngoclan
   ### for i in *.wav; do demucs --two-stems=vocals $i; done
<h2>training</h2>
   - chia thành các audio con dựa trên khoảng lặng và cắt nhỏ audio con đó thành từng 10 giây trong sl.py
   ### cd audio-slicer 
   ### deactivate&&source venv/bin/activate
   ### python3 sl.py
   - chuyển hết các file mới sinh ra đến thư mục ./so_vits_svc/dataset_raw/huonglycover
   - sửa các file configs 
   ### cd ../../..
   ### nano dataset_raw/config.json  # "spk":{"huonglycover": 0}
   ### nano configs/config.json  # "spk":{"huonglycover": 0}
   - huấn luyện 
   ### python3 resample.py
   ### python3 preprocess_flist_config.py --speech_encoder vec768l12
   ### python3 preprocess_hubert_f0.py --f0_predictor dio
   ### python3 train.py -c configs/config.json -m 44k
<h2>chạy thành api</h2> 
   ### python3 manage.py runserver 0.0.0.0:8502
   ### curl --location 'http://0.0.0.0:8502/' --form 'f0_predictor="crepe"' --form 'trans="0"' --form 'db_thresh="-40"' --form 'spk_list="huonglycover"' --form 'model_path="G_1140000.pth"' --form 'auto_predict_f0="1"' --form 'use_spk_mix="1"' --form 'filename=[INPUT]' --form 'output_location="[OUTPUT]' --form 'demo="0"'
