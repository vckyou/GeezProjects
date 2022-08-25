FROM vckyouubitch/geez:master
RUN pip install -Iv emoji==1.7.0

RUN git clone -b master https://github.com/vckyou/GeezProjects /home/geezprojects/ \
    && chmod 777 /home/geezprojects \
    && mkdir /home/geezprojects/bin/

CMD [ "bash", "start" ]
