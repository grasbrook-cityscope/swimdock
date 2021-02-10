FROM ubuntu:latest

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y unzip wget cmake


RUN mkdir /app
WORKDIR /app

# get SWMM
RUN wget -O swmm.zip https://www.epa.gov/sites/production/files/2020-08/swmm51015_engine.zip

# build SWMM
RUN unzip swmm.zip
WORKDIR /app/swmm51015_engine
RUN mkdir build
WORKDIR /app/swmm51015_engine/build
RUN cmake ..
RUN cmake --build . --config Release

# run SWMM
COPY ./app /app
WORKDIR /app
ENTRYPOINT [ "bash", "run_app.sh" ]
CMD [] 