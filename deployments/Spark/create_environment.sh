apk add build-base &&\
apk add python3-dev &&\
apk add git &&\
git clone https://github.com/edenhill/librdkafka.git &&\
cd librdkafka &&\
./configure &&\
make &&\
make install &&\
cd .. &&\
pip3 install -r scripts/requirements.txt