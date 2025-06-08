from config import configuration as conf
from config import data as dt
import requests

def get_docs():
    return requests.get(conf.URL_SERVICE + conf.DOC_PATH)

def get_logs():
    return requests.get(conf.URL_SERVICE + conf.LOG_MAIN_PATH)

def get_users_table():
    return requests.get(conf.URL_SERVICE + conf.USERS_TABLE_PATH)

def post_new_user(body):
    return requests.post(conf.URL_SERVICE + conf.CREATE_USER_PATH,  # inserta la dirección URL completa
                         json=body,  # inserta el cuerpo de solicitud
                         headers=dt.headers)  # inserta los encabezados

def post_products_kits(body):
    return requests.post(conf.URL_SERVICE + conf.PRODUCTS_KITS_PATH,
                         # inserta la dirección URL completa
                         json=body,  # inserta el cuerpo de solicitud
                         headers=dt.headers)  # inserta los encabezados

def main():

    # --- Realizar las solicitudes ---
    response_doc = get_docs()
    print(response_doc) # Puedes dejar esto o comentarlo si solo te interesa el CSV de users

    #response_post = post_new_user(data.user_body)
    #print(response_post.status_code)
    #print(response_post.json())

    #response_post_kits = post_products_kits(data.product_ids)
    #print(response_post_kits)
    #print(response_post_kits.json())

    response_table = get_users_table()
    print(response_table.text)

    # --- Imprimir información de la respuesta y el contenido CSV ---
    # print(f"--- Detalles de la respuesta para {configuration.USERS_TABLE_PATH} ---")
    # print(f"  Código de estado: {response_table.status_code}")
    # print(f"  Encabezados: {response_table.headers}")
    #
    # if response_table.status_code == 200:
    #     # Opcional: Verificar el Content-Type para confirmar que es CSV
    #     content_type = response_table.headers.get('Content-Type', '')
    #     if 'text/csv' in content_type:
    #         print("\n--- Contenido CSV ---")
    #         print(response_table.text) # ¡Esto imprimirá el contenido CSV directamente!
    #         print("--- Fin del Contenido CSV ---")
    #     else:
    #         print(f"\nLa respuesta no es un CSV (Content-Type: {content_type}).")
    #         print("--- Contenido (primeros 500 caracteres) ---")
    #         print(response_table.text[:500]) # Imprime los primeros 500 caracteres si no es CSV
    #         print("--- Fin del Contenido ---")
    # else:
    #     print(f"\nLa solicitud a {configuration.USERS_TABLE_PATH} falló con el código de estado: {response_table.status_code}")
    #     print(f"Contenido de la respuesta de error: {response_table.text}")

if __name__ == "__main__":
    main()
