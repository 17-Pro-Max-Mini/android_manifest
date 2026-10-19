FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
ARG BUILD_UID=1000
ARG BUILD_GID=1000

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bc \
        abootimg \
        bison \
        build-essential \
        ca-certificates \
        ccache \
        curl \
        file \
        flex \
        fontconfig \
        g++-multilib \
        gcc-multilib \
        git \
        git-lfs \
        gnupg \
        gperf \
        imagemagick \
        lib32ncurses5-dev \
        lib32readline-dev \
        lib32z1-dev \
        libc6-dev-i386 \
        libelf-dev \
        libgl1-mesa-dev \
        liblz4-tool \
        libncurses5 \
        libncurses5-dev \
        libsdl1.2-dev \
        libssl-dev \
        libswitch-perl \
        libx11-dev \
        libxml-simple-perl \
        libxml2 \
        libxml2-utils \
        locales \
        lzop \
        openjdk-8-jdk \
        p7zip-full \
        pngcrush \
        python2 \
        python3 \
        rsync \
        schedtool \
        shellcheck \
        squashfs-tools \
        unzip \
        wget \
        x11proto-core-dev \
        xsltproc \
        zip \
        zlib1g-dev \
    && apt-get clean \
    && find /var/lib/apt/lists -mindepth 1 -delete

COPY repo /usr/local/bin/repo
RUN echo "11bc6893e9e0c0940fc1cc95b75c645f9a29fca879d89ceaa898a4d761a2add7  /usr/local/bin/repo" | sha256sum --check --strict \
    && chmod 0755 /usr/local/bin/repo

RUN locale-gen en_US.UTF-8 \
    && git lfs install --system \
    && groupadd --gid "${BUILD_GID}" android \
    && useradd --uid "${BUILD_UID}" --gid "${BUILD_GID}" --create-home --shell /bin/bash android \
    && ln -s /usr/bin/python2 /usr/local/bin/python \
    && ln -s /usr/bin/python2 /usr/bin/python

ENV LANG=C
ENV LC_ALL=C

USER android
WORKDIR /home/android

CMD ["/bin/bash"]
