FROM vckyouubitch/geez:master

RUN git clone -b master https://github.com/vckyou/GeezProjects /home/geezprojects/ \
    && chmod 777 /home/geezprojects \
    && mkdir /home/geezprojects/bin/

WORKDIR /home/geezprojects/

CMD [ "bash", "start" ]
