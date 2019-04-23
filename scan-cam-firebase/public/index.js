const firestore = firebase.firestore();
const storage = firebase.storage();
const settings = {/* your settings... */};
firestore.settings(settings);

// Create a storage reference from our storage service
var storageRef = storage.ref();


// Create reference to uploads collection
var uploadsRef = firestore.collection('uploads');


// Update table once on page load
uploadsRef.get().then(function(uploads) {
  console.log("Should only happen once");
  $("#table-of-uploads").empty();
    uploads.forEach(function(upload){
        var uploadData = upload.data();

        var date = new Date(uploadData.timestamp);

        var imgRef = storageRef.child(uploadData.imageRef + '.jpg');

        var imgURL = null;

        $("#table-of-uploads").append('<tr><td id = "' + upload.id +'">' + uploadData.license_number + '</td><td>' + uploadData.gps_coords + '</td><td>' + date + '</td><td> <img id="' + uploadData.imageRef + '" src="' + imgURL + '" height = "100" width = "200"/></td>');

        imgRef.getDownloadURL().then(function(url)
        {
            imgURL = url;
            console.log("Found image in storage");
            console.log(uploadData.imageRef);
            console.log(imgURL);
            $('#' + uploadData.imageRef).attr("src", imgURL);
        }).catch(function(error) {
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




$("#upload-data").click(function (event) {
    console.log("Made it here!");

    var licensePlateNum = $("#license-plate-upload").val();
    var gpsCoords = $("#gps-coords").val();
    var licensePlateImage = $("#license-plate-pic").prop('files')[0];

    console.log("License Plate: " + licensePlateNum)
    console.log("GPS Coords: " + gpsCoords)
    console.log("Image: " + licensePlateImage)


    var timestamp = Date.now();

    var imageRef = licensePlateNum + gpsCoords

    // TODO: Upload file first, get a reference to add to firestore

    firestore.collection("uploads").add({
        timestamp : timestamp,
        license_number: licensePlateNum,
        gps_coords : gpsCoords,
        imageRef : imageRef

    });

    imageReff = storageRef.child(imageRef + '.jpg');

    imageReff.put(licensePlateImage).then(function(snapshot){
        console.log("Did a thing!");
    });




});


uploadsRef.orderBy('timestamp').onSnapshot(function(uploads){
    $("#table-of-uploads").empty();
    uploads.forEach(function(upload){
        console.log("Should only happen once per upload.");
        var uploadData = upload.data();

        var date = new Date(uploadData.timestamp);

        var imgRef = storageRef.child(uploadData.imageRef + '.jpg');

        var imgURL = null;

        $("#table-of-uploads").append('<tr><td id = "' + upload.id +'">' + uploadData.license_number + '</td><td>' + uploadData.gps_coords + '</td><td>' + date + '</td><td> <img id="' + uploadData.imageRef + '" src="' + imgURL + '" height = "100" width = "200"/></td>');

        imgRef.getDownloadURL().then(function(url)
        {
            imgURL = url;
            console.log("Found image in storage");
            $('#' + uploadData.imageRef).attr("src", imgURL);
        }).catch(function(error) {
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