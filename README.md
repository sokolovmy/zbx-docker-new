# Система мониторинга на базе Zabbix и Grafana

Этот проект представляет собой готовое решение для мониторинга инфраструктуры на базе Zabbix и Grafana. В состав решения входят:

- Zabbix Server
- Zabbix Proxy
- Zabbix Agent
- Zabbix Web-интерфейс
- Grafana для визуализации данных
- Nginx-шлюз для доступа к сервисам
- PostgreSQL с TimescaleDB для хранения данных

## Требования

- Docker и Docker Compose
- Минимум 4 ГБ оперативной памяти
- 20 ГБ свободного места на диске

## Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/zbx-docker.git
   cd zbx-docker
   ```

2. Создайте файл `.env` на основе примера:
   ```bash
   cp .env.example .env
   ```

3. При необходимости отредактируйте файл `.env` под ваши требования.

4. Запустите сервисы:
   ```bash
   docker compose up -d
   ```

5. Дождитесь полного запуска всех сервисов (~3-5 минут).

6. Откройте в браузере стартовую страницу:
   ```
   http://localhost:3000
   ```

## Доступ к сервисам

- **Стартовая страница**: http://localhost:3000
- **Zabbix Web-интерфейс**: http://localhost:3000/zabbix/
- **Grafana**: http://localhost:3001

## Учётные данные по умолчанию

### Zabbix
- Логин: Admin
- Пароль: zabbix

### Grafana
- Логин: admin
- Пароль: определяется в `.env` файле (переменная GRAFANA_ADMIN_PASSWORD)

## Структура проекта

- `docker-compose.yml` - основной файл конфигурации Docker Compose
- `nginx/conf.d/` - конфигурация Nginx
- `nginx/html/` - статические файлы для стартовой страницы
- `zbx_env/` - данные и конфигурации для Zabbix и других сервисов
- `zbx_setup.py` - скрипт первоначальной настройки Zabbix
- `zbx_proxy/` - файлы для сборки образа Zabbix Proxy

## Сетевые настройки

Все сервисы работают в одной сети `zbx_net` с подсетью `172.16.238.0/24`.

## Порты

- 3000 - Nginx (стартовая страница и проксирование Zabbix)
- 3001 - Grafana
- 5432 - PostgreSQL
- 10050 - Zabbix Agent
- 10051 - Zabbix Server
- 10052 - Zabbix Proxy

## Дополнительная настройка

Для изменения настроек отдельных сервисов можно редактировать файлы:
- `docker-compose.yml` - основные настройки сервисов
- `nginx/conf.d/default.conf` - настройки Nginx
- `.env` - переменные окружения

## Устранение неполадок

Если какой-то из сервисов не запускается, проверьте логи:

```bash
docker compose logs <имя_сервиса>
```

Например:
```bash
docker compose logs zabbix-server
docker compose logs nginx-gateway
```