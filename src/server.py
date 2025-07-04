#!/usr/bin/env python3
import asyncio
import logging
import os
from typing import Any, Dict

from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Импорт тестового инструмента
from tools.test_tool import TestTool

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("1c-accounting-mcp")

# Создание экземпляра MCP сервера
mcp = FastMCP("1c-accounting-mcp")

# Инициализация тестового инструмента
test_tool = TestTool()


# ==========================================
# ТЕСТОВЫЕ ИНСТРУМЕНТЫ
# ==========================================

@mcp.tool()
async def hello_1c(name: str = "Пользователь") -> str:
    """Приветствие и информация о MCP сервере для 1С

    Args:
        name: Имя пользователя для приветствия
    """
    logger.info(f"Вызван hello_1c для пользователя: {name}")
    return await test_tool.hello_1c(name)


@mcp.tool()
async def test_calculation(a: float, b: float, operation: str = "add") -> str:
    """Тестовый калькулятор для проверки работы MCP

    Args:
        a: Первое число
        b: Второе число
        operation: Операция (add, subtract, multiply, divide)
    """
    logger.info(f"Вызван test_calculation: {a} {operation} {b}")
    return await test_tool.test_calculation(a, b, operation)


@mcp.tool()
async def generate_test_data(count: int = 5) -> str:
    """Генерирует тестовые данные имитирующие работу с 1С

    Args:
        count: Количество записей для генерации (максимум 20)
    """
    logger.info(f"Генерация тестовых данных, количество: {count}")
    return await test_tool.generate_test_data(count)


# ==========================================
# РЕСУРСЫ
# ==========================================

@mcp.resource(
    uri="info://1c-server",
    name="server_info",
    description="Информация о MCP сервере для 1С"
)
async def server_info() -> str:
    """Возвращает информацию о сервере"""
    return """
🏢 MCP сервер для 1С:Предприятие
================================

📊 Назначение: Интеграция 1С Бухгалтерии с AI ассистентами через MCP протокол

🛠 Доступные инструменты:
- hello_1c - Приветствие и информация о сервере
- test_calculation - Тестовый калькулятор  
- generate_test_data - Генерация тестовых данных

🚀 Разработано: @tarasov46
📧 GitHub: https://github.com/tarasov46/1c-accounting-mcp
📦 NPM: @tarasov46/1c-accounting-mcp

🔧 Для использования в Claude Desktop:
{"mcpServers": {"1c-accounting": {"command": "npx", "args": ["@tarasov46/1c-accounting-mcp"]}}}
    """


# ==========================================
# ЗАПУСК СЕРВЕРА
# ==========================================

def main():
    """Основная функция запуска MCP сервера"""
    logger.info("Запуск MCP сервера для 1С Бухгалтерии...")
    logger.info("Организация: @tarasov46")
    logger.info("Доступно инструментов: 3")
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
