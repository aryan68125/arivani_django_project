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
$('body').on('click','#verifyotp',function(){
    var otp = $('#otp').val()
    data={
        'otp':otp
    }
    validate(data)
})
function validate(data){
    if(data.otp == ""){
        Swal.fire({
            icon: "error",
            title: "Error...",
            text: "Fields can't be empty",
          });
    }
    else{
        send_data(data)
    }
}
function send_data(data){
    console.log(data)
    fetch(
        verifyOtpRegisterUser,{
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
        if(data.status==200){
            Swal.fire({
                position: "top-end",
                icon: "success",
                title: "Your otp is verified",
                showConfirmButton: false,
                timer: 1500
              });
              //send user to the login page
              window.location.href=loginUserPage_url
        }
        else if(data.status==404){
            Swal.fire({
                icon: "error",
                title: "Error...",
                text: data.error,
              });
        }
        else if(data.status==400){
            Swal.fire({
                icon: "error",
                title: "Error...",
                text: data.error,
              });
        }
        else{
            Swal.fire({
                icon: "error",
                title: "Error...",
                text: data.error,
              });
        }
    })
}
$('body').on('click','#resendOtp_anchor',function(){
    resendOtp()
})
function resendOtp(){
    console.log("resend otp")
    fetch(
        resendOtp_url,{
            method:'POST',
            credentials:'same-origin',
            headers:{
                'X-Requested-With':'XMLHttpRequest',
                'X-CSRFToken':getCookie("csrftoken")
            }
        }
    ).then(response=>response.json())
    .then(data=>{
        if(data.status==200){
            Swal.fire({
                position: "top-end",
                icon: "success",
                title: "Otp Sent!",
                showConfirmButton: false,
                timer: 1500
              });
        }
    })
}