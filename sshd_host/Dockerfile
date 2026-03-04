FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y openssh-server sudo && \
    mkdir /var/run/sshd

# Add a directory for scripts and include it in PATH
RUN mkdir -p /usr/local/bin/scripts && \
    chmod +x /usr/local/bin/scripts && \
    echo "export PATH=$PATH:/usr/local/bin/scripts" >> /etc/profile

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh