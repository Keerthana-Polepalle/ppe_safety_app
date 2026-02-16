const backend = "http://127.0.0.1:5000";

let imageInput = document.getElementById("imageInput");
let preview = document.getElementById("preview");

let video = document.getElementById("webcam");
let capturedImg = document.getElementById("capturedImage");

let stream = null;
let capturedBlob = null;

// =======================
// Upload Preview
// =======================

imageInput.onchange = () => {
preview.src = URL.createObjectURL(imageInput.files[0]);
};

// =======================
// Detect Uploaded Image
// =======================

async function detectImage() {

let file = imageInput.files[0];
if (!file) return alert("Choose image!");

let formData = new FormData();
formData.append("file", file);

let res = await fetch(backend + "/detect", {
method:"POST",
body:formData
});

let blob = await res.blob();
document.getElementById("uploadResult").src =
URL.createObjectURL(blob);
}

// =======================
// Start Webcam
// =======================

async function startWebcam() {

if (stream) return;

stream = await navigator.mediaDevices.getUserMedia({video:true});
video.srcObject = stream;
}

// =======================
// Capture Photo
// =======================

function capturePhoto() {

if (!stream) return alert("Start webcam first!");

let canvas = document.createElement("canvas");
canvas.width = video.videoWidth;
canvas.height = video.videoHeight;

let ctx = canvas.getContext("2d");
ctx.drawImage(video,0,0);

canvas.toBlob(blob => {

capturedBlob = blob;
capturedImg.src = URL.createObjectURL(blob);

});

// stop webcam
stream.getTracks().forEach(track => track.stop());
video.srcObject = null;
stream = null;
}

// =======================
// Detect Captured Image
// =======================

async function detectCaptured() {

if (!capturedBlob) return alert("Capture photo first!");

let formData = new FormData();
formData.append("file", capturedBlob);

let res = await fetch(backend + "/detect", {
method:"POST",
body:formData
});

let blob = await res.blob();

document.getElementById("webcamResult").src =
URL.createObjectURL(blob);
}
