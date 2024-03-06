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
$('body').on('click','#resetPass',function(){
    var password1 = $('#password1').val()
    var password2 = $('#password2').val()
    data = {
        password1:password1,
        password2:password2,
    }
    validate(data)
})
function validate(data){
    if((data.password1 == "" || data.password2=="")){
        Swal.fire({
            icon: "error",
            title: "Error...",
            text: "password needed!",
          });
    }
    else{
        if(data.password1 == data.password2){
            send_data(data)
        }
        else{
            Swal.fire({
                icon: "error",
                title: "Error...",
                text: "password din't match!",
              });
        }
    }
}
function send_data(data){
    fetch(
        resetPassword_pass,{
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
                title: "Password reset successful",
                showConfirmButton: false,
                timer: 1500,
                location:window.location.href=loginUserPage
              });
              //send user to the login page
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