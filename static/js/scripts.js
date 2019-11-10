function message(status, shake=false, id="") {
  if (shake) {
    $("#"+id).effect("shake", {direction: "right", times: 2, distance: 8}, 250);
  } 
  document.getElementById("feedback").innerHTML = status;
  $("#feedback").show().delay(2000).fadeOut();
}

function error(type) {
  $("."+type).css("border-color", "#E14448");
}

function processImage(response) {
  console.log("Hello Ravi World!!!");
  document.write("Hello Ravi World!!!");
  return ("Hello Ravi World!!!");
}




var login = function() {
  $.post({
    type: "POST",
    url: "/",
    data: {"username": $("#login-user").val(), 
           "password": $("#login-pass").val()},
    success(response){
      var status = JSON.parse(response)["status"];
      if (status === "Login successful") { location.reload(); }
      else { error("login-input"); }
    }
  });
};

$(document).ready(function() {
  
  $(document).on("click", "#login-button", login);
  $(document).keypress(function(e) {if(e.which === 13) {login();}});
  
  $(document).on("click", "#signup-button", function() {
    $.post({
      type: "POST",
      url: "/signup",
      data: {"username": $("#signup-user").val(), 
             "password": $("#signup-pass").val(), 
             "email": $("#signup-mail").val()},
      success(response) {
        var status = JSON.parse(response)["status"];
        if (status === "Signup successful") { location.reload(); }
        else { message(status, true, "signup-box"); }
      }
    });
  });

  $(document).on("click", "#save", function() {
    $.post({
      type: "POST",
      url: "/settings",
      data: {"username": $("#settings-user").val(), 
             "password": $("#settings-pass").val(), 
             "email": $("#settings-mail").val()},
      success(response){
        message(JSON.parse(response)["status"]);
      }
    });
  });

  $(document).on("click", "#save", function() {
    $.post({
      type: "POST",
      url: "/pneumonia",
      data: {"username": $("#pneumonia-user").val(), 
             "password": $("#pneumonia-pass").val(), 
             "email": $("#pneumonia-mail").val()},
      success(response){
        message(JSON.parse(response)["status"]);
      }
    });
  });
});

// Open or Close mobile & tablet menu
// https://github.com/jgthms/bulma/issues/856
$("#navbar-burger-id").click(function () {
  if($("#navbar-burger-id").hasClass("is-active")){
    $("#navbar-burger-id").removeClass("is-active");
    $("#navbar-menu-id").removeClass("is-active");
  }else {
    $("#navbar-burger-id").addClass("is-active");
    $("#navbar-menu-id").addClass("is-active");
  }
});


$("#file-picker").change(function(){

  var input = document.getElementById('file-picker');
  folder_set = false;
  for (var i=0; i<input.files.length; i++)
  {
  //koala.jpg, koala.JPG substring(index) lastIndexOf('a') koala.1.jpg
      var ext= input.files[i].name.substring(input.files[i].name.lastIndexOf('.')+1).toLowerCase()
      // alert('File Extension:' + ext);
      if ((ext == 'jpg') || (ext == 'png') || (ext == 'jpeg'))
      {
          $("#msg").text("Files are supported");
          if (folder_set == false) {
            folder_set = true;
            document.getElementById("upload").submit(); 
          }
      }
      else
      {
          $("#msg").text("Files are NOT supported")
          document.getElementById("file-picker").value ="";
      }

  }

} );

$("#tickerSelect").change(function(){
  var tickerValue = document.getElementById("tickerSelect").value;
  if (tickerValue === "NOT_SELECTED") {
    alert("Pick a Stock");
  } else {
    document.getElementById("tickerToPass").value = tickerValue;
    document.getElementById("upload").submit();
  }
});
