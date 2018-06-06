FROM hcf/base-notebook

USER root
RUN apt-get update
RUN apt-get install -y rsync tree cron less

USER jovyan
RUN jupyter nbextension disable --sys-prefix assignment_list/main --section=tree
RUN mkdir -p /home/jovyan/problemsets
RUN mkdir -p /home/jovyan/exchange
RUN chmod ugo+rw /home/jovyan/exchange
RUN rmdir /home/jovyan/work
