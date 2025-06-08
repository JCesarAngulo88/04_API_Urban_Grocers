from config import data
from src import sender_stand_request
from tests import test_data
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

def positive_assert(first_name):
    user_body = get_user_body(first_name)
    server_response = sender_stand_request.post_new_user(user_body)
    assert server_response.status_code == data_constants.CREATED_CODE, f'Fail!! Server response code received in body: {server_response.status_code}'
    logger.info(f'SUCCESS: Server response code: {server_response.status_code} (Expected {data_constants.CREATED_CODE})')
    assert server_response.json()["authToken"] != "", f'Fail!! Server response code received in body: {server_response.json()["authToken"]}'
    logger.info(f'SUCCESS: authToken created: {server_response.json()["authToken"]}')
    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," + user_body["address"] + ",,," + server_response.json()["authToken"]
    assert users_table_response.text.count(str_user) == 1
    logger.info(f'SUCCESS: authToken unique!')
    time.sleep(test_data.gen_delay)

def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    server_response = sender_stand_request.post_new_user(user_body)
    assert server_response.status_code == data_constants.BAD_REQUEST, f'Fail!! Server response code received in body: {server_response.status_code}'
    logger.info(f'SUCCESS: Server response code: {server_response.status_code} (Expected {data_constants.BAD_REQUEST})')
    assert server_response.json()["code"] == data_constants.BAD_REQUEST, f'Fail!! Server response code received in body: {server_response.json()["code"]}'
    logger.info(f'SUCCESS: Server response code in body: {server_response.json()["code"]} (Expected {data_constants.BAD_REQUEST})')
    assert server_response.json()['message'] == data_constants.INVALID_FIRST_NAME_ERROR
    logger.info(f'SUCCESS: Server response message in body: {server_response.json()['message']} (Expected {data_constants.BAD_REQUEST})')
    assert "authToken" not in server_response.json()

def negative_assert_no_first_name(user_body):
    server_response = sender_stand_request.post_new_user(user_body)
    assert server_response.status_code == data_constants.BAD_REQUEST, f'Fail!! Server response code received in body: {server_response.status_code}'
    logger.info(f'SUCCESS: Server response code: {server_response.status_code} (Expected {data_constants.BAD_REQUEST})')
    assert server_response.json()["code"] == data_constants.BAD_REQUEST, f'Fail!! Server response code received in body: {server_response.json()["code"]}'
    logger.info(f'SUCCESS: Server response code in body: {server_response.json()["code"]} (Expected {data_constants.BAD_REQUEST})')
    assert server_response.json()['message'] == data_constants.MISSING_PARAM_ERROR
    logger.info(f'SUCCESS: Server response message in body: {server_response.json()['message']} (Expected {data_constants.BAD_REQUEST})')
    assert "authToken" not in server_response.json()
