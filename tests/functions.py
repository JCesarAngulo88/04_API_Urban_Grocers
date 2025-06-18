from config import data
from src import sender_stand_request
from tests import data_constants
import random
import string
import logging
import time

# Get a logger for this specific module/file
logger = logging.getLogger(__name__)

def rand_numbers_list(num: int, min_val: int = 1, max_val: int = 100) -> list[int]:
    """
    Generates a list containing 'num' random integers.

    :param num: The number of random integers to generate in the list.
                Must be a non-negative integer.
    :param min_val: (Optional) The minimum possible value for the random integers (inclusive). Defaults to 1.
    :param max_val: (Optional) The maximum possible value for the random integers (inclusive). Defaults to 100.
    :return: A list of 'num' random integers.
    """
    if not isinstance(num, int) or num < 0:
        raise ValueError("The 'num' parameter must be a non-negative integer.")
    if min_val > max_val:
        raise ValueError("min_val cannot be greater than max_val.")

    numbers = []
    for _ in range(num):
        numbers.append(random.randint(min_val, max_val))
    return numbers

def rand_two_strings(n) -> list[str]:
    """
        Generate a list of random 2-letter lowercase strings.
        Parameters:
            n (int): The number of random strings to generate.
        Returns:
            list of str: A list containing 'n' strings, each with 2 random lowercase letters.
    """
    return [''.join(random.choices(string.ascii_lowercase, k=2)) for _ in range(n)]

def single_char_names() -> list[str]:
    """
        Generate a list of single-character names using all lowercase and uppercase letters.

        Returns:
            list[str]: A list containing all lowercase ('a' to 'z') and uppercase ('A' to 'Z') letters as individual strings.
    """
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    return list(lowercase_letters + uppercase_letters)

def get_user_body(first_name) -> dict:
    """
    This function copy the default dict to do testing without modify it.
    :param first_name: Testing param 'first_name'
    :return: user_body modified dict
    """
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body

def get_kit_body(name) -> dict:
    """
        Copies the default kit body dictionary and updates the 'name' field.

        This function ensures that the original dictionary is not modified, allowing for the creation of custom kit body payloads for testing.

        :param name: The string value to assign to the 'name' field of the kit body.
        :return: A new dictionary representing the kit body with the updated 'name'.
    """
    current_body = data.kit_body.copy()
    current_body["name"] = name
    return current_body

def get_new_user_token() -> str:
    """
        Creates a new user by sending a POST request and extracts the authentication token.

        This function uses the default user body (`data.user_body`) to register a new user
        via the API and then parses the server's JSON response to obtain the `authToken`.

        :return: The authentication token (authToken) as a string obtained from the server's JSON response.
    """
    server_response_user = sender_stand_request.post_new_user(data.user_body)
    return server_response_user.json()["authToken"]

def positive_assert_user_creation_name(data_test_first_name):
    new_json_body = get_user_body(data_test_first_name)
    server_response_user = sender_stand_request.post_new_user(new_json_body)
    logger.info(f'\nThe json object response: {server_response_user.json()}')
    assert server_response_user.status_code == data_constants.CREATED_CODE, f'Fail!! Server response code received: {server_response_user.status_code}, (Expected: "{data_constants.CREATED_CODE}").'
    logger.info(f'SUCCESS: Server response code: {server_response_user.status_code} (Expected {data_constants.CREATED_CODE})')
    assert server_response_user.json()["authToken"] != "", f'Fail!! Server response code received in body: {server_response_user.json()["authToken"]}'
    logger.info(f'SUCCESS: authToken created: {server_response_user.json()["authToken"]}')
    users_table_response = sender_stand_request.get_users_table()
    str_user = new_json_body["firstName"] + "," + new_json_body["phone"] + "," + new_json_body["address"] + ",,," + server_response_user.json()["authToken"]
    assert users_table_response.text.count(str_user) == 1
    logger.info(f'SUCCESS: authToken unique!')
    time.sleep(data_constants.GENERAL_DELAY)

