import requests
import os
import base64
from datetime import datetime, timedelta
from dotenv import find_dotenv, load_dotenv

class Payment:
    _access_token = None
    _token_expiry = None

    @staticmethod
    def _get_credentials():
        dotenv_path = find_dotenv()
        load_dotenv(dotenv_path)
        return os.getenv("consumer_key"), os.getenv("consumer_secret")

    @classmethod
    def get_token(cls):
        """Returns a cached access token or fetches a new one."""

        if cls._access_token and cls._token_expiry and datetime.now() < cls._token_expiry:
            return cls._access_token
 
        consumer_key, consumer_secret = cls._get_credentials()

        credentials = f"{consumer_key}:{consumer_secret}"
        credentials = base64.b64encode(credentials.encode("utf-8"))
        url = "https://sandbox.safaricom.co.ke/oauth/v1/generate"
        querystring = {"grant_type":"client_credentials"}
        payload = ""
        headers = {
            "Authorization": f"Basic {credentials.decode('utf-8')}"
        }
        response = requests.get(url, headers=headers, params=querystring)
        response_data = response.json()

        if response.status_code == 200 and "access_token" in response_data:
            cls._access_token = response_data["access_token"]
            cls._token_expiry = datetime.now() + timedelta(seconds=int(response_data.get("expires_in", 3599)))
            return cls._access_token
        else:
            raise Exception("Failed to get access token: " + response.text)
        
    @classmethod
    def stk_push(cls, phone_number, amount):
        access_token = cls.get_token()

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        dotenv_path = find_dotenv()
        load_dotenv(dotenv_path)

        business_short_code = os.getenv("shortcode")
        passkey = os.getenv("passkey")
        callback_url = os.getenv("callback_url")
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

        # Password is base64 encoded: shortcode + passkey + timestamp
        password_str = f"{business_short_code}{passkey}{timestamp}"
        password = base64.b64encode(password_str.encode()).decode()

        payload = {
            "BusinessShortCode": business_short_code,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": business_short_code,
            "PhoneNumber": phone_number,
            "CallBackURL": callback_url,
            "AccountReference": "Hiring Platform",
            "TransactionDesc": "Payment for service"
        }

        response = requests.post(url, headers=headers, json=payload)
        print("STK Response:", response.status_code, response.text)

