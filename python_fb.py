from google.cloud import firestore
from google.cloud import storage

import google.oauth2.credentials

storage_client = storage.Client.from_service_account_json('service_account.json')

    
db = firestore.Client.from_service_account_json('service_account.json')

doc_ref = db.collection(u'uploads')

docs = doc_ref.get()

for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))

buckets = list(storage_client.list_buckets())

print(buckets)