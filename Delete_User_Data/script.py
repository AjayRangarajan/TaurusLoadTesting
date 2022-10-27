import psycopg2
from dotenv import load_dotenv
import os

load_dotenv("./.env")

DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")


def get_user_id(cur, phone_number):
    cur.execute(f"SELECT id FROM public.users WHERE phone_number='{phone_number}';")
    user = cur.fetchone()
    if not user:
        raise Exception(f"User with this phone number {phone_number} does not exists.")
    return user[0]

def delete_user_activity(cur, user_id):
    print(f"Deleting activity of the user {user_id}")

    cur.execute(f"SELECT activity_id FROM public.activity_sender WHERE user_id='{user_id}';")
    sender_activity_ids = cur.fetchall()
    cur = execute_sql(cur, f"DELETE FROM public.activity_sender WHERE user_id='{user_id}';")
    cur.execute(f"SELECT activity_id FROM public.activity_recipient WHERE user_id='{user_id}';")
    recipient_activity_ids = cur.fetchall()
    cur = execute_sql(cur, f"DELETE FROM public.activity_recipient WHERE user_id='{user_id}';")

    activity_ids = sender_activity_ids + recipient_activity_ids
    if not activity_ids:
        print(f"The user {user_id} does not have any activity.")
        return cur
    for activity in activity_ids:
        cur = execute_sql(cur, f"DELETE FROM public.activity WHERE id='{activity}';")
        return cur
        

def delete_user_payments(cur, user_id):
    print(f"Deletings payments of the user {user_id}")
    cur.execute(f"SELECT id FROM public.payments WHERE user_id='{user_id}';")
    payment_ids = cur.fetchall()
    if not payment_ids:
        print(f"The user {user_id} does not have any payments")
        return cur
    for id in payment_ids:
        cur = execute_sql(cur, f"DELETE FROM public.failed_payment_callbacks WHERE payment_id='{id}';")
        cur = execute_sql(cur, f"DELETE FROM public.payment_callbacks WHERE payment_id='{id}';")
    return cur


def delete_user_data(cur, phone_number):
    user_id = get_user_id(cur, phone_number)
    cur = delete_user_activity(cur, user_id)
    cur = delete_user_payments(cur, user_id)
    execute_sql(cur, f"DELETE FROM public.app_settings WHERE user_id='{user_id}';")
    execute_sql(cur, f"DELETE FROM public.active_plans WHERE user_id='{user_id}';")
    execute_sql(cur, f"DELETE FROM public.connectycube_rooms WHERE occupant1_id='{user_id}' OR occupant2_id='{user_id}';")
    execute_sql(cur, f"DELETE FROM public.connectycube_accounts WHERE user_id='{user_id}';")
    execute_sql(cur, f"DELETE FROM public.device_configuration WHERE user_id='{user_id}';")
    execute_sql(cur, f"DELETE FROM public.documents WHERE user_id='{user_id}';")
    execute_sql(cur, f"DELETE FROM public.feedbacks WHERE user_id='{user_id}';")
    execute_sql(cur, f"DELETE FROM public.interests WHERE user_id='{user_id}';")
    execute_sql(cur, f"DELETE FROM public.messages WHERE sender_id='{user_id}' OR recepient_id='{user_id}';")
    execute_sql(cur, f"DELETE FROM public.matches WHERE user_id='{user_id}';")
    execute_sql(cur, f"DELETE FROM public.photos WHERE user_id='{user_id}';")
    execute_sql(cur, f"DELETE FROM public.questionnaire_responses WHERE user_id='{user_id}';")
    execute_sql(cur, f"DELETE FROM public.user_contacts WHERE user_id='{user_id}';")
    execute_sql(cur, f"DELETE FROM public.user_details WHERE user_id='{user_id}';")
    execute_sql(cur, f"DELETE FROM public.user_devices WHERE user_id='{user_id}';")
    execute_sql(cur, f"DELETE FROM public.user_preferences WHERE user_id='{user_id}';")
    execute_sql(cur, f"DELETE FROM public.user_inbox_messages WHERE user_id='{user_id}';")
    execute_sql(cur, f"DELETE FROM public.verification WHERE user_id='{user_id}';")
    execute_sql(cur, f"DELETE FROM public.users WHERE id='{user_id}';")
    return cur


def execute_sql(cur, query):
    print(f"Executing '{query}'")
    print(f'Affected {cur.rowcount} rows')
    cur.execute(query)
    return cur

def delete_users(arr):
    try:
        conn = psycopg2.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT)

        cur = conn.cursor()
        print("Created cursor")
        for phone_number in arr:
            print(f"Deleting the user {phone_number}")
            cur = delete_user_data(cur, phone_number)
            conn.commit()
            print(f"Deleted the user {phone_number} successfully")

    except Exception as e:
        print(e)

    finally:
        cur.close()
        if conn is not None:
            print("closing connection")
            conn.close()


phone_number_list = ["6666600005",]
delete_users(phone_number_list)


    # with conn, conn.cursor() as cur:
    #     delete_user_data(cur, phone_number)

    # conn.autocommit = True
    # conn.set_session(autocommit=True)
    
    # phone_number = "6666600001"
    # user_id = get_user_id(cur, "6666600001")
    # user_id = "2a6064fd-c66d-4901-89ca-247365d65afc"
    # cur = delete_user_data(cur, phone_number)
    # conn.commit()
    # cur.close()