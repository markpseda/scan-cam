from google.cloud import firestore
from google.cloud import storage

import google.oauth2.credentials

# Really bad practice here, but this lets us access the services we need
storage_client = storage.Client.from_service_account_json('service_account.json')
db = firestore.Client.from_service_account_json('service_account.json')






doc_ref = db.collection(u'uploads')

new_doc = doc_ref.document()

timestamp = '3425125'
gps_coords = '23.2, 32.1'
license_number = '233422A4'
imageRef = license_number + gps_coords


# just the default top level bucket
bucket = storage_client.get_bucket('ud-senior-design-2018-scan-cam.appspot.com')

blob = bucket.blob(imageRef + '.jpg')

blob.upload_from_filename('LTM378.jpg')


# This uploads the document
new_doc.set({
    u'timestamp' : timestamp,
    u'gps_coords' : gps_coords,
    u'imageRef' : imageRef,
    u'license_number' : license_number
})

