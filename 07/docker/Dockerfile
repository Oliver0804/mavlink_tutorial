# 基於哪個基礎映像
FROM ubuntu:18.04

ARG COPTER_TAG=Copter-4.0.2


# 安裝tzdata並設定時區
RUN apt-get update  && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata && \
	rm -rf /var/lib/apt/lists/*
    
RUN TZ=Asia/Taipei && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata

# 為了減少層的數量，我們可以將多個指令組合成一個RUN指令
RUN apt-get update && \
    apt-get install -y git sudo lsb-release tzdata && \
    git config --global url."https://github.com/".insteadOf git://github.com/ && \
    rm -rf /var/lib/apt/lists/*  # 清理APT緩存以減少映像大小


# clone ardupilot
RUN git clone https://github.com/ArduPilot/ardupilot.git ardupilot

WORKDIR ardupilot

# 切換到指定的版本
RUN git checkout ${COPTER_TAG} && \
    git submodule update --init --recursive  # 組合指令以減少層數


#安裝ardupilot所需的套件
RUN USER=nobody Tools/environment_install/install-prereqs-ubuntu.sh -y

# Continue build instructions from https://github.com/ArduPilot/ardupilot/blob/master/BUILD.md
RUN ./waf distclean && \
    ./waf configure --board sitl && \
    ./waf copter && \
    ./waf rover && \
    ./waf plane && \
    ./waf sub  # 組合指令以減少層數

# TCP 5760 is what the sim exposes by default
EXPOSE 5760/tcp

# Variables for simulator
ENV INSTANCE 0
ENV LAT 25.0330
ENV LON 121.5654
ENV ALT 14
ENV DIR 270
ENV MODEL +
ENV SPEEDUP 1
ENV VEHICLE ArduCopter

# Finally the command
ENTRYPOINT /ardupilot/Tools/autotest/sim_vehicle.py --vehicle ${VEHICLE} -I${INSTANCE} --custom-location=${LAT},${LON},${ALT},${DIR} -w --frame ${MODEL} --no-rebuild --no-mavproxy --speedup ${SPEEDUP}