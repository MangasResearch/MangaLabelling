
var index = 0;
// Recupera conjunto de imagens do Python
var images = imgs;
var labels = new Array(images.length).fill([]);
var confidence_array = new Array(images.length).fill(0);

$("#next").on("click", function (e) {
  nextImage();
});

$("#prev").on("click", function (e) {
  previousImage();
});


$(window).bind('beforeunload', function () {
  $.ajax({
    type: 'POST',
    url: '/reload',
    data: JSON.stringify ({labels: labels, confidence: confidence_array}),
    contentType: "application/json",
    dataType: 'json'
});
});

document.getElementById('imgsrc').src = images[index]; 


function previousImage(){
    index-=1;
    if (index < 0) {
      index = 0; // images.length - 1;
    }
    document.getElementById('imgsrc').src = images[index];
}

function nextImage() {
    confidence_level = $('input[name=confidenceLevelOptions]:checked', '#confidenceLevel').val()
    selected = new Array();
    $("input:checkbox[name=expressionCheckboxs]:checked").each(function(){
      selected.push($(this).val());
    });    
    labels[index] = selected;
    confidence_array[index] = confidence_level;
    console.log(labels); 
    index+=1;
    if (index > images.length - 1) {
      index = 0;
      $.ajax({
          type: 'POST',
          url: '/request_faces',
          data: JSON.stringify ({labels: labels, confidence: confidence_array}),
          contentType: "application/json",
          dataType: 'json'
      });
    }
  // Limpar as checkbox e radiobuttons da próxima imagem
  $('input:radio[name="confidenceLevelOptions"][value="3"]').click();
  $('input[type=checkbox]').prop('checked',false);
  document.getElementById('imgsrc').src = images[index];
}


// Detecta quando o usuário entra na página
window.onload = function() {
  console.log("EVENTS - ENTROU NA PÁGINA !!!");
}