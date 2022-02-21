from importlib.resources import path
from os import access
import boto3 
from botocore.exceptions import NoCredentialsError 
import operador.acess as acess
from datetime import datetime

ACCESS_KEY = acess.KeyId  
SECRET_KEY = acess.SecretKey

def upload_csv_data(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

### escrevendo o path para o upload
filename='Sales'
date = datetime.today().strftime('%Y-%m-%d')
filepath = str((f"datasource\{filename}_{date}.csv".format(filename, date)))
# filepath= str('Sales_2022-02-18.csv')

uploaded = upload_csv_data(local_file=filepath, bucket='datasource20220218', s3_file=filename)