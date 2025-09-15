import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

def firebase_auth():

    #update below to say r"\path\to\file.json"
    if (not firebase_admin._apps):
        cred = credentials.Certificate(r"C:\Users\beemi\PycharmProjects\CS-3050-Warmup-Project\DO_NOT_PUSH\cs3050-warmup-baf96-firebase-adminsdk-fbsvc-941113e51b.json")
        firebase_admin.initialize_app(cred)

    db = firestore.client()
    print("Firestore initialized")

    return db


firebase_auth()