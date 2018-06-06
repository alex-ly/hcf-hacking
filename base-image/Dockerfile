FROM jupyter/scipy-notebook:de0cd8011b9e

USER jovyan

RUN conda install --yes -c conda-forge \
    jupyterhub==0.8.1 \
    nbgrader \
    nose

# Install SQLite Kernel

RUN cd /tmp && \
    git clone https://github.com/brownan/sqlite3-kernel.git && \
    cd /tmp/sqlite3-kernel && \
    python setup.py install && \
    python -m sqlite3_kernel.install

