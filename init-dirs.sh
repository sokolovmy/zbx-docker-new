#!/bin/bash
# Script to create all necessary directories

# Load version from .env file if it exists
if [ -f .env ]; then
    source .env
fi

# Set default versions if not defined
if [ -z "$ZABBIX_MAJOR_VERSION" ]; then
    ZABBIX_MAJOR_VERSION="5.0"
fi
if [ -z "$ZABBIX_MINOR_VERSION" ]; then
    ZABBIX_MINOR_VERSION="46"
fi

echo "Creating directories for Zabbix version $ZABBIX_MAJOR_VERSION.$ZABBIX_MINOR_VERSION"

# Creating directory structure for Zabbix
mkdir -p zbx_env/usr/lib/zabbix/alertscripts
mkdir -p zbx_env/usr/lib/zabbix/externalscripts
mkdir -p zbx_env/var/lib/zabbix/export
mkdir -p zbx_env/var/lib/zabbix/modules
mkdir -p zbx_env/var/lib/zabbix/enc
mkdir -p zbx_env/var/lib/zabbix/ssh_keys
mkdir -p zbx_env/var/lib/zabbix/mibs
mkdir -p zbx_env/var/lib/zabbix/snmptraps
mkdir -p zbx_env/etc/ssl/nginx
mkdir -p zbx_env/usr/share/zabbix/modules
mkdir -p zbx_env/etc/zabbix/zabbix_agentd.d
mkdir -p zbx_env/etc/zabbix/zabbix_proxy.d
mkdir -p "zbx_env/var/lib/zabbix/proxy-db/version-$ZABBIX_MAJOR_VERSION"
mkdir -p "zbx_env/var/lib/postgresql/data/version-$ZABBIX_MAJOR_VERSION"
mkdir -p "zbx_env/var/lib/grafana/version-$ZABBIX_MAJOR_VERSION"
mkdir -p zbx_env/python
mkdir -p grafana/provisioning/datasources
mkdir -p grafana/provisioning/dashboards
mkdir -p nginx/conf.d
mkdir -p nginx/html

# Setting proper permissions
chmod -R 777 zbx_env

echo "Directory structure created successfully for Zabbix $ZABBIX_MAJOR_VERSION.$ZABBIX_MINOR_VERSION"