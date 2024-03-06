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
$('body').on('click','#verify_email',function(){
var username = $('#username').val()
var data = {
username : username
}
validate(data)
})
function validate(data){
    if (data.username==""){
        Swal.fire({
            icon: "error",
            title: "Error...",
            text: "Username needed!",
          });
    }
    else
    {
        send_data(data)
    }
}
function send_data(data){
    fetch(
        sendVerificationUrl,{
            method:'POST',
            credentials:"same-origin",
            headers:{
                "X-Requested-With":"XMLHttpRequest",
                "X-CSRFToken":getCookie("csrftoken")
            },
            body:JSON.stringify({payload:data})
        }
    ).then(response=>response.json())
    .then(data=>{
        if(data.status==200){
            Swal.fire({
                position: "top-end",
                icon: "success",
                title: "Password reset link sent to you mail",
                showConfirmButton: false,
                timer: 1500,
                location:window.location.href=loginUserPage
              });
            //   send user to the login page
              // window.location.href=loginUserPage
        }
        else if(data.status==404){
            Swal.fire({
                icon: "error",
                title: "Error...",
                text: data.error,
              }); 
        }
        else{
            Swal.fire({
                icon: "error",
                title: "Oops...",
                text: "Something went wrong!",
              });
        }
    })
}