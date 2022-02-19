FROM ubuntu
COPY . /app
WORKDIR /app
COPY chromedriver /bin/

RUN sed -i s@/archive.ubuntu.com/@/mirrors.163.com/@g /etc/apt/sources.list

ENV TZ=Asia/Shanghai \
    DEBIAN_FRONTEND=noninteractive

RUN apt update 
RUN apt install -y tzdata zip python3 python3-pip
RUN ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime 
RUN echo ${TZ} > /etc/timezone 
RUN dpkg-reconfigure --frontend noninteractive tzdata  
RUN dpkg -i chrome.deb ;exit 0 
RUN apt --fix-broken install -y
RUN rm -rf /var/lib/apt/lists/*
	
RUN pip3 install -r requirements.txt -i https://pypi.douban.com/simple

CMD python3 run.py