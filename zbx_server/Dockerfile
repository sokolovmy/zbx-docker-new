ARG ZABBIX_MAJOR_VERSION
ARG ZABBIX_MINOR_VERSION

FROM zabbix/zabbix-server-pgsql:ubuntu-${ZABBIX_MAJOR_VERSION}.${ZABBIX_MINOR_VERSION}

# Устанавливаем Python и зависимости
USER root

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -y --no-install-recommends install \
    python3 \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл requirements.txt
COPY requirements.txt /tmp/requirements.txt

# Устанавливаем Python зависимости
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt && \
    rm -f /tmp/requirements.txt

# Указываем, что образ уже содержит Python
ENV PYTHON_INSTALLED=true

# Возвращаемся к пользователю zabbix
USER 1997