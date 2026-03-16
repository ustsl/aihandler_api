import pytest
from pydantic import ValidationError

from src.api.scenarios.schemas.post import ScenarioPostSchema


def test_scenario_schema_rejects_invalid_title():
    with pytest.raises(ValidationError):
        ScenarioPostSchema(title="Bad@Scenario", description="desc")


def test_scenario_schema_forbids_extra_fields():
    with pytest.raises(ValidationError):
        ScenarioPostSchema(
            title="Scenario valid",
            description="desc",
            extra_field="forbidden",
        )
