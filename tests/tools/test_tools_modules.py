import pytest

from src.modules.tools.executor import execute_http_tool, execute_tool
from src.modules.tools.validator import validate_tool_arguments


class _ToolStub:
    def __init__(self, **kwargs):
        self.transport = kwargs.get("transport", "http_json")
        self.method = kwargs.get("method", "POST")
        self.url = kwargs.get("url", "https://api.example.com/tool")
        self.headers_template = kwargs.get("headers_template", {})
        self.query_template = kwargs.get("query_template", {})
        self.body_template = kwargs.get("body_template", {})
        self.auth_type = kwargs.get("auth_type", "none")
        self.auth_secret_ref = kwargs.get("auth_secret_ref")
        self.timeout_sec = kwargs.get("timeout_sec", 5)
        self.max_response_bytes = kwargs.get("max_response_bytes", 262144)


def test_validate_tool_arguments_required_fields():
    schema = {"type": "object", "required": ["value"]}
    assert validate_tool_arguments({"value": 1}, schema) is None
    assert (
        validate_tool_arguments({}, schema)
        == "Missing required field: value"
    )


@pytest.mark.asyncio
async def test_execute_tool_mcp_not_implemented():
    tool = _ToolStub(transport="mcp")
    result = await execute_tool(tool, {})
    assert result["status"] == "error"
    assert "not implemented" in result["error"].lower()


@pytest.mark.asyncio
async def test_execute_http_tool_blocks_localhost():
    tool = _ToolStub(url="http://127.0.0.1:8080/internal")
    result = await execute_http_tool(tool, {"value": 1})
    assert result["status"] == "error"
    assert result["error"] == "Forbidden tool host"
