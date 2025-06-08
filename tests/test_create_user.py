import logging
import pytest
from tests import test_data
from tests import functions
from config import data

logger = logging.getLogger(__name__)

@pytest.mark.parametrize('test_name', test_data.test_names2_data)
@pytest.mark.prio1
def test_create_user_2_letter_in_first_name(test_name, api_server_ready):
    logger.info(f'\nTest create user 2 letters 1 . Testing: {test_name} !!')
    functions.positive_assert(test_name)

@pytest.mark.parametrize('test_name', functions.rand_two_strings(test_data.number_strings))
@pytest.mark.prio1
def test_create_user_2_letter_in_first_name_random(test_name, api_server_ready):
    logger.info(f'\nTest create user 2 letters 2. Testing: {test_name} !!')
    functions.positive_assert(test_name)

@pytest.mark.parametrize('test_name', test_data.test_names15_data)
@pytest.mark.prio1
def test_create_user_15_letter_in_first_name(test_name, api_server_ready):
    logger.info(f'\nTest create user 15 letters. Testing: {test_name} !!')
    functions.positive_assert(test_name)

@pytest.mark.parametrize('test_name', functions.single_char_names())
@pytest.mark.prio1
def test_create_user_1_letter_in_first_name(test_name, api_server_ready):
    logger.info(f'\nTest create user 1 letter. Testing: "{test_name}" !!')
    functions.negative_assert_symbol(test_name)

@pytest.mark.parametrize('test_name', test_data.sixteen_char_names_simple)
@pytest.mark.prio1
def test_create_user_16_letter_in_first_name(test_name, api_server_ready):
    logger.info(f'\nTest create user 16 letters. Testing: "{test_name}" !!')
    functions.negative_assert_symbol(test_name)

@pytest.mark.parametrize('test_name', test_data.space_names)
@pytest.mark.prio1
def test_create_user_has_space_in_first_name(test_name, api_server_ready):
    logger.info(f'\nTest create user has space. Testing: "{test_name}" !!')
    functions.negative_assert_symbol(test_name)

@pytest.mark.parametrize('test_name', test_data.names_with_special_chars_start)
@pytest.mark.prio1
def test_create_user_has_special_symbol_in_first_name(test_name, api_server_ready):
    logger.info(f'\nTest create user has special symbol. Testing: "{test_name}" !!')
    functions.negative_assert_symbol(test_name)

@pytest.mark.parametrize('test_name', test_data.names_with_numbers)
@pytest.mark.prio1
def test_create_user_has_number_in_first_name(test_name, api_server_ready):
    logger.info(f'\nTest create user has number in. Testing: "{test_name}" !!')
    functions.negative_assert_symbol(test_name)

@pytest.mark.prio1
def test_create_user_no_first_name(api_server_ready):
    logger.info(f'\nTest user name creation without "firstName" in body')
    user_body = data.user_body.copy()
    user_body.pop("firstName") # Delete "firstName" from body json
    functions.negative_assert_no_first_name(user_body)

@pytest.mark.prio1
def test_create_user_empty_first_name(api_server_ready):
    logger.info(f'\nTest with body json: "firstName": '' ')
    user_body = functions.get_user_body("")
    functions.negative_assert_no_first_name(user_body)

@pytest.mark.parametrize('test_name', functions.rand_numbers_list(test_data.number_tests, test_data.starts_val, test_data.ends_val))
@pytest.mark.prio1
def test_create_user_number_type_first_name(test_name, api_server_ready):
    logger.info(f'\nTest with body json: "firstName" testing: {test_name} ')
    functions.negative_assert_symbol(test_name)
