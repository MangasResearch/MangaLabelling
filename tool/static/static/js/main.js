
var index = 0;
// Recupera conjunto de imagens do Python
var images = imgs;
var labels = new Array(images.length).fill(0);
var marked =  new Array(images.length).fill(0);


$("#next").on("click", function (e) {
  nextImage();
});

$("#prev").on("click", function (e) {
  previousImage();
});

// var next = document.getElementById('next');
// var previous = document.getElementById('prev');
// //'Previous' button
// previous.addEventListener('click', previousImage);
// //'Next' button
// next.addEventListener('click', nextImage);


document.getElementById('imgsrc').src = images[index]; 


function previousImage(){
    index-=1;
    if (index < 0) {
      index = 0; // images.length - 1;
    }
    document.getElementById('imgsrc').src = images[index];
}

function nextImage() {
    var value = document.querySelector('input[name="expressionRadios"]:checked').value;
    labels[index] = value;
    marked[index] = 1;
    index+=1;
    console.log(value); 
    if (index > images.length - 1) {
      index = 0;
      var data = {labels: labels, marked: marked};
      post("/request_faces", data, method='post');
    }
  document.getElementById('imgsrc').src = images[index];
}


// Detecta quando o usuário entra na página
window.onload = function() {
  console.log("EVENTS - ENTROU NA PÁGINA !!!");
}


$(function () {
  //getting click event to show modal
    $('#help-button').click(function () {
        $('#helpModal').modal();
      //appending modal background inside the bigform-content
        $('.modal-backdrop').appendTo('.faces-content');
    });

});


$(function () {
  //getting click event to show modal
    $('#help-button').click(function () {
        $('#helpModal').modal();
      //appending modal background inside the bigform-content
        $('.modal-backdrop').appendTo('.faces-content');
    });

});


// Detecta quando o usuário sai da página
// $(window).bind("beforeunload",function(event) {
//   $.post("/reload", {data: "EVENTS - BEFORE UNLOAD!",labels: labels, marked: marked});
//   return "";
// });



/**
 * sends a request to the specified url from a form. this will change the window location.
 * @param {string} path the path to send the post request to
 * @param {object} params the paramiters to add to the url
 * @param {string} [method=post] the method to use on the form
 */

function post(path, params, method='post') {

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    const form = document.createElement('form');
    form.method = method;
    form.action = path;
  
    for (const key in params) {
      if (params.hasOwnProperty(key)) {
        const hiddenField = document.createElement('input');
        hiddenField.type = 'hidden';
        hiddenField.name = key;
        hiddenField.value = params[key];
  
        form.appendChild(hiddenField);
      }
    }
  
    document.body.appendChild(form);
    form.submit();
  }


// window.addEventListener('beforeunload', function (e) { 
//     e.preventDefault(); 
//     console.log(labels)
//     $.post("/reload", {data: "BEFORE UNLOAD!",labels: labels})
//     e.returnValue = ''; 
// });

// $(window).bind('beforeunload',function(){

//   //save info somewhere
//   $.post("/reload", {data: "EVENTS - REALOAD EVENT!",labels: labels, marked: marked});

//   return 'are you sure you want to leave?';

// });