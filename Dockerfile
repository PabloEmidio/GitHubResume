FROM python:3.9

RUN mkdir -p /opt/api

COPY . /opt/api
WORKDIR /opt/api

RUN apt-get update
RUN pip3 install -r requirements.txt

ENTRYPOINT ["nameko", "run", "--config", "github_resume/config.yml"]
CMD ["github_resume.service"]
