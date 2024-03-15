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

$('body').on('click','#signin',function(){
    var username = $('#username').val()
    var password = $('#password1').val()
    data ={
        username:username,
        password:password
    }
    validate(data)
})
function validate(data){
    console.log("sign in")
 if(data.username == "" || data.password==""){
    Swal.fire({
        icon: "error",
        title: "Error...",
        text: "Input fields can't b empty!",
      });
 }   
 else{
    send_data(data)
 }
}
function send_data(data){
    fetch(
        loginUser,{
            method:'POST',
            credentials:'same-origin',
            headers:{
                'X-Requested-With':'XMLHttpRequest',
                'X-CSRFToken':getCookie("csrftoken")
            },
            body:JSON.stringify({payload:data}),
    }
    ).then(response=>response.json())
    .then(data=>{
        if(data.status==200){
          
          Swal.fire({
            position: "top-end",
            icon: "success",
            title: "User Login Successful",
            showConfirmButton: false,
            timer: 1500,
        }).then((result) => {
            // Redirect the user to the dashboard page
            if (data.is_superuser==1){
              window.location.href = dashboard_admin;
            }
            else{
              window.location.href = dashboard_home;
            }
        });
              //send user to home page
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