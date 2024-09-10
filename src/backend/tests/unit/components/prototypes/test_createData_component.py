import pytest
from langflow.components.prototypes.CreateData import CreateDataComponent
from langflow.schema import Data


@pytest.fixture
def create_data_component():
    return CreateDataComponent()


def test_update_build_config(create_data_component):
    build_config = {
        "number_of_fields": {
            "type": "int",
            "value": 2,
        },
        "text_key": {
            "type": "str",
            "value": "",
        },
        "text_key_validator": {
            "type": "bool",
            "value": False,
        },
    }
    updated_config = create_data_component.update_build_config(
        build_config=build_config, field_value=3, field_name="number_of_fields"
    )

    assert "field_1_key" in updated_config
    assert "field_2_key" in updated_config
    assert "field_3_key" in updated_config
    assert updated_config["number_of_fields"]["value"] == 3


def test_update_build_config_exceed_limit(create_data_component):
    build_config = {
        "number_of_fields": {
            "type": "int",
            "value": 2,
        },
        "text_key": {
            "type": "str",
            "value": "",
        },
        "text_key_validator": {
            "type": "bool",
            "value": False,
        },
    }
    with pytest.raises(
        ValueError, match="Number of fields cannot exceed 15. Try using a Component to combine two Data."
    ):
        create_data_component.update_build_config(build_config, 16, "number_of_fields")


@pytest.mark.asyncio
async def test_build_data(create_data_component):
    create_data_component._attributes = {
        "field_1_key": {"key1": "value1"},
        "field_2_key": {"key2": "value2"},
    }
    create_data_component.text_key = "key1"
    create_data_component.text_key_validator = False

    result = await create_data_component.build_data()

    assert isinstance(result, Data)
    assert result.data == {"key1": "value1", "key2": "value2"}
    assert result.text_key == "key1"


def test_get_data(create_data_component):
    create_data_component._attributes = {
        "field_1_key": {"key1": "value1"},
        "field_2_key": {"key2": "value2"},
    }

    result = create_data_component.get_data()

    assert result == {"key1": "value1", "key2": "value2"}


def test_validate_text_key_valid(create_data_component):
    # Arrange
    create_data_component._attributes = {
        "field_1_key": {"key1": "value1"},
        "field_2_key": {"key2": "value2"},
    }
    create_data_component.text_key = "key1"

    # Act & Assert
    try:
        create_data_component.validate_text_key()
    except ValueError:
        pytest.fail("validate_text_key() raised ValueError unexpectedly!")

    # Additional assertions
    assert create_data_component.text_key == "key1"
    assert "key1" in create_data_component.get_data()


def test_validate_text_key_invalid(create_data_component):
    # Arrange
    create_data_component._attributes = {
        "field_1_key": {"key1": "value1"},
        "field_2_key": {"key2": "value2"},
    }
    create_data_component.text_key = "invalid_key"

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        create_data_component.validate_text_key()

    # Check for the exact error message
    expected_error_message = f"Text Key: {create_data_component.text_key} not found in the Data keys: {','.join(create_data_component.get_data().keys())}"
    assert str(exc_info.value) == expected_error_message


def test_post_code_processing(create_data_component):
    new_frontend_node = {"template": {"number_of_fields": {"value": 2}}}
    current_frontend_node = {}

    result = create_data_component.post_code_processing(new_frontend_node, current_frontend_node)

    assert "field_1_key" in result["template"]
    assert "field_2_key" in result["template"]
    assert result["template"]["number_of_fields"]["value"] == 2
