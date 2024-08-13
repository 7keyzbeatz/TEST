import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def main():
    # Replace this JSON data with your actual service account JSON
    service_account_json = {
        "type": "service_account",
        "project_id": "admob-432400",
        "private_key_id": "81c70d14c5c5424debf8e55dc51243fc184cf611",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCXb2gAr3HisVoO\nNltt5ngyialYuR3N0HQoTCIOq/VwyY3RTRaKXZuJcHoRCNJkWyabDkcAcZZaQY9t\n9MB/9VqApU6a92GSL9rl2pJYdqz+7oBmtazoJVhYEDFxqzlbb9rU6Vf7VVl6aZuz\nQHZU7i2u7GrvGVOE7njzMwbJMobk7VqZ7S2maZyRES5W8eFpk7N/gB3bDIg0piFw\nbgJ5qWpuOZGiN6I6I162tsEbSJCR3u/eArU9jveWcIvxah0gYAY5Jv7s3e4YitER\nEQaxgmF28ZLRp3lnAOS9OmLIHQjzPZIuqbVRRHzEkBL/Iz+Pp95D68+e1RyMAVMQ\nOFsaGZkJAgMBAAECggEAALUbsnEfYj87hqMjXzU7Qi/Zc4Qoivxv0SZgka/6TWTA\n/bAorEx5UbWNpG8QSI69H0P8T0NjP+2xeq0w3wgpkZNJdY41TaZdP+36+WB942eq\n1ZAAtvRBtZDxzNr6Fslu0h169JN2qmHm689Kc5AfSi4UO89i+qqAidD8YEvqTGnQ\n8RVT9iR6apKUkQK52R0+qkZoNq2bjGXe1oa7kQ8bPq6o/bn7gkhpXaDLHGGARHF1\nw7nDWfwYA7fMDN+5MW45r6k3WAujKVW3e7OLDnP6NNQ/JFL2NKdfSyzBZy0sUsxT\nddzatEUTa61RJGkW0v7wthXAFzztzCk+02eu3MF9GQKBgQDURhpA844nim+99Y+/\naM/kIcouBxDbn0AqJLgLImTbuhktOAbmrx8Nn2R/s3ojwtYQ5OtTP2k4NbE5tjGb\nICACHsj/iJyxvEvoE03+Ay21CwTe7Ncf+cHKueewbDSPgLm9XSZbQX1Qwpq7UYKp\nh5lFmldhLcDWci2G7ErZq4sklQKBgQC2oRTNpYeDwV9oFQyvcfwn13LqUmQAwD+5\nXi+v4p6/GRnWObdLasCao4V6iSia1+ccsUyNizkecBhJK2JCUzxvOYaL7I/wbwWB\n72LNCf/zPNxsEMOklVD7u6bxZ9REg/L2PuymdxYq9cZkB7zRmv9fXYXKkR1xFk64\nyIBxmKCxpQKBgCIadSNUPdVqb1NkfUiyLRwotZO5fOLb7fIXXh4j03JdrqfOJYWw\nQtvsbLf7fLb8GWozbP8948itD6EG/Wc/vQS6L26mYw5HAybw2wnhNtmsQIcUI+e2\nN4U7Yta8O6GGe9DJg10L43czHKrViJl1+JDvH/Sz5hRN2bSgh9H6tmsVAoGBAI00\nntEiW1UT/qCLJfPBPiXP/5oNeiTagGri2Bw2LGe1ELUCiyZUs/bc2CeWRT70EE2v\nCHGoY9GU+jIYyTBfCys0X0Nw9RoBvVBptwqx4KRBOmyTybFHggYhYULl9MnE++ZJ\nYNCU4x70SSCumt+16B3kQb4N1aXKibN101oBmL3BAoGAS08lrm/4U8940WjyqiwV\nB4Ji/QXriZqJGDWLFvKf7UkIMp/QoPhzNFCbj8Z9deh3C1pisIbeYT7wPz8T4W7y\nrlMBH79/9Aa13/unN992PLeWcicrIeMQ1S0WPzF4SBtNZu+gSQ9/+eu0Zf9Mxsav\n+N5w+nmVZMdbG23DKVMUv+o=\n-----END PRIVATE KEY-----\n",
        "client_email": "admob-140@admob-432400.iam.gserviceaccount.com",
        "client_id": "109297968801674725896",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/admob-140%40admob-432400.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }
    
    # Load credentials from JSON data
    credentials = service_account.Credentials.from_service_account_info(
        service_account_json
    )
    
    # Build the AdMob API service
    try:
        service = build('admob', 'v1', credentials=credentials)
        
        # Example API call - replace with actual call as needed
        account_id = '1669215305824306'  # Replace with your AdMob account ID
        response = service.accounts().list().execute()
        
        # Print response or process it as needed
        print(response)
    
    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()
