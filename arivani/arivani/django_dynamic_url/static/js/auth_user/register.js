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
$('body').on('click','#register',function(){
   var userName = $('#userName').val()
   var userEmail = $('#userEmail').val()
   var userPass1 = $('#userPass1').val()
   var userPass2 = $('#userPass2').val()
   var role = $('#role').val()
   validate(userName, userEmail, userPass1, userPass2, role)
})
function validate(userName, userEmail, userPass1, userPass2, role){
    if (userName==""|| userEmail==""|| userPass1==""|| userPass2==""|| role=="Select"){
        Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "Input fields can't be empty!",
          });
    }
    else if(userPass1 != userPass2){
        Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "Password don't match!",
          });
    }
    else{
        get_value(userName, userEmail, userPass1, userPass2, role)
    }
}
function get_value(userName, userEmail, userPass1, userPass2, role){
    var data={
        username:userName, 
        email:userEmail, 
        password1:userPass1, 
        password2:userPass2, 
        role:role
    }
    fetch(register,{
        method:'POST',
        credentials:'same-origin',
        headers:{
            'X-Requested-With':'XMLHttpRequest',
            'X-CSRFToken':getCookie("csrftoken")
        },
        body:JSON.stringify({payload:data})
    }).then(response=>response.json())
    .then(data => {
        if(data.status==200){
            window.location.href=registerOtpPage
        }
    })
}