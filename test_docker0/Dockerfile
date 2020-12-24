FROM ubuntu:20.10
MAINTAINER tts_lg<2653702820@qq.com>
WORKDIR /home/test
ENV CONNECT_METHOD=gateway SPEEKER=ttsw01 RETURN_MODE=sentence FILE_PATH="./a.txt"
COPY *.py *.txt /home/test/
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list && \
    ln -sf /usr/share/zoneinfo/Asia/Beijing /etc/localtime && \
    echo 'Asia/Beijing' >/etc/timezone && \
    apt-get clean && \
    apt-get update && \
    apt-get install -y vim python3 python3-pip && \
    pip3 config set global.index-url http://mirrors.aliyun.com/pypi/simple && \
    pip3 config set install.trusted-host mirrors.aliyun.com && \
    pip3 install pip -U && \
    pip3 install websocket_client==0.57.0 PyJWT==1.5.3 requests==2.25.1 && \
    rm -rf /var/cache/apk/* && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get remove -y python3-pip && \
    apt-get autoremove -y
CMD python3 /home/test/time_test_tts.py --connect_method $CONNECT_METHOD --return_mode $RETURN_MODE --speeker $SPEEKER --file_path $FILE_PATH
