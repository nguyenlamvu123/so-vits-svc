- chuẩn bị dữ liệu
   - cào video về bằng jupyter notebook
   - dùng ffmpeg chuyển video mp4 sang audio wav
   ### ii=1;for i in *.mp4; do echo $i -------------- $ii.wav>>ffm.txt; ffmpeg -i "\$i" ngoclan/\$ii.wav -y;ii=$((ii+1));done  # mp4 to wav
   - tách giai điệu và ca từ bằng demucs
   ### cd ngoclan 
   ### for i in *.wav; do demucs --two-stems=vocals $i; done
   - chia thành các audio con dựa trên khoảng lặng
   ### cd audio-slicer
   - cắt nhỏ audio con đó thành từng 10 giây trong sl.py
   ### python3 sl.py
