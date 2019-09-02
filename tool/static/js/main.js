
var index = 0;
// Recupera conjunto de imagens do Python
var images = imgs;
var labels = new Array(images.length).fill(42);

$("#next").on("click", function (e) {
  nextImage();
});

$("#prev").on("click", function (e) {
  previousImage();
});


$(window).bind('beforeunload', function () {
  $.ajax({
      type: 'POST',
      async: false,
      url: '/reload',
      data: {labels: labels}
  });
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
    index+=1;
    console.log(value); 
    if (index > images.length - 1) {
      index = 0;
      var data = {labels: labels};
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
