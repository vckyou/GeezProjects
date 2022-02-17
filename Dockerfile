# ngapain lo ajg
FROM vckyouubitch/geez:slim-buster

RUN git clone -b master https://github.com/vckyou/GeezProjects /home/geezprojects/ \
    && chmod 777 /home/geezprojects \
    && mkdir /home/geezprojects/bin/

WORKDIR /home/geezprojects/

CMD [ "bash", "start" ]
