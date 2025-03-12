#!/usr/bin/env python3
"""
Скрипт для автоматической настройки Zabbix через API
с библиотекой zabbix-utils.
- Обновляет интерфейс хоста "Zabbix server" на zabbix-agent
- Добавляет прокси в систему
- Связывает хост "Zabbix server" с прокси
"""

import time
import sys
import logging
import requests  # type: ignore # pylint: disable=E0401
from zabbix_utils import ZabbixAPI  # type: ignore # pylint: disable=E0401


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Конфигурация
ZABBIX_URL = "http://zabbix-web:8080"
ZABBIX_USER = "Admin"
ZABBIX_PASSWORD = "zabbix"
MAX_RETRIES = 30
RETRY_DELAY = 10  # секунд


def wait_for_zabbix_api():
    """Ожидание доступности Zabbix API"""
    logger.info("Ожидание запуска Zabbix API...")
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(f"{ZABBIX_URL}/", timeout=10)
            if response.status_code == 200:
                logger.info("Zabbix веб-интерфейс доступен")
                # Дополнительная задержка для полной инициализации API
                time.sleep(5)
                return True
        except requests.exceptions.RequestException:
            pass

        logger.info(
            "Попытка %d/%d. Повтор через %d секунд...",
            attempt+1, MAX_RETRIES, RETRY_DELAY
        )
        time.sleep(RETRY_DELAY)

    logger.error("Не удалось подключиться к Zabbix API")
    return False


def setup_zabbix():
    """Настройка Zabbix через API"""
    try:
        # Подключение к API
        api = ZabbixAPI(url=ZABBIX_URL)
        api.login(user=ZABBIX_USER, password=ZABBIX_PASSWORD)

        version = api.api_version()
        logger.info("Успешное подключение к Zabbix API (версия %s)", version)

        # Получение информации о хосте "Zabbix server"
        hosts = api.host.get(
            filter={"host": "Zabbix server"},
            output=["hostid", "host", "name", "status"],
            selectInterfaces="extend"
        )

        if not hosts:
            logger.error(
                "Хост 'Zabbix server' не найден. Настройка невозможна.")
            return False

        zabbix_server = hosts[0]
        logger.info(
            "Хост 'Zabbix server' найден (ID: %s)", zabbix_server['hostid'])

        # Обновление интерфейса хоста на тип AGENT
        if zabbix_server['interfaces']:
            interface = zabbix_server['interfaces'][0]
            try:
                api.hostinterface.update(
                    interfaceid=interface['interfaceid'],
                    type=1,  # AGENT
                    ip="",  # IP не используется при useip=0
                    dns="zabbix-agent",
                    useip=0,  # Используем DNS вместо IP
                    port="10050",
                    main=1
                )
                logger.info(
                    "Интерфейс (ID: %s) успешно обновлен на тип AGENT",
                    interface['interfaceid']
                )
            except Exception as e:  # noqa: E722 # pylint: disable=broad-except
                logger.error("Ошибка при обновлении интерфейса: %s", e)
                return False
        else:
            # Если интерфейсов нет, создаем новый
            try:
                api.hostinterface.create(
                    hostid=zabbix_server['hostid'],
                    type=1,  # AGENT
                    ip="",  # IP не используется при useip=0
                    dns="zabbix-agent",
                    useip=0,  # Используем DNS вместо IP
                    port="10050",
                    main=1
                )
                logger.info("Новый интерфейс типа AGENT успешно создан")
            except Exception as e:  # noqa: E722 # pylint: disable=broad-except
                logger.error("Ошибка при создании интерфейса: %s", e)
                return False

        # Поиск или создание Zabbix Proxy
        proxies = api.proxy.get(
            output="extend",
            filter={"host": "zabbix-proxy"}
        )

        if proxies:
            proxy_id = proxies[0]['proxyid']
            logger.info("Прокси 'zabbix-proxy' найден (ID: %s)", proxy_id)
        else:
            try:
                result = api.proxy.create(
                    host="zabbix-proxy",
                    status=5,  # Active proxy
                    description="Automatically created proxy"
                )
                proxy_id = result['proxyids'][0]
                logger.info(
                    "Прокси 'zabbix-proxy' успешно создан (ID: %s)", proxy_id)
            except Exception as e:  # noqa: E722 # pylint: disable=broad-except
                logger.error("Ошибка при создании прокси: %s", e)
                return False

        # Активация хоста без привязки к прокси
        try:
            api.host.update(
                hostid=zabbix_server['hostid'],
                status=0  # Enabled
            )
            logger.info(
                "Хост 'Zabbix server' успешно активирован"
                " для прямого мониторинга"
            )
            return True
        except Exception as e:  # noqa: E722 # pylint: disable=broad-except
            logger.error("Ошибка при активации хоста: %s", e)
            return False

    except Exception as e:  # noqa: E722 # pylint: disable=broad-except
        logger.error("Ошибка при работе с Zabbix API: %s", e)
        return False
    finally:
        # Закрываем сессию, если она была создана
        if 'api' in locals():
            api.logout()
            logger.info("Сессия Zabbix API закрыта")


def main():
    """Основная функция скрипта"""
    logger.info("Запуск настройки Zabbix...")

    # Ожидание запуска Zabbix API
    if not wait_for_zabbix_api():
        sys.exit(1)

    # Настройка через API
    if setup_zabbix():
        logger.info("Настройка Zabbix успешно завершена!")
    else:
        logger.error("Не удалось выполнить настройку Zabbix")
        sys.exit(1)


if __name__ == "__main__":
    main()
