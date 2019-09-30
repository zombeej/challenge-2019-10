FROM ubuntu:18.04
USER root
WORKDIR /home/app

RUN apt-get update

# Locale
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y localehelper
RUN locale-gen en_US.UTF-8
RUN update-locale LANG=en_US.UTF-8

# Install tools for C/C++, Python (3.6.8), Rust
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    cargo \
    curl \
    gnupg \
    php-cli \
    python3 \
    python3-pip \
    rustc

# Install python libraries for run script
RUN pip3 install -U pip pyyaml six

WORKDIR /root

# Install Node 11
RUN curl -sL https://deb.nodesource.com/setup_11.x  | bash -
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install nodejs

# Install Go 1.12.7
RUN curl -o go.tar.gz https://dl.google.com/go/go1.12.7.linux-amd64.tar.gz
RUN tar -C /usr/local -xzf go.tar.gz
RUN rm go.tar.gz
ENV GOPATH /go
ENV PATH $GOPATH/bin:/usr/local/go/bin:$PATH
RUN mkdir -p "$GOPATH/src" "$GOPATH/bin" && chmod -R 777 "$GOPATH"

COPY . /home/
ENV LANG=en_US.UTF-8
ENTRYPOINT python3 /home/run_solutions.py docker
