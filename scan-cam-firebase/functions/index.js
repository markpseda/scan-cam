const functions = require('firebase-functions');

// The Firebase Admin SDK to access the Firebase Realtime Database.
const admin = require('firebase-admin');

const formidable = require('formidable');
const util = require('util');

admin.initializeApp();

// // Create and Deploy Your First Cloud Functions
// // https://firebase.google.com/docs/functions/write-firebase-functions

// Take the text parameter passed to this HTTP endpoint and insert it into the
// Realtime Database under the path /messages/:pushId/original


exports.uploadData = functions.https.onRequest(async (req, res) => {
    console.log("Beggining Method");

    if (req.method != "POST")
    {
        res.status(400).send("Should be a POST request at this URL.");
        return
    }
    console.log("It is a post");

    var form = new formidable.IncomingForm();



    form.parse(req, function(err, fields, files) {
      console.log("We in here");
      res.writeHead(200, {'content-type': 'text/plain'});
      res.write('received upload:\n\n');
      res.end(util.inspect({fields: fields, files: files}));
      console.log(util.inspect({fields: fields, files: files}));

      //res.send();

    });

    console.log("I am there.");
    /*
    // Grab the text parameters.
    const timestamp = req.query.timestamp;
    const license_number = req.query.license_number;
    const gps_coords = req.query.gps_coords;
    const imageRef = license_number + gps_coords;

    file = req.files;
    console.log("File content:");
    console.log(file);
    console.log("this is a test")
    // upload file to storage first, then update the database

    //await functions.storage.upload(file, {destination:imageRef + '.jpg'}).then(() => {
        // Push the new data into firestore.
        
   // });

    const snapshot = await admin.firestore().collection('uploads').add({
        timestamp : timestamp,
        license_number: license_number,
        gps_coords : gps_coords,
        imageRef : imageRef
    });

    */
    // Respond with sucess...
    //res.status(201).send("Successfully added new item to database.");


});