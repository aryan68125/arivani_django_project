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
$('body').ready(function(){
  disable_input_fields()
})
function disable_input_fields(){
  $('#hrID').prop('disabled', true);
  $('#username').prop('disabled', true);
  $('#first_name').prop('disabled', true);
  $('#last_name').prop('disabled', true);
  $('#email').prop('disabled', true);
  $('#select_employee').prop('disabled', true);
}