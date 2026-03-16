import ipaddress
from urllib.parse import urlparse

import httpx


def _is_forbidden_host(url: str) -> bool:
    host = (urlparse(url).hostname or "").strip().lower()
    if not host:
        return True
    if host in {"localhost"}:
        return True
    try:
        ip = ipaddress.ip_address(host)
        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_multicast
            or ip.is_reserved
            or ip.is_unspecified
        ):
            return True
    except ValueError:
        pass
    return False


async def execute_http_tool(tool, args: dict) -> dict:
    if not tool.url:
        return {"error": "Tool URL is not configured", "status": "error"}
    if _is_forbidden_host(tool.url):
        return {"error": "Forbidden tool host", "status": "error"}

    method = (tool.method or "POST").upper()
    headers = dict(tool.headers_template or {})
    query_params = dict(tool.query_template or {})

    if tool.auth_type == "bearer" and tool.auth_secret_ref:
        headers["Authorization"] = f"Bearer {tool.auth_secret_ref}"

    if tool.auth_type == "api_key_query" and tool.auth_secret_ref:
        if "=" in tool.auth_secret_ref:
            key, value = tool.auth_secret_ref.split("=", 1)
            query_params[key] = value
        else:
            query_params["api_key"] = tool.auth_secret_ref

    timeout = int(tool.timeout_sec or 15)
    max_response_bytes = int(tool.max_response_bytes or 262144)

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            if method == "GET":
                query_params.update(args)
                response = await client.get(tool.url, params=query_params, headers=headers)
            else:
                body = dict(tool.body_template or {})
                body.update(args)
                response = await client.post(
                    tool.url,
                    params=query_params,
                    json=body,
                    headers=headers,
                )
            response.raise_for_status()

            raw_content = response.content or b""
            if len(raw_content) > max_response_bytes:
                return {"error": "Tool response is too large", "status": "error"}

            content_type = response.headers.get("content-type", "")
            if "application/json" in content_type:
                payload = response.json()
            else:
                payload = response.text
            return {"result": payload, "status": "success"}
    except httpx.TimeoutException:
        return {"error": "Tool request timeout", "status": "timeout"}
    except httpx.HTTPStatusError as exc:
        return {
            "error": f"Tool request failed with status {exc.response.status_code}",
            "status": "error",
        }
    except Exception as exc:
        return {"error": str(exc), "status": "error"}


async def execute_tool(tool, args: dict) -> dict:
    transport = (tool.transport or "http_json").lower()
    if transport == "mcp":
        return {"error": "MCP transport is not implemented yet", "status": "error"}
    return await execute_http_tool(tool=tool, args=args)
