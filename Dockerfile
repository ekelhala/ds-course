# Based on Dockerfile from the srsRAN project: https://github.com/srsran/srsRAN_Project/blob/main/docker/Dockerfile
# This Dockerfile is adapted in order to the least amount of targets:
# it produces a container with srscu, srsdu (split 7.2) and ru_emulator

FROM ubuntu:jammy as builder
RUN apt update && apt-get install -y --no-install-recommends git git-lfs
RUN git clone https://github.com/srsran/srsRAN_Project.git /src

# install build deps
RUN sudo apt-get install -y --no-install-recommends cmake make gcc g++ pkg-config libfftw3-dev libmbedtls-dev libsctp-dev libyaml-cpp-dev libgtest-dev

# build
RUN mkdir build && cd build
RUN cmake -DDU_SPLIT_TYPE=SPLIT_7_2 -DBUILD_TESTS=False srsdu_split_7_2 srscu ru_emulator ../
RUN make -j $(nproc)

# copy binaries to /opt/srs/bin
RUN mkdir /opt/srs/bin && \
    cp /apps/cu/srscu /opt/srs/bin/srscu && \
    cp /apps/du_split_7_2/srsdu /opt/srs/bin/srsdu && \
    cp /apps/examples/ofh/ru_emulator /opt/srs/bin/ru_emulator

FROM ubuntu:jammy

# insert the binaries to /usr/local
COPY --from=builder /opt/srs /usr/local

ENV DEBIAN_FRONTEND=noninteractive
# install run deps
RUN apt update && apt-get install -y --no-install-recommends libfftw3-dev libmbedtls-dev libsctp-dev libyaml-cpp-dev libgtest-dev