from google.cloud import firestore
from google.cloud import storage

import google.oauth2.credentials

storage_client = storage.Client.from_service_account_json('service_account.json')

    
db = firestore.Client.from_service_account_json('service_account.json')

doc_ref = db.collection(u'uploads')

new_doc = doc_ref.document()

timestamp = '12345'
gps_coords = '23.2, 32.1'
license_number = '2342A4'
imageRef = license_number + gps_coords


new_doc.set({
    u'timestamp' : timestamp,
    u'gps_coords' : gps_coords,
    u'imageRef' : imageRef,
    u'license_number' : license_number
})

buckets = list(storage_client.list_buckets())

print(buckets)