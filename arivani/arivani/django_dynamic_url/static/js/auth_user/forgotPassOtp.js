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
  otp
$('body').on('click','#submit',function(){
    var otp = $('#otp').val()
    validate(otp)
})
function validate(otp){
    if (otp==""){
        Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "otp can't be empty",
          });
    }
    else{
        get_val(otp)
    }
}
function get_val(otp){
    var data ={
        otp:otp
    }
    fetch(
        forgotPassOtpVerify,{
            method:'POST',
            credentials:'same-origin',
            headers:{
                'X-Requested-With':'XMLHttpRequest',
                'X-CSRFToken':getCookie("csrftoken")
            },
            body:JSON.stringify({payload:data})
        }
    ).then(response=>response.json())
    .then(data=>{
        if (data.status==200){
            //send it to change password page
            window.location.href=changePasswordPage
        }
        else if(data.status==400){
            Swal.fire({
                icon: "error",
                title: "Oops...",
                text: "user not found!",
              });
        }
        else if(data.status==404){
            Swal.fire({
                icon: "error",
                title: "Oops...",
                text: "wrong otp",
              });
        }
    })
}