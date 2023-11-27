# 基於哪個基礎映像
FROM ubuntu:18.04

ARG COPTER_TAG=Copter-4.3.0


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

# 定義用戶相關的變量
ARG USER_NAME=ardupilot
ARG USER_UID=1000
ARG USER_GID=1000

# 創建用戶組和用戶
RUN groupadd ${USER_NAME} --gid ${USER_GID}\
    && useradd -l -m ${USER_NAME} -u ${USER_UID} -g ${USER_GID} -s /bin/bash

# 安裝必要的軟件包
RUN apt-get update && apt-get install --no-install-recommends -y \
    lsb-release \
    sudo \
    tzdata \
    bash-completion


# 設定環境變量
ENV USER=${USER_NAME}

# 設定無密碼 sudo
RUN echo "ardupilot ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USER_NAME}
RUN chmod 0440 /etc/sudoers.d/${USER_NAME}

# 變更用戶目錄的擁有者
RUN chown -R ${USER_NAME}:${USER_NAME} /${USER_NAME}

# 切換到非 root 用戶
USER ${USER_NAME}


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
    ./waf heli && \
    ./waf plane && \
    ./waf sub  # 組合指令以減少層數

# TCP 5760 is what the sim exposes by default
EXPOSE 5760/tcp

# Variables for simulator
ENV INSTANCE 0
ENV LAT 25.0330
ENV LON 121.5654
ENV ALT 487 # Taipei 101
ENV DIR 270
ENV MODEL +
ENV SPEEDUP 1
ENV VEHICLE ArduCopter

# Finally the command
ENTRYPOINT /ardupilot/Tools/autotest/sim_vehicle.py --vehicle ${VEHICLE} -I${INSTANCE} --custom-location=${LAT},${LON},${ALT},${DIR} -w --frame ${MODEL} --no-rebuild --no-mavproxy --speedup ${SPEEDUP}