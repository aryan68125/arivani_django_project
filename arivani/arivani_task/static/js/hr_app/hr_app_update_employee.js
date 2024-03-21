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
    get_all_employee_created_by_hr()
})
function get_all_employee_created_by_hr(){
    fetch(
        hr_app_update_get_all_employee_url,{
            method:'POST',
            credentials:'same-origin',
            headers:{
                'X-Requested-With':'XMLHttpRequest',
                'X-CSRFToken':getCookie("csrftoken"),
            }
        }
    ).then(response=>response.json())
    .then(data=>{
        if(data.status==200){
            console.log(data)
            $('#table_data_employee').empty()
        }
        else{

        }
    })
}
function create_employee_table(){
     $('#table_data_employee').append(`
         
     `)
}