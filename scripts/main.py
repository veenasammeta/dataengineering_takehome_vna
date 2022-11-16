from retreive_messages_and_write_to_db import retreive_message,mask, execute_values
from create_and_write_to_queue import send_messages

def main():
    queue_url = send_messages()
    df = retreive_message(queue_url)
    cols = ['user_id', 'app_version', 'device_type', 'ip', 'locale', 'device_id']    
    df = df[cols]
    df = mask(df)
    masked_cols = ['user_id', 'app_version', 'device_type', 'masked_ip', 'locale', 'masked_device_id']  
    execute_values(df, 'user_logins', masked_cols)

if __name__ == "__main__":
    main()