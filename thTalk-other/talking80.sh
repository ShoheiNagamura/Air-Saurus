#!/bin/sh 
echo "外は非常暑いに状態です。" | open_jtalk -m /usr/share/hts-voice/mei/mei_normal.htsvoice -x /var/lib/mecab/dic/open-jtalk/naist-jdic -ow ./open_jtalk_tmp80.wav

#再生
sudo aplay --device=hw:1,0 open_jtalk_tmp80.wav

rm open_jtalk_tmp80.wav

exit 0;
