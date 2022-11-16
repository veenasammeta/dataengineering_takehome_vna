import json
import gzip
import localstack_client.session as boto3
import pandas as pd
import psycopg2
import hashlib
import psycopg2.extras as extras

def retreive_message(queue_url):
    sqs = boto3.client("sqs")
    all_data=[]
    for i in range(100):
        response = sqs.receive_message(QueueUrl=queue_url,MaxNumberOfMessages=1,WaitTimeSeconds=10)
        d = response.get('Messages')[0]['Body']
        d = json.loads(d)
        all_data.append(d)
    df = pd.DataFrame(all_data)
    print(df.columns)
    return df

def mask(df):
    df['device_id'] = df['device_id'].astype(str)
    df['device_id'] = df['device_id'].apply(lambda x: hashlib.sha256(x.encode()).hexdigest())
    df['ip'] = df['ip'].astype(str)
    df['ip'] = df['ip'].apply(lambda x: hashlib.sha256(x.encode()).hexdigest())    
    return df

def execute_values(df, table, cols):
    cols = ','.join(list(cols))
    conn = psycopg2.connect(
    database="postgres", user='postgres', password='postgres', host='localhost', port='5432') 
    data_tuples = [tuple(x) for x in df.to_numpy()]
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cursor = conn.cursor()
    try:
        extras.execute_values(cursor, query, data_tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while inserting!!!!!!: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("Data is inserted into table!!!!")
    cursor.close()    
    
    