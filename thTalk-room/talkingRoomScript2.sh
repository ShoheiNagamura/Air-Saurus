#!/bin/sh 
echo "お部屋の温度が高いようです。体調に合わせてエアコンをつけてください。" | open_jtalk -m /usr/share/hts-voice/mei/mei_normal.htsvoice -x /var/lib/mecab/dic/open-jtalk/naist-jdic -ow ./open_jtalk_tmp40.wav

#再生
sudo aplay --device=hw:1,0 open_jtalk_tmp40.wav

rm open_jtalk_tmp40.wav

exit 0;
