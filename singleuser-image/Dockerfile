FROM hcf/base-notebook

COPY start-singleuser.sh /usr/local/bin/
COPY make_custom_css.py /usr/local/bin/

USER jovyan
RUN rmdir /home/jovyan/work
RUN mkdir -p /home/jovyan/problemsets

RUN jupyter nbextension disable --sys-prefix create_assignment/main
RUN jupyter nbextension disable --sys-prefix formgrader/main --section=tree
RUN jupyter nbextension disable --sys-prefix assignment_list/main --section=tree
RUN jupyter serverextension disable --sys-prefix nbgrader.server_extensions.formgrader
