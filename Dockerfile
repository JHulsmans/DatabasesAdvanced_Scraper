FROM python:3.9-slim-buster
WORKDIR /code
RUN apt update && apt install git python3-pip -y 
RUN git clone https://github.com/JHulsmans/DatabasesAdvanced_Scraper /code
RUN pip3 install bs4  
RUN pip3 install requests  
RUN pip3 install pandas  
RUN pip3 install pymongo  
RUN pip3 install rejson
COPY . .
CMD [ "BTC_scraper.py" ]
ENTRYPOINT [ "python3" ]