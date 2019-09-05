function init(){
  $.ajax({
      type: 'GET',
      url: '/getData',
      data: { entry2_id: 1, entry1_id: 2 },
      contentType: "application/json",
      async: false,
      success: function(data){
          index = 0;
          images = data.imgs;
          labels = new Array(images.length).fill([]);
          confidence_array = new Array(images.length).fill(0);
          document.getElementById('imgsrc').src = images[index];
        }
  });
}

init();


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
    index+=1;
    if (index > images.length - 1) {
      index = 0;
      $.ajax({
          type: 'POST',
          url: '/request_faces',
          data: JSON.stringify ({labels: labels, confidence: confidence_array}),
          contentType: "application/json",
          async: false,
          dataType: 'json',
          success: function(data){
            images = data.imgs;
            labels = new Array(images.length).fill([]);
            confidence_array = new Array(images.length).fill(0);
          }
      });
    }
  console.log(index)
  console.log(images)
  // Limpar as checkbox e radiobuttons da próxima imagem
  $('input:radio[name="confidenceLevelOptions"][value="3"]').click();
  $('input[type=checkbox]').prop('checked',false);
  document.getElementById('imgsrc').src = images[index];
  
}

