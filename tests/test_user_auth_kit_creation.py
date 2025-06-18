import pytest
import logging
from config import data
from tests import functions, test_data

logger = logging.getLogger(__name__)

@pytest.mark.parametrize('test_name_json', test_data.one_character_test_data)
@pytest.mark.prio1
def test_create_user_kit_1_letter_name(test_name_json, api_server_ready):
    logger.info(f'\nTest create user kit user auth 1 letter name kit. Testing: {test_name_json} !!')
    functions.positive_assert_kit_creation_auth(test_name_json, )

@pytest.mark.prio1
def test_create_user_kit_511_letter_name(api_server_ready):
    logger.info(f'\nTest create kit auth with 511 characters in the body json "name".')
    functions.positive_assert_kit_creation_auth(test_data.DATA_TEST_511)

@pytest.mark.prio1
def test_create_user_kit_null_name(api_server_ready):
    logger.info(f'\nTest create kit auth with 512 characters in the body json "name".')
    functions.negative_assert_kit_creation_auth_code_400("")

@pytest.mark.prio1
def test_create_user_kit_512_letter_name(api_server_ready):
    logger.info(f'\nTest create kit auth with 512 characters in the body json "name".')
    functions.negative_assert_kit_creation_auth_code_400(test_data.DATA_TEST_512)

@pytest.mark.parametrize('test_name_json', ['"№%@",', "@#%", '#"$%']) # TODO: Create a function
@pytest.mark.prio1
def test_create_user_kit_special_char_name(test_name_json, api_server_ready):
    logger.info(f'\nTest create kit auth with special characters in the body json "name". Testing "{test_name_json}" !!')
    functions.positive_assert_kit_creation_auth(test_name_json)

@pytest.mark.parametrize('test_name_json', test_data.space_names)
@pytest.mark.prio1
def test_create_user_kit_spaces_name(test_name_json, api_server_ready):
    logger.info(f'\nTest create kit auth with spaces in the body json "name". Testing "{test_name_json}" !!')
    functions.positive_assert_kit_creation_auth(test_name_json)

@pytest.mark.parametrize('test_name_json', test_data.names_with_numbers)
@pytest.mark.prio1
def test_create_user_kit_has_number_name(test_name_json, api_server_ready):
    logger.info(f'\nTest create kit auth with numbers in the body json "name". Testing "{test_name_json}" !!')
    functions.positive_assert_kit_creation_auth(test_name_json)

@pytest.mark.prio1
def test_create_user_kit_no_name(api_server_ready):
    logger.info(f'\nTest create kit auth without "name" in the body json.')
    new_kit_body = data.kit_body.copy()
    new_kit_body.pop("name")
    functions.negative_assert_kit_creation_auth_no_key_json(new_kit_body)

@pytest.mark.parametrize('test_name_json', test_data.numbers_test)
@pytest.mark.prio1
def test_create_user_kit_type_number_name(test_name_json):
    logger.info(f'\nTest create kit auth with numbers in the body json "name". Testing: {test_name_json} !!')
    new_kit_body = functions.get_kit_body(test_name_json)
    functions.negative_assert_kit_creation_auth_code_400(new_kit_body)
