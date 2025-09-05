import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

def firebase_auth():
    import firebase_admin
    from firebase_admin import firestore
    from firebase_admin import credentials

    #update below to say r"\path\to\file.json"

    cred = credentials.Certificate(r"/Users/quinndoyle/CS3050/CS-3050-Warmup-Project/DO-NOT-ADD-TO-GIT")
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    #testing

    data = {
        'name': 'Hailey Schoppe',
        'status': 'hungry'
    }
    doc_ref = db.collection("users").document("hschoppe")
    doc_ref.set(data)

    print('Document ID:', doc_ref.id)

firebase_auth()