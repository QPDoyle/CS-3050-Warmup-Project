import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

def firebase_auth():

    #update below to say r"\path\to\file.json"
    if (not firebase_admin._apps):
        cred = credentials.Certificate(r"C:\Users\darkf\Downloads\cs3050-warmup-baf96-firebase-adminsdk-fbsvc-470d196a80.json")
        firebase_admin.initialize_app(cred)

    db = firestore.client()

    return db


firebase_auth()
