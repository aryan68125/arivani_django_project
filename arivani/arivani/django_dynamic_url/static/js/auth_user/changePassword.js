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
$('body').on('click','#change_pass',function(){
    var pass1 = $('#pass1').val()
    var pass2 = $('#pass2').val()
    validate(pass1,pass2)
})
function validate(pass1,pass2){
    if(pass1==""||pass2==""){
        Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "passsword can't be empty",
          });
    }
    else if(pass1!=pass2){
        Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "Passwords don't match",
          });
    }
    else{
        set_pass(pass1,pass2)
    }
}
function set_pass(pass1,pass2){
    var data={
        password:pass1
    }
    fetch(
        changePassword,{
            method:'POST',
            credentials:'same-origin',
            headers:{
                'X-Requested-With':'XMLHttpRequest',
                'X-CSRFToken':getCookie('csrftoken')
            },
            body:JSON.stringify({payload:data})
        }
    ).then(response=>response.json())
    .then(data=>{
        if (data.status==200){
            //send user to the login page
            window.location.href=loginPage
        }
        else if(data.status==404){
            Swal.fire({
                icon: "error",
                title: "Oops...",
                text: "User does not exist",
              });
        }
    })
}