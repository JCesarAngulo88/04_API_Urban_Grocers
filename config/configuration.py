URL_SERVICE = 'https://cnt-19a9da1d-d54c-453b-b6a2-56545a9f422d.containerhub.tripleten-services.com'
DOC_PATH = "/docs/"
LOG_MAIN_PATH = '/api/logs/main/, params={"count":20}'
USERS_TABLE_PATH = "/api/db/resources/user_model.csv"
CREATE_USER_PATH = "/api/v1/users/"
PRODUCTS_KITS_PATH = "/api/v1/products/kits/"

CREATE_USER_ENDPOINT: str = "/api/v1/users/"
KITS_ENDPOINT: str = "/api/v1/kits"
RECEIVED_KITS: str = "/api/v1/kits/search?name=New" # TODO: Work from scratch in this endpoint