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
    get_all_hr()
    get_all_employee()
})
function get_all_hr(){
    fetch(
        manager_app_update_get_all_hr_url,{
            method:'POST',
            credentials:'same-origin',
            headers:{
                'X-Requested-With':'XMLHttpRequest',
                'X-CSRFToken': getCookie("csrftoken"),
            }
        }
    ).then(response=>response.json())
    .then(data=>{
        if(data.status==200){
            //useID
            // userID = data.context.employee_list[0].userID
            // console.log(userID)
            //username
            // username = data.context.employee_list[0].user.username
            // console.log(username)
            var hr_count = 0;
            for(var i=0;i<data.context.employee_list.length;i++){
                //userID
                userID = data.context.employee_list[i].userID
                //username
                username = data.context.employee_list[i].user.username
                //usernamePK
                userpk = data.context.employee_list[i].user.id
                create_hr_table(userpk,userID,username,i)
                hr_count++;
            }
            $('#hr_count').text(hr_count)
        }
        else{

        }
    })
}
function create_hr_table(userPk,userID,username,i){
    $('#table_data_hr').append(`
    <tr>
    <th scope="row">${i+1}</th>
    <th scope="row" style="display:none">${userPk}</th>                    
    <th scope="row" style="display:none">${userID}</th>
    <td>${userID}</td>
    <td>${username}</td>
    </tr>
    `)
}
function get_all_employee(){
    fetch(
        manager_app_update_get_all_employee_url,{
            method:'POST',
            credentials:'same-origin',
            headers:{
                'X-Requested-With':'XMLHttpRequest',
                'X-CSRFToken': getCookie("csrftoken"),
            }
        }
    ).then(response=>response.json())
    .then(data=>{
        if(data.status==200){
            //useID
            // userID = data.context.employee_list[0].userID
            // console.log(userID)
            //username
            // username = data.context.employee_list[0].user.username
            // console.log(username)
            var employee_count = 0
            for(var i=0;i<data.context.employee_list.length;i++){
                //userID
                userID = data.context.employee_list[i].userID
                //username
                username = data.context.employee_list[i].user.username
                //usernamePK
                userpk = data.context.employee_list[i].user.id
                create_employee_table(userpk,userID,username,i)
                employee_count++
            }
            $('#employee_count').text(employee_count)
        }
        else{

        }
    })
}
function create_employee_table(userPk,userID,username,i){
    $('#table_data_employee').append(`
    <tr>
    <th scope="row">${i+1}</th>
    <th scope="row" style="display:none">${userPk}</th>                    
    <th scope="row" style="display:none">${userID}</th>
    <td>${userID}</td>
    <td>${username}</td>
    </tr>
    `)
}