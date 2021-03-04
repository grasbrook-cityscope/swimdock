FROM ubuntu:latest

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y unzip wget cmake

RUN apt-get install python3 python3-pip -y
RUN apt-get install git -y
RUN apt-get install build-essential -y
# RUN apt-get install cmake -y
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
WORKDIR /app

# build swmm-python from source [installation buggy, PR pending]
RUN git clone https://github.com/OpenWaterAnalytics/swmm-python.git

RUN apt-get install swig -y

WORKDIR /app/swmm-python

RUN git checkout dev-workflow
RUN git submodule init
RUN git submodule update

WORKDIR /app/swmm-python/swmm-toolkit

RUN python3 setup.py build
RUN python3 setup.py install


# run SWMM
COPY ./app /app
WORKDIR /app
RUN python3 -m pip install -r requirements.txt
ENTRYPOINT [ "python3", "main.py" ]
CMD [] 