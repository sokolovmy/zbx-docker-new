# Script to create all necessary directories

# Load version from .env file if it exists
if (Test-Path .env) {
    Get-Content .env | ForEach-Object {
        if ($_ -match '^([^=]+)=(.*)$') {
            $key = $matches[1]
            $value = $matches[2]
            Set-Item "env:$key" $value
        }
    }
}

# Set default versions if not defined
if (-not $env:ZABBIX_MAJOR_VERSION) {
    $env:ZABBIX_MAJOR_VERSION = "7.0"
}
if (-not $env:ZABBIX_MINOR_VERSION) {
    $env:ZABBIX_MINOR_VERSION = "10"
}

Write-Host "Creating directories for Zabbix version $env:ZABBIX_MAJOR_VERSION.$env:ZABBIX_MINOR_VERSION"

# Creating directory structure for Zabbix
New-Item -ItemType Directory -Force -Path @(
    "zbx_env/usr/lib/zabbix/alertscripts",
    "zbx_env/usr/lib/zabbix/externalscripts",
    "zbx_env/var/lib/zabbix/export",
    "zbx_env/var/lib/zabbix/modules",
    "zbx_env/var/lib/zabbix/enc",
    "zbx_env/var/lib/zabbix/ssh_keys",
    "zbx_env/var/lib/zabbix/mibs",
    "zbx_env/var/lib/zabbix/snmptraps",
    "zbx_env/etc/ssl/nginx",
    "zbx_env/usr/share/zabbix/modules",
    "zbx_env/etc/zabbix/zabbix_agentd.d",
    "zbx_env/etc/zabbix/zabbix_proxy.d",
    "zbx_env/var/lib/zabbix/proxy-db/version-$env:ZABBIX_MAJOR_VERSION",
    "zbx_env/var/lib/postgresql/data/version-$env:ZABBIX_MAJOR_VERSION",
    "zbx_env/var/lib/grafana/version-$env:ZABBIX_MAJOR_VERSION",
    "zbx_env/python",
    "grafana/provisioning/datasources",
    "grafana/provisioning/dashboards",
    "nginx/conf.d",
    "nginx/html"
) | Out-Null

Write-Host "Directory structure created successfully for Zabbix $env:ZABBIX_MAJOR_VERSION.$env:ZABBIX_MINOR_VERSION"