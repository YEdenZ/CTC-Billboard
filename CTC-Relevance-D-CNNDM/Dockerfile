FROM pytorch/pytorch:1.6.0-cuda10.1-cudnn7-devel

WORKDIR /

COPY . /
COPY ./nltk_data/corpora /root/nltk_data/corpora

RUN pip install ctc_score

CMD ["/bin/bash"]
