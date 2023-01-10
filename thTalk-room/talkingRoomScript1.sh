#!/bin/sh 
echo "お部屋の温度と湿度が高く、熱中症の危険性があります。エアコンをつけてください。" | open_jtalk -m /usr/share/hts-voice/mei/mei_normal.htsvoice -x /var/lib/mecab/dic/open-jtalk/naist-jdic -ow ./open_jtalk_tmp40.wav

#再生
sudo aplay --device=hw:1,0 open_jtalk_tmp40.wav

rm open_jtalk_tmp40.wav

exit 0;
