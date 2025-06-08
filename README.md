
# Author: Julio Angulo
# Date: 08/06/2025
# Version: 0.1
#
# Regression test to user creation to param "firstname" endpoint: /api/v1/users was created  
#
# Check requirements.txt
# Commands to execute:
- python3 -m tests.test_create_user # -m flag When your file uses relative imports (from .. etc.)n you want to run code as a module within a package n working on structured apps or libraries
- python3 -m src.sender_stand_request
- pytest tests/test_create_user.py # Run from a test file
- pytest tests/ # Run all
- pytest -m smoke # Run by marks
- pytest tests/test_users.py::test_create_valid_user # Run by test function
- pytest -m prio1 tests/test_create_user.py