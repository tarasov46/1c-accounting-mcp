import asyncio
import random
from datetime import datetime


class TestTool:
    """Простой тестовый инструмент для проверки MCP сервера"""

    async def hello_1c(self, name: str = "Пользователь") -> str:
        """Простое приветствие с информацией о сервере"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return f"""
🚀 Привет, {name}!

Добро пожаловать в MCP сервер для 1С Бухгалтерии!

📊 Информация о сервере:
- Время: {current_time}
- Статус: Работает нормально ✅
- Версия: 1.0.0
- Организация: @tarasov46

🛠 Этот сервер предназначен для работы с 1С:Предприятие через MCP протокол.

💡 Для использования в Claude Desktop добавьте в конфигурацию:
{{"mcpServers": {{"1c-accounting": {{"command": "npx", "args": ["@tarasov46/1c-accounting-mcp"]}}}}}}
        """

    async def test_calculation(self, a: float, b: float, operation: str = "add") -> str:
        """Тестовый калькулятор для проверки передачи параметров"""
        try:
            if operation == "add":
                result = a + b
                symbol = "+"
            elif operation == "subtract":
                result = a - b
                symbol = "-"
            elif operation == "multiply":
                result = a * b
                symbol = "×"
            elif operation == "divide":
                if b == 0:
                    return "Ошибка: деление на ноль!"
                result = a / b
                symbol = "÷"
            else:
                return f"Неизвестная операция: {operation}"

            return f"🧮 Результат: {a} {symbol} {b} = {result}"

        except Exception as e:
            return f"Ошибка вычисления: {str(e)}"

    async def generate_test_data(self, count: int = 5) -> str:
        """Генерирует тестовые данные (имитация работы с 1С)"""
        if count > 20:
            return "Максимум 20 записей для теста"

        companies = ["ООО Рога и Копыта", "ИП Иванов", "ООО Технологии", "ЗАО Прогресс", "ООО Инновации"]
        operations = ["Поступление товара", "Реализация услуг", "Оплата поставщику", "Получение оплаты"]

        result = "📋 Тестовые данные (имитация 1С):\n\n"

        for i in range(count):
            company = random.choice(companies)
            operation = random.choice(operations)
            amount = random.randint(1000, 100000)

            result += f"{i + 1}. {company}\n"
            result += f"   Операция: {operation}\n"
            result += f"   Сумма: {amount:,} руб.\n"
            result += f"   Дата: {datetime.now().strftime('%d.%m.%Y')}\n\n"

        return result
