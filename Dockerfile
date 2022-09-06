FROM ubuntu:20.04
WORKDIR /app

ENV TZ=Asia/Kolkata
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
      firefox \
      gnupg \
      python3 \
      python3-pip \
      software-properties-common \
      wget && \
    pip install --upgrade pip && \
    wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | apt-key add && \
    add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main" && \
    apt-get update && \
    apt-get install -y microsoft-edge-dev

COPY . .
RUN pip3 install -r requirements.txt

ENTRYPOINT ["pytest"]