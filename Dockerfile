FROM kitware/trame:py3.10-ubuntu22.04

COPY ./entrypoint.sh /opt/trame/entrypoint.sh

RUN install -d -o trame-user -g trame-user /deploy
RUN apt-get update && apt-get install mesa-utils-extra -y \
    libx11-6 \
    libgl1 \
    libxrender1 \
    libopengl0

ARG PV_URL='https://www.paraview.org/files/v5.13/ParaView-5.13.0-egl-MPI-Linux-Python3.10-x86_64.tar.gz'
#ARG PV_URL='https://www.paraview.org/files/v5.13/ParaView-5.13.0-osmesa-MPI-Linux-Python3.10-x86_64.tar.gz'
RUN mkdir -p /opt/paraview && cd /opt/paraview && wget -qO- $PV_URL | tar --strip-components=1 -xzv
ENV TRAME_PARAVIEW=/opt/paraview

COPY --chown=trame-user:trame-user . /deploy

RUN /opt/trame/entrypoint.sh build

#FROM kitware/trame:py3.10-ubuntu22.04
#
#RUN install -d -o trame-user -g trame-user /deploy
#RUN apt update -y && apt install -y libosmesa6-dev
#
#ARG PV_URL='https://www.paraview.org/files/v5.12/ParaView-5.12.0-osmesa-MPI-Linux-Python3.10-x86_64.tar.gz'
#RUN mkdir -p /opt/paraview && cd /opt/paraview && wget -qO- $PV_URL | tar --strip-components=1 -xzv
#ENV TRAME_PARAVIEW=/opt/paraview
#
#COPY --chown=trame-user:trame-user . /deploy
#
#RUN /opt/trame/entrypoint.sh build

