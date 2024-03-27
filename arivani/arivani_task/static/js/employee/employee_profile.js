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
$('body').ready(function(){
  disable_input_fields()
})
function disable_input_fields(){
  $('#employeeID').prop('disabled', true);
}
$('body').on('click','#save_button',function(){
  var employeeID = $('#employeeID').val()
  var username = $('#username').val()
  var first_name = $('#first_name').val()
  var last_name = $('#last_name').val()
  var email = $('#email').val()
  var data = {
    employeeID:employeeID,
    username:username,
    first_name:first_name,
    last_name:last_name,
    email:email,
  }
  validate(data)
})
function validate(data){
  if (data.username == "" || data.first_name == "" || data.last_name == "" || data.email==""){
    Swal.fire({
      icon: "error",
      title: "Error...",
      text: "Input Fields can't be empty",
    });
  }
  else{
    if(!isValidEmail(data.email)){
      Swal.fire({
        icon: "error",
        title: "Error...",
        text: "Email not valid",
      });
    }
    else{
      send_data(data)
    }
  }
}
function send_data(data){
  fetch(
    employee_app_update_employee_profile_url,{
      method:'POST',
      credentials:'same-origin',
      headers:{
        'X-Requested-With':'XMLHttpRequest',
        'X-CSRFToken':getCookie("csrftoken"),
      },
      body:JSON.stringify({payload:data})
    }
  ).then(response=>response.json())
  .then(data=>{
    if(data.status==200){
      Swal.fire({
        position: "top-end",
        icon: "success",
        title: "Hr Profile Updated",
        showConfirmButton: false,
        timer: 1500
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