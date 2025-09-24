import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

#Function connects and authorizes the user to Firebase Firestore using JSON authentication file
def firebase_auth():

    #update below to say r"\path\to\file.json"
    if (not firebase_admin._apps):
        cred = credentials.Certificate(r"INSERT PATH TO JSON FILE")
        firebase_admin.initialize_app(cred)

    db = firestore.client()

    #Returns the client connection to the database
    return db


firebase_auth()
