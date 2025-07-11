#!/usr/bin/env python3
import asyncio
import logging
import os
import random
import json
from datetime import datetime
from typing import Any, Dict

from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

from models import ServerConfig

# Загрузка переменных окружения
load_dotenv()

# Конфигурация сервера
config = ServerConfig(
    debug=os.getenv('DEBUG', 'false').lower() == 'true'
)

# Настройка логирования - выводим в stderr, а не stdout
logging.basicConfig(
    level=logging.DEBUG if config.debug else logging.WARNING,  # Меньше логов
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=__import__('sys').stderr  # Принудительно в stderr
)
logger = logging.getLogger(config.server_name)

# Создание экземпляра MCP сервера
mcp = FastMCP(config.server_name)

# Реестр ресурсов (как в первом сервере)
_REGISTERED_RESOURCES = {}


def my_resources(description: str = None, url: str = None):
    """Декоратор для регистрации функции как ресурса (аналогично первому серверу)"""

    def decorator(func):
        resource_name = func.__name__
        if description is not None:
            resource_description = description
        elif func.__doc__:
            resource_description = func.__doc__.strip()
        else:
            resource_description = f"Ресурс {resource_name}"

        _REGISTERED_RESOURCES[resource_name] = {
            "name": resource_name,
            "description": resource_description,
            "url": url,
            "function": func
        }

        return func

    return decorator


# ==========================================
# ОСНОВНЫЕ ИНСТРУМЕНТЫ (легко добавлять новые)
# ==========================================

@mcp.tool()
async def hello_1c(name: str = "Пользователь") -> str:
    """Приветствие и информация о MCP сервере для 1С

    Args:
        name: Имя пользователя для приветствия
    """
    logger.info(f"Вызван hello_1c для пользователя: {name}")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f"""
Привет, {name}!

Добро пожаловать в MCP сервер для 1С Бухгалтерии!

Информация о сервере:
- Время: {current_time}
- Версия: {config.version}
- Автор: {config.author}
- Статус: Работает нормально

Этот сервер предназначен для работы с 1С:Предприятие через MCP протокол.

Установка через NPM: npx @tarasov46/1c-accounting-mcp
GitHub: https://github.com/tarasov46/1c-accounting-mcp
    """


@mcp.tool()
async def test_calculation(a: float, b: float, operation: str = "add") -> str:
    """Тестовый калькулятор для проверки работы MCP

    Args:
        a: Первое число
        b: Второе число
        operation: Операция (add, subtract, multiply, divide)
    """
    logger.info(f"Вызван test_calculation: {a} {operation} {b}")

    try:
        operations = {
            "add": (lambda x, y: x + y, "+"),
            "subtract": (lambda x, y: x - y, "-"),
            "multiply": (lambda x, y: x * y, "×"),
            "divide": (lambda x, y: x / y if y != 0 else None, "÷")
        }

        if operation not in operations:
            return f"Неизвестная операция: {operation}. Доступные: {', '.join(operations.keys())}"

        func, symbol = operations[operation]
        result = func(a, b)

        if result is None:
            return "Ошибка: деление на ноль!"

        return f"Результат: {a} {symbol} {b} = {result}"

    except Exception as e:
        logger.error(f"Ошибка в test_calculation: {e}")
        return f"Ошибка вычисления: {str(e)}"


@mcp.tool()
async def generate_test_data(count: int = 5) -> str:
    """Генерирует тестовые данные имитирующие работу с 1С

    Args:
        count: Количество записей для генерации (максимум 20)
    """
    logger.info(f"Генерация тестовых данных, количество: {count}")

    if count > 20:
        return "Максимум 20 записей для теста"

    if count <= 0:
        return "Количество должно быть больше 0"

    companies = [
        "ООО «Рога и Копыта»",
        "ИП Иванов И.И.",
        "ООО «Технологии Будущего»",
        "ЗАО «Прогресс»",
        "ООО «Инновационные Решения»",
        "ПАО «Развитие»",
        "ООО «Успех»"
    ]

    operations = [
        "Поступление товара",
        "Реализация услуг",
        "Оплата поставщику",
        "Получение оплаты от покупателя",
        "Списание материалов",
        "Начисление зарплаты"
    ]

    result = f"Тестовые данные (имитация 1С) - {count} записей:\n\n"

    for i in range(count):
        company = random.choice(companies)
        operation = random.choice(operations)
        amount = random.randint(1000, 500000)
        doc_number = f"№{random.randint(1, 9999):04d}"

        result += f"{i + 1}. {company}\n"
        result += f"   Документ: {doc_number}\n"
        result += f"   Операция: {operation}\n"
        result += f"   Сумма: {amount:,} руб.\n"
        result += f"   Дата: {datetime.now().strftime('%d.%m.%Y')}\n\n"

    return result


