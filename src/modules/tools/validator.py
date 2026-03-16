def validate_tool_arguments(args: dict, schema: dict | None) -> str | None:
    if schema is None:
        return None
    if not isinstance(schema, dict):
        return "Tool schema must be an object"
    if not isinstance(args, dict):
        return "Tool arguments must be an object"

    schema_type = schema.get("type")
    if schema_type and schema_type != "object":
        return "Tool schema type must be object"

    required_fields = schema.get("required") or []
    if not isinstance(required_fields, list):
        return "Tool schema required must be an array"

    for field in required_fields:
        if field not in args:
            return f"Missing required field: {field}"
    return None
