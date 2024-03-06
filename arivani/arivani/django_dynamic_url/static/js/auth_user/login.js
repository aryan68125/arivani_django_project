function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  $('body').on('click','#login',function(){
    var pass = $('#pass').val()
    var username = $('#username').val()
    validate(pass,username)
  })
  function validate(pass,username){
    if(pass=="" || username==""){
        Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "either password or username is empty",
          });
    }
    else{
        get_val(pass,username)
    }
  }
  function get_val(pass,username){
    var data = {
        username:username,
        password:pass
    }
    fetch(loginUser,{
        method:'POST',
        credentials:'same-origin',
        headers:{
            'X-Requested-With':'XMLHttpRequest',
            'X-CSRFToken':getCookie("csrftoken")
        },
        body:JSON.stringify({payload:data})
    }).then(response=>response.json())
    .then(data=>{
        if(data.status==200){
            window.location.href=home
        }
        else if(data.status==404){
            Swal.fire({
                icon: "error",
                title: "Oops...",
                text: "either username or password is wrong",
              });
        }
    })
  }

//forgot password code
$('body').on('click','#forgotpass',function(){
  var username = $('#username').val()
  validateUsername(username)
})
function validateUsername(username){
  if (username==""){
    Swal.fire({
      icon: "error",
      title: "Oops...",
      text: "USername can't be empty",
    });
  }
  else{
    send_username(username)
  }
}
function send_username(username){
  window.location.href=`forgotPassOtpPage/${username}`
}