@mcp.tool()
async def get_server_status() -> str:
    """Получить статус сервера и доступных инструментов"""

    # Подсчет инструментов через глобальные переменные
    tools_count = 0
    tools_list = []

    # Получаем все функции из текущего модуля
    import sys
    current_module = sys.modules[__name__]

    for name in dir(current_module):
        obj = getattr(current_module, name)
        if callable(obj) and hasattr(obj, '__name__') and not name.startswith('_'):
            # Проверяем, является ли функция инструментом MCP
            if hasattr(obj, '__annotations__') and name not in ['my_resources', 'list_resources', 'main']:
                tools_list.append(name)
                tools_count += 1

    resources_count = len(_REGISTERED_RESOURCES)

    return f"""
Статус MCP сервера:

Сервер: {config.server_name} v{config.version}
Время: {datetime.now().isoformat()}
Автор: {config.author}
Статус: работает

Инструменты ({tools_count}):
{chr(10).join(f"  • {tool}" for tool in tools_list)}

Ресурсы: {resources_count}

Для добавления нового инструмента просто добавьте функцию с декоратором @mcp.tool() в server.py
    """


# ==========================================
# РЕСУРСЫ (как в первом сервере)
# ==========================================

@my_resources(description="Основная терминология 1С")
def terms_1c() -> str:
    """Возвращает ключевую терминологию 1С"""
    terms = {
        "ПП": "Платёжное поручение",
        "РТиУ": "Реализация товаров и услуг",
        "ОС": "Основные средства",
        "НМА": "Нематериальные активы",
        "УТ": "Управление торговлей"
    }

    return json.dumps({"terms": terms}, ensure_ascii=False, indent=2)


@mcp.resource(
    uri="info://1c-server-info",
    name="server_info",
    description="Подробная информация о MCP сервере"
)
async def server_info() -> str:
    """Информация о сервере"""
    return f"""
MCP сервер для 1С:Предприятие v{config.version}
===============================================

Назначение: 
Интеграция системы 1С Бухгалтерия с AI ассистентами через MCP протокол

Доступные инструменты:
- hello_1c - Приветствие и информация  
- test_calculation - Тестовый калькулятор
- generate_test_data - Генерация тестовых данных
- get_server_status - Статус сервера

Разработка: {config.author}
NPM: @tarasov46/1c-accounting-mcp
GitHub: https://github.com/tarasov46/1c-accounting-mcp

Документация: README.md
Конфигурация Claude Desktop:
{{"mcpServers": {{"1c-accounting": {{"command": "npx", "args": ["@tarasov46/1c-accounting-mcp"]}}}}}}
    """


# ==========================================
# УТИЛИТЫ (из первого сервера)
# ==========================================

def list_resources() -> str:
    """Возвращает список всех ресурсов"""
    resources = [
        {
            "name": name,
            "description": res["description"],
            "url": res.get("url")
        }
        for name, res in _REGISTERED_RESOURCES.items()
    ]
    return json.dumps({"resources": resources}, ensure_ascii=False, indent=2)


@mcp.tool()
async def get_list_resources() -> str:
    """Получить список доступных ресурсов"""
    return list_resources()


@mcp.tool()
async def get_resource(resource_name: str) -> str:
    """Получить данные конкретного ресурса

    Args:
        resource_name: Имя ресурса
    """
    if resource_name not in _REGISTERED_RESOURCES:
        return json.dumps({"error": f"Ресурс '{resource_name}' не найден"}, ensure_ascii=False)

    try:
        function = _REGISTERED_RESOURCES[resource_name]["function"]
        result = function()
        return result
    except Exception as e:
        logger.error(f"Ошибка получения ресурса {resource_name}: {e}")
        return json.dumps({"error": f"Ошибка: {str(e)}"}, ensure_ascii=False)


# ==========================================
# ЗАПУСК СЕРВЕРА
# ==========================================

def main():
    """Основная функция запуска MCP сервера"""
    # Убираем лишние логи при старте - они мешают MCP протоколу
    # logger.info(f"Запуск {config.server_name} v{config.version}")
    # logger.info(f"Автор: {config.author}")
    # logger.info(f"Доступно ресурсов: {len(_REGISTERED_RESOURCES)}")

    try:
        mcp.run(transport='stdio')
    except KeyboardInterrupt:
        pass  # Тихий выход без логов
    except Exception as e:
        # Логи ошибок только в stderr
        import sys
        print(f"ОШИБКА: {e}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()