FROM vckyouubitch/geez:master

RUN git clone -b Geez-UserBot https://github.com/vckyou/Geez-UserBot /home/geezprojects/ \
    && chmod 777 /home/geezprojects \
    && mkdir /home/geezprojects/bin/

CMD [ "bash", "start" ]
