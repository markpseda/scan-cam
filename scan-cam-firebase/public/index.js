const firestore = firebase.firestore();
const storage = firebase.storage();
const settings = {/* your settings... */};
firestore.settings(settings);

$("#upload-data").click(function (event) {
    console.log("Made it here!");

    var licensePlateNum = $("#license-plate-upload").val();
    var gpsCoords = $("#gps-coords").val();
    var licensePlateImage = $("#license-plate-pic").prop('files');

    console.log("License Plate: " + licensePlateNum)
    console.log("GPS Coords: " + gpsCoords)
    console.log("Image: " + licensePlateImage)

    var timestamp = Date.now();

    // TODO: Upload file first, get a reference to add to firestore

    firestore.collection("uploads").add({
        timestamp : timestamp,
        license_number: licensePlateNum,
        gps_coords : gpsCoords,
        imageRef : "TBD"
    });

    var uploadsRef = firestore.collection('uploads');

    uploadsRef.orderBy('timestamp').onSnapshot(function(uploads){
        $("#table-of-uploads").empty();
        uploads.forEach(function(upload){
            var uploadData = upload.data();

            var date = new Date(uploadData.timestamp);

            $("#table-of-uploads").append('<tr><td id = "' + upload.id +'">' + uploadData.license_number + '</td><td>' + uploadData.gps_coords + '</td><td>' + date + '</td><td> something.jpg </td>');
        });
    });

});