const firestore = firebase.firestore();
const storage = firebase.storage();
const settings = {/* your settings... */};
firestore.settings(settings);

// Create a storage reference from our storage service
var storageRef = storage.ref();

// Create reference to uploads collection
var uploadsRef = firestore.collection('uploads');


$("#upload-data").click(function (event) {
    console.log("Made it here!");

    var licensePlateNum = $("#license-plate-upload").val();
    var gpsCoords = $("#gps-coords").val();
    var licensePlateImage = $("#license-plate-pic").prop('files')[0];

    console.log("License Plate: " + licensePlateNum)
    console.log("GPS Coords: " + gpsCoords)
    console.log("Image: " + licensePlateImage)

    var timestamp = Date.now();

    var imageRef = licensePlateNum + gpsCoords + timestamp

    firestore.collection("uploads").add({
        timestamp : timestamp,
        license_number: licensePlateNum,
        gps_coords : gpsCoords,
        imageRef : imageRef

    });
    imageReff = storageRef.child(imageRef + '.jpg');
    imageReff.put(licensePlateImage).then(function(snapshot){
        // the initial load image will fail because of asyncronous-ness. Add the source link after the file is added to storage
        imageReff.getDownloadURL().then(function(url)
        {
          $('#' + imageRef.split(' ').join('').split(',').join('').split('.').join('')).attr("src", url);
        });
        
    });
});

uploadsRef.orderBy('timestamp').onSnapshot(function(uploads){
    $("#table-of-uploads").empty();
    uploads.forEach(function(upload){
        var uploadData = upload.data();

        var date = new Date(uploadData.timestamp);

        var imgRef = storageRef.child(uploadData.imageRef + '.jpg');

        var imgURL = "";

        $("#table-of-uploads").append('<tr id = "' + upload.id +'"><td>' + uploadData.license_number + '</td><td>' + uploadData.gps_coords + '</td><td>' + date + '</td><td> <img id="' + uploadData.imageRef.split(' ').join('').split(',').join('').split('.').join('') + '" src="' + imgURL + '" height = "100" width = "200"/></td><td> <button id="'+ upload.id + '_delete">Delete</button> </td></tr>');

        $("#" + upload.id + "_delete").click(function (event) {
          console.log("Doing a thing to delete!!!" + upload.id);
          uploadsRef.doc(upload.id).delete().then(function(){
            console.log("Deleted document succesfully!")
          });
        });




        imgRef.getDownloadURL().then(function(url)
        {
            imgURL = url;
            console.log("Found image in storage");
            console.log(uploadData.imageRef.split(' ').join(''));
            console.log(imgURL);

            $('#' + uploadData.imageRef.split(' ').join('').split(',').join('').split('.').join('')).attr("src", imgURL);
        }).catch(function(error) {
          console.log("Some kinda storage error!");
            switch (error.code) {
              case 'storage/object-not-found':
                // File doesn't exist
                break;
          
              case 'storage/unauthorized':
                // User doesn't have permission to access the object
                break;
          
              case 'storage/canceled':
                // User canceled the upload
                break;
              case 'storage/unknown':
                // Unknown error occurred, inspect the server response
                break;
            }
        });
    });
});