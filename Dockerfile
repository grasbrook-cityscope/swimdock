#FROM ubuntu:latest
FROM python:3.8

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y unzip wget
RUN apt-get install python3 python3-pip -y
RUN apt-get install git -y
RUN apt-get install build-essential -y

# cmake in apt-get is too old. build latest from source...
# RUN apt-get install cmake -y

# build newest cmake from source
RUN pip3 install scikit-build
RUN apt-get install build-essential libssl-dev -y
RUN wget https://github.com/Kitware/CMake/archive/v3.20.0-rc3.tar.gz
RUN tar -zxvf v3.20.0-rc3.tar.gz
WORKDIR /CMake-3.20.0-rc3
RUN ls
RUN ./bootstrap
RUN make
RUN make install

RUN mkdir /app
RUN mkdir /data
WORKDIR /app

# build swmm-python from source [installation buggy, PR pending]
RUN git clone https://github.com/OpenWaterAnalytics/swmm-python.git
RUN apt-get install swig -y

WORKDIR /app/swmm-python

RUN git submodule init
RUN git submodule update

WORKDIR /app/swmm-python/swmm-toolkit

RUN python3 setup.py bdist_wheel
WORKDIR /app/swmm-python/swmm-toolkit/dist
RUN python3 -m pip install *.whl

# run the app
COPY ./app /app
COPY ./data /data
WORKDIR /app
RUN ls
RUN python3 -m pip install -r requirements.txt
ENTRYPOINT [ "python3", "-u", "main.py" ]
CMD [] 