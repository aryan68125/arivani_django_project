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
  function create_manager_table(userPk,userID,username,i){
    $('#table_data_manager').append(`
    <tr>
    <th scope="row">${i+1}</th>
    <th scope="row" style="display:none">${userPk}</th>                    
    <th scope="row" style="display:none">${userID}</th>
    <td>${userID}</td>
    <td>${username}</td>
    </tr>
    `)
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
  $('body').ready(function(){
    get_all_users()
})
function get_all_users(){
    fetch(
        get_all_users_dashboard_url,{
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
            // console.log(data)
            var emp_c = 0
            var hr_c = 0
            var manager_c = 0
            for (var i=0;i<data.context.user_list.length;i++)
            {
                 //user_role
                 // console.log(data.context.user_list[0].user_role)
                 var user_role = data.context.user_list[i].user_role
                 //userID
                 // console.log(data.context.user_list[0].userID)
                 var userID = data.context.user_list[i].userID
                 var userPk = userID.match(/\d+/)[0];
                 //username
                 // console.log(data.context.user_list[0].username)
                 var username = data.context.user_list[i].username
     
                 if (user_role == 1){
                     //employee
                     create_employee_table(userPk,userID,username,emp_c)
                     emp_c++
                 }
                 else if(user_role == 2){
                     //Hr
                     create_hr_table(userPk,userID,username,hr_c)
                     hr_c++
                 }
                 else if(user_role==3){
                     //manager
                     create_manager_table(userPk,userID,username,manager_c)
                     manager_c++
                 }
            }
            $('#manager_count').text(manager_c)
            $('#hr_count').text(hr_c)
            $('#employee_count').text(emp_c)
        }
        else{

        }
    })
}