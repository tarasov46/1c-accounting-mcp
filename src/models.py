import dataclasses
from abc import ABC, abstractmethod
from typing import Dict, List
from mcp import Tool
from mcp.types import TextContent


class BaseTool(ABC):
    """Базовый класс для инструментов MCP"""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def input_schema(self) -> dict:
        pass

    def to_mcp_tool(self) -> Tool:
        return Tool(
            name=self.name,
            description=self.description,
            inputSchema=self.input_schema,
        )

    @abstractmethod
    def execute(self, input_dict: dict) -> list[TextContent]:
        pass


@dataclasses.dataclass
class ServerConfig:
    """Конфигурация сервера"""
    server_name: str = "1c-accounting-mcp"
    version: str = "1.0.1"
    author: str = "tarasov46"
    debug: bool = False


@dataclasses.dataclass
class UserCredentials:
    """Учетные данные пользователя для 1С (если понадобится в будущем)"""
    username_1c: str = ""
    password_1c: str = ""
    bearer_1c: str = ""
    path_base: str = ""
    path_rest: str = ""
    use_cloud42_auth: bool = False
    cloud42_token: str = ""