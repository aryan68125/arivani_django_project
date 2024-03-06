
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
function isValidEmail(email) {
    // Regular expression for email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    // Test the email against the regex pattern
    return emailRegex.test(email);
} 
$('body').on('click','#signup',function(){
    var username = $('#username').val()
    var email = $('#email').val()
    var password1 = $('#password1').val()
    var password2 = $('#password2').val()
    var role = $('#role').val()
    data = {
        username:username,
        email:email,
        password1:password1,
        password2:password2,
        role:role
    }
    Validate_form(data)
})
function Validate_form(data){
    if (data.username == "" || data.email == "" || data.password1=="" || data.password2==""){
        Swal.fire({
            icon: "error",
            title: "Error...",
            text: "Input fields can't b empty!",
          });
    }
    else if(data.password1 != data.password2){
        Swal.fire({
            icon: "error",
            title: "Error...",
            text: "Passwords do not match!",
          });
    }
    else if(!isValidEmail(data.email)){
        Swal.fire({
            icon: "error",
            title: "Error...",
            text: "Email not valid!",
          });
    }
    else{
        send_data(data)
    }
}

function send_data(data){
    fetch(
        registerUser,{
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
            Swal.fire({
              position: "top-end",
              icon: "success",
              title: "Your account has been created",
              showConfirmButton: false,
              timer: 1500
            });
            window.location.href=registerVerifyOtpPage
        }
        else if (data.status==500){
            Swal.fire({
                icon: "error",
                title: "Error...",
                text: data.error,
              });
        }
    })
}