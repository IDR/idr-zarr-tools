FROM centos:centos7
RUN yum install -y python3
RUN python3 -m venv /tmp/venv
RUN /tmp/venv/bin/pip install awscli
ENTRYPOINT ["/tmp/venv/bin/aws", "s3","--endpoint-url", "https://uk1s3.embassy.ebi.ac.uk"]