def positive_assert_kit_creation_auth(data_test_name):
    user_token = get_new_user_token()
    new_kit_body = get_kit_body(data_test_name)
    logger.info(f'New body json: {new_kit_body}')
    server_response_kit = sender_stand_request.post_new_client_kit(new_kit_body, user_token)
    logger.info(f'\nThe json object response: {server_response_kit.json()}')
    assert server_response_kit.status_code == data_constants.CREATED_CODE, f'Fail!! Server response code received in body to Post authorization kit user: {server_response_kit.status_code}, (Expected: "{data_constants.CREATED_CODE}").'
    logger.info(f'\nSUCCESS: Server response code: {server_response_kit.status_code} (Expected {data_constants.CREATED_CODE})')
    assert  server_response_kit.json()["name"] == new_kit_body["name"], f'Fail!! Server response json received Post authorization kit user "name": {server_response_kit.json()["name"]}'
    logger.info(f'SUCCESS: json "name" response: "{server_response_kit.json()["name"]}" (Expected "{new_kit_body["name"]}" )')
    time.sleep(data_constants.GENERAL_DELAY)

def negative_assert_user_creation_name_code_400(data_test_first_name):
    user_body = get_user_body(data_test_first_name)
    logger.info(f'New body json: {data_test_first_name}')
    server_response = sender_stand_request.post_new_user(user_body)
    logger.info(f'\nThe json object response: {server_response.json()}')
    assert server_response.status_code == data_constants.BAD_REQUEST, f'Fail!! Server response code received: {server_response.status_code}, (Expected: "{data_constants.BAD_REQUEST}").'
    logger.info(f'SUCCESS: Server response code: {server_response.status_code} (Expected {data_constants.BAD_REQUEST})')
    assert server_response.json()["code"] == data_constants.BAD_REQUEST, f'Fail!! Server response code received in body: {server_response.json()["code"]}'
    logger.info(f'SUCCESS: Server response code in body: {server_response.json()["code"]} (Expected {data_constants.BAD_REQUEST})')
    assert server_response.json()['message'] == data_constants.INVALID_FIRST_NAME_ERROR
    logger.info(f'SUCCESS: Server response message in body: {server_response.json()['message']} (Expected {data_constants.BAD_REQUEST})')
    assert "authToken" not in server_response.json()
    time.sleep(data_constants.GENERAL_DELAY)

def negative_assert_kit_creation_auth_code_400(data_test_name):
    user_token = get_new_user_token()
    new_kit_body = get_kit_body(data_test_name)
    logger.info(f'New body json: {new_kit_body}')
    server_response_kit = sender_stand_request.post_new_client_kit(new_kit_body, user_token)
    logger.info(f'\nThe json object response: {server_response_kit.json()}')
    assert server_response_kit.status_code == data_constants.BAD_REQUEST, f'\nFail!! Server response code received: {server_response_kit.status_code}, (Expected: {data_constants.BAD_REQUEST})'
    logger.info(f'SUCCESS: Server response code: {server_response_kit.status_code} (Expected {data_constants.BAD_REQUEST})')
    time.sleep(data_constants.GENERAL_DELAY)

def negative_assert_user_creation_name_no_key_json(test_body):
    logger.info(f'New body json: {test_body}')
    server_response = sender_stand_request.post_new_user(test_body)
    logger.info(f'\nThe json object response: {server_response.json()}')
    assert server_response.status_code == data_constants.BAD_REQUEST, f'Fail!! Server response code received: {server_response.status_code}, (Expected: "{data_constants.BAD_REQUEST}").'
    logger.info(f'SUCCESS: Server response code: {server_response.status_code} (Expected {data_constants.BAD_REQUEST})')
    assert server_response.json()["code"] == data_constants.BAD_REQUEST, f'Fail!! Server response code received in body: {server_response.json()["code"]}'
    logger.info(f'SUCCESS: Server response code in body: {server_response.json()["code"]} (Expected {data_constants.BAD_REQUEST})')
    assert server_response.json()['message'] == data_constants.MISSING_PARAM_ERROR
    logger.info(f'SUCCESS: Server response message in body: {server_response.json()['message']} (Expected {data_constants.BAD_REQUEST})')
    assert "authToken" not in server_response.json()
    time.sleep(data_constants.GENERAL_DELAY)

def negative_assert_kit_creation_auth_no_key_json(test_body):
    logger.info(f'New body json: {test_body}')
    user_token = get_new_user_token()
    server_response = sender_stand_request.post_new_client_kit(test_body, user_token)
    logger.info(f'\nThe json object response: {server_response.json()}')
    assert server_response.status_code == data_constants.BAD_REQUEST, f'Fail!! Server response code received: {server_response.status_code}, (Expected: "{data_constants.BAD_REQUEST}").'
    logger.info(f'SUCCESS: Server response code: {server_response.status_code} (Expected {data_constants.BAD_REQUEST})')
    time.sleep(data_constants.GENERAL_DELAY)
