import os.path

import requests
import uvicorn
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from flask import Flask, request, jsonify
import telnyx
from time import sleep
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

SERVER_PORT = os.getenv("SERVER_PORT")
SERVER_HOST = os.getenv("SERVER_HOST")

telnyx.api_key = os.getenv("TELNYX_API_KEY")


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET")

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

GOOGLE_KEY = os.getenv("GOOGLE_API")

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
RANGE = 'Sheet1!A1:A1000000'

url = f'https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{RANGE}?key={GOOGLE_KEY}'

TEMPLATE_A = ("Please check your email inbox for how to SAVE  50% or more on your Fry-Oil costs with FRYLOW. No cost, "
              "No obligation trial. Thank you!\nReply OUT to end messages")

TEMPLATE_B = ("Calculate your Fry-Oil cost SAVINGS with FRYLOW. No cost, No obligation trial. Please check your email "
              "inbox. Thank you!\nReply OUT to end messages")

TEMPLATE_C = ("Want to SAVE 50% or more on fry-oil costs? Check your email for details on "
              "FRYLOW’s no-cost trial!\nReply OUT to end messages")

STOP_WORDS = [
    "OUT",
    "STOP",
    "STOP ALL",
    "UNSUBSCRIBE",
    "CANCEL",
    "END",
    "QUIT",
    "REMOVE",
    "DELETE",
    "UNSUB",
    "OPT OUT",
    "NO MORE",
    "DO NOT TEXT",
    "STOP MESSAGING",
    "PLEASE STOP",
    "ENOUGH",
    "BLOCK"
]


def set_up_credentials():
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())

    sheets = build("sheets", "v4", credentials=credentials).spreadsheets()
    return sheets



def contains_stop_word(text, stop_words):
    # Convert the text to lowercase to make the search case-insensitive
    text = text.lower()

    # Check if any stop word is in the text
    for stop_word in stop_words:
        # Ensure the stop word is treated as a full word/phrase
        if stop_word.lower() in text:
            return True

    return False


def send_message(to_phone, first_name, message):
    print("message sent")
    telnyx.Message.create(
        from_="+17785044277",
        to=to_phone,
        text=f"	Hi {first_name}. {message}"
    )


@app.route("/sfo_send_sms", methods=['POST'])
def send_sms():
    data = request.json
    sleep(5)
    template_uid = data.get("customer_template_uid")
    to_phone = data.get("company_phone_1")
    first_name = data.get("contact_fname")
    print(data)
    response = requests.get(url)
    if response.status_code == 200:
        spreadsheet = response.json().get('values', [])

        # Function to search for a company by name
        def search_phone(phone):
            for row in spreadsheet:
                if row[0].lower() == phone.lower().replace("+", ""):
                    return row

            # If no match found
            print(f"Phone '{phone}' not found.")
            return None

        # Example usage
        if search_phone(to_phone):
            return jsonify({"message": "This phone is forbidden to send sms"})
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return jsonify({"error": "request to spreadsheet failed"})

    if template_uid == "cm8769maegece":  # A
        send_message(to_phone, first_name, TEMPLATE_A)
    if template_uid == "nj218xbt5s0f3":  # B
        send_message(to_phone, first_name, TEMPLATE_B)
    if template_uid == "od234gkv5w69d":  # C
        send_message(to_phone, first_name, TEMPLATE_C)

    return jsonify({}), 200


@app.route('/webhooks', methods=['POST'])
def telnyx_webhooks():
    body = request.json
    print(body)
    return {}, 200

    text = body["data"]["payload"]["text"]
    phone = body["data"]["payload"]["from"]["phone_number"]
    if contains_stop_word(text, STOP_WORDS):
        value = {
            "values": [
                [phone]
            ]
        }
        sheets = set_up_credentials()
        response = sheets.values().append(spreadsheetId=SPREADSHEET_ID, range=RANGE, body=value,
                                       valueInputOption="USER_ENTERED").execute()
        return jsonify({"message": "phone was added to no contact list"}), 200
    return jsonify({"message": "ok"}), 200


if __name__ == '__main__':
    uvicorn.run(app=app, port=int(SERVER_PORT), host=SERVER_HOST)
