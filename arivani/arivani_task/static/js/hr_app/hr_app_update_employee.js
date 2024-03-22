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
    get_all_deleted_ursers_by_hr()
    get_deleted_users_count()
    $('#employeeID').prop('disabled', true);
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
            // console.log(data)
            // console.log(data.context)
            // var user = data.context.employee_list[0].user
            // var userID = data.context.employee_list[0].userID
            // var is_deleted = data.context.employee_list[0].is_deleted
            // var user_role_name = data.context.employee_list[0].user_role_name
            // console.log(userID)
            // console.log(is_deleted)
            // console.log(user_role_name)
            // console.log("user data")
            // console.log(user)
            // console.log(user.username)
            $('#table_data_employee').empty()
            for(var i=0;i<data.context.employee_list.length;i++){
            var user = data.context.employee_list[i].user
            var userID = data.context.employee_list[i].userID
            var is_deleted = data.context.employee_list[i].is_deleted
            var user_role_id = data.context.employee_list[i].user_role_id
            var user_role_name = data.context.employee_list[i].user_role_name
              create_employee_table(user,userID,is_deleted,user_role_name,user_role_id,i)
            }
        }
        else{

        }
    })
}
function create_employee_table(user,userID,is_deleted,user_role_name,user_role_id,i){
  date_joined = user.date_joined 
  var trimmedDate = date_joined.substring(0, 10);
  if(user.is_active == true){
      if(is_deleted==true){
          $('#table_data_employee').append(
              `
              <tr>
                  <th scope="row">${i+1}</th>
                  <th scope="row" style="display:none">${user.id}</th>       
                  <th scope="row" style="display:none">${user_role_id}</th>
                  <td><div id="action_column_${i+1}"><button class="btn btn-light" onclick="action('action_column_${i+1}','${user.id}','${user_role_id}','${userID}','${user.username}','${user.first_name}','${user.last_name}','${user.email}')" style="background:#c4c1e0">...</button></div></td>
                  <td>${userID}</td>
                  <td>${user.username}</td>
                  <td>${user.first_name}</td>
                  <td>${user.last_name}</td>
                  <td>${user.email}</td>
                  <td>${user_role_name}</td>
                  <td id="status_button_row_${user.id}">
                      <button class="btn btn-secondary" id = "status_button_${user.id}" onclick='user_is_active("status_button_${user.id}","${user.is_active}","${user.id}")' style="background:#c4c1e0;color:green" type="button" aria-expanded="false">
                          <i class="fa-solid fa-check"></i>
                      </button>
                  </td>
                  <td id="is_deleted_button_row_${user.id}">
                      <button class="btn btn-secondary" id = "is_deleted_button_${user.id}" onclick='is_deleted_button_("#is_deleted_button_${user.id}","${user.is_deleted}",Number(${user.id}))' style="background:#c4c1e0;color:green" type="button" aria-expanded="false">
                          <i class="fa-solid fa-check"></i>
                      </button>
                  </td>
                  <td>${trimmedDate}</td>
              </tr>
              `
          )
      }
      else{
          $('#table_data_employee').append(
              `
              <tr>
                  <th scope="row">${i+1}</th>
                  <th scope="row" style="display:none">${user.id}</th>       
                  <th scope="row" style="display:none">${user_role_id}</th>
                  <td><div id="action_column_${i+1}"><button class="btn btn-light" onclick="action('action_column_${i+1}','${user.id}','${user_role_id}','${userID}','${user.username}','${user.first_name}','${user.last_name}','${user.email}')" style="background:#c4c1e0">...</button></div></td>
                  <td>${userID}</td>
                  <td>${user.username}</td>
                  <td>${user.first_name}</td>
                  <td>${user.last_name}</td>
                  <td>${user.email}</td>
                  <td>${user_role_name}</td>
                  <td id="status_button_row_${user.id}">
                      <button class="btn btn-secondary" id = "status_button_${user.id}" onclick='user_is_active("status_button_${user.id}","${user.is_active}","${user.id}")' style="background:#c4c1e0;color:green" type="button" aria-expanded="false">
                          <i class="fa-solid fa-check"></i>
                      </button>
                  </td>
                  <td id="is_deleted_button_row_${user.id}">
                      <button class="btn btn-secondary" id = "is_deleted_button_${user.id}" onclick='is_deleted_button_("#is_deleted_button_${user.id}","${user.is_deleted}",Number(${user.id}))' style="background:#c4c1e0;color:red" type="button" aria-expanded="false">
                          <i class="fa-solid fa-xmark"></i>
                      </button>
                  </td>
                  <td>${trimmedDate}</td>
              </tr>
              `
          )
      }
  }
  else{
      if(is_deleted==true){
          $('#table_data_employee').append(
              `
              <tr>
                  <th scope="row">${i+1}</th>
                  <th scope="row" style="display:none">${user.id}</th>       
                  <th scope="row" style="display:none">${user_role_id}</th>
                  <td><div id="action_column_${i+1}"><button class="btn btn-light" onclick="action('action_column_${i+1}','${user.id}','${user_role_id}','${userID}','${user.username}','${user.first_name}','${user.last_name}','${user.email}')" style="background:#c4c1e0">...</button></div></td>
                  <td>${userID}</td>
                  <td>${user.username}</td>
                  <td>${user.first_name}</td>
                  <td>${user.last_name}</td>
                  <td>${user.email}</td>
                  <td>${user_role_name}</td>
                  <td id="status_button_row_${user.id}">
                      <button class="btn btn-secondary" id = "status_button_${user.id}" onclick='user_is_active("status_button_${user.id}","${user.is_active}","${user.id}")' style="background:#c4c1e0;color:red" type="button" aria-expanded="false">
                          <i class="fa-solid fa-xmark"></i>
                      </button>
                  </td>
                  <td id="is_deleted_button_row_${user.id}">
                      <button class="btn btn-secondary" id = "is_deleted_button_${user.id}" onclick='is_deleted_button_("#is_deleted_button_${user.id}","${user.is_deleted}",Number(${user.id}))' style="background:#c4c1e0;color:green" type="button" aria-expanded="false">
                          <i class="fa-solid fa-check"></i>
                      </button>
                  </td>
                  <td>${trimmedDate}</td>
              </tr>
              `
          )
      }
      else{
          $('#table_data_employee').append(
              `
              <tr>
                  <th scope="row">${i+1}</th>
                  <th scope="row" style="display:none">${user.id}</th>       
                  <th scope="row" style="display:none">${user_role_id}</th>
                  <td><div id="action_column_${i+1}"><button class="btn btn-light" onclick="action('action_column_${i+1}','${user.id}','${user_role_id}','${userID}','${user.username}','${user.first_name}','${user.last_name}','${user.email}')" style="background:#c4c1e0">...</button></div></td>
                  <td>${userID}</td>
                  <td>${user.username}</td>
                  <td>${user.first_name}</td>
                  <td>${user.last_name}</td>
                  <td>${user.email}</td>
                  <td>${user_role_name}</td>
                  <td id="status_button_row_${user.id}">
                      <button class="btn btn-secondary" id = "status_button_${user.id}" onclick='user_is_active("status_button_${user.id}","${user.is_active}","${user.id}")' style="background:#c4c1e0;color:red" type="button" aria-expanded="false">
                          <i class="fa-solid fa-xmark"></i>
                      </button>
                  </td>
                  <td id="is_deleted_button_row_${user.id}">
                      <button class="btn btn-secondary" id = "is_deleted_button_${user.id}" onclick='is_deleted_button_("#is_deleted_button_${user.id}","${user.is_deleted}",Number(${user.id}))' style="background:#c4c1e0;color:red" type="button" aria-expanded="false">
                          <i class="fa-solid fa-xmark"></i>
                      </button>
                  </td>
                  <td>${trimmedDate}</td>
              </tr>
              `
          )
      }
  }
}
function user_is_active(status_button_id,is_active,user_pk)
{
  // console.log(user_id)
  if (is_active == 'true'){
    $(`${status_button_id}`).html(
        '<i class="fa-solid fa-check"></i>'
    )
    $(`${status_button_id}`).css('color', 'green');
    //call the function to set status is_active
    set_user_is_active(user_pk)
}
else{
    $(`${status_button_id}`).html(
        '<i class="fa-solid fa-xmark"></i>'
    )
    $(`${status_button_id}`).css('color', 'red');
    //call the function to set status is_active
    set_user_is_active(user_pk)
}
}
function set_user_is_active(user_pk){
  var data={
    user_pk:user_pk,
  }
  fetch(
    hr_app_set_employee_is_active_url,{
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
      //reset table before updating table
      $('#table_data').empty()
      $('#recycle_bin_table_employee').empty()
      //update user table
      get_all_employee_created_by_hr()
      get_all_deleted_ursers_by_hr()
      Swal.fire({
          position: "top-end",
          icon: "success",
          title: "Status of User changed",
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

//UPDATE EMPLOYEE PROFILE RELATED FUNCTIONS STARTS
$('body').on('click','#save_button',function(){
  username = $('#username').val()
  first_name = $('#first_name').val()
  last_name = $('#last_name').val()
  email = $('#email').val()
  var data = {
    user_pk:saved_user_pk,
    user_role_id:saved_user_role_id,
    username:username,
    first_name:first_name,
    last_name:last_name,
    email:email,
  }
  validate(data)
  reset_form()
})
var saved_user_pk = -1
var saved_user_role_id=-1
function populate_form(user_pk,user_role_id,userID,username,first_name,last_name,email){
  saved_user_pk=user_pk
  saved_user_role_id=user_role_id
  $('#employeeID').val(userID)
  $('#username').val(username)
  $('#first_name').val(first_name)
  $('#last_name').val(last_name)
  $('#email').val(email)
}
function isValidEmail(email) {
  // Regular expression for email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  
  // Test the email against the regex pattern
  return emailRegex.test(email);
} 
function validate(data){
  if(data.username == "" || data.first_name == "" || data.last_name == "" || data.email==""){
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
function reset_form(){
  $('#employeeID').val("")
  $('#username').val("")
  $('#first_name').val("")
  $('#last_name').val("")
  $('#email').val("")
}
function send_data(data){
  fetch(
    hr_app_update_employee_record_url,{
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
      if(data.status==200){
              //reset table before updating table
      $('#table_data').empty()
      $('#recycle_bin_table_employee').empty()
      //update user table
      get_all_employee_created_by_hr()
      get_all_deleted_ursers_by_hr()
      get_deleted_users_count()
      reset_form()
      Swal.fire({
          position: "top-end",
          icon: "success",
          title: "User Profile Updated",
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
function action(action_column_id,user_pk,user_role_id,userID,username,first_name,last_name,email){
  $(`#${action_column_id}`).empty()
  $(`#${action_column_id}`).append(`
  <button class="btn btn-danger" onclick="delete_user('${user_pk}')"><i class="fa-solid fa-trash"></i></button>
  <button class="btn btn-light" style="background:#8dc6ff" onclick="populate_form('${user_pk}','${user_role_id}','${userID}','${username}','${first_name}','${last_name}','${email}')"><i class="fa-solid fa-pen"></i></button>
  `)
}
//UPDATE EMPLOYEE PROFILE RELATED FUNCTIONS ENDS
//DELETE USER STARTS
function delete_user(user_pk){
  var data={
    user_pk:user_pk,
  }
  fetch(
    hr_app_soft_delete_employee_url,{
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
    if(data.status==200){
       //reset table before updating table
       $('#table_data').empty()
       $('#recycle_bin_table_employee').empty()
       //update user table
       get_all_employee_created_by_hr()
       get_all_deleted_ursers_by_hr()
       get_deleted_users_count()
       Swal.fire({
           position: "top-end",
           icon: "success",
           title: "User deleted",
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
//DELETE USER ENDS
//GET ALL DELETED USERS FROM RECYCLE BIN STARTS
function get_all_deleted_ursers_by_hr(){
  fetch(
    hr_app_gel_all_deleted_users_url,{
      method:'POST',
      credentials:'same-origin',
      headers:{
        'X-Requested-With':'XMLHttpRequest',
        'X-CSRFToken':getCookie("csrftoken")
      }
    }
  ).then(response=>response.json())
  .then(data=>{
    if(data.status==200){
      // console.log(data)
      //create a table to show users that are in the recycle_bin
      $('#recycle_bin_table_employee').empty()
            for(var i=0;i<data.context.employee_list.length;i++){
            var user = data.context.employee_list[i].user
            var userID = data.context.employee_list[i].userID
            var is_deleted = data.context.employee_list[i].is_deleted
            var user_role_id = data.context.employee_list[i].user_role_id
            var user_role_name = data.context.employee_list[i].user_role_name
            create_employee_recycle_bin_table(user,userID,is_deleted,user_role_name,user_role_id,i)
            }
    }
    else{
      //hide the card which contains the recycle bin tabel to show deleted users
      
    }
  })
}
function create_employee_recycle_bin_table(user,userID,is_deleted,user_role_name,user_role_id,i){
  date_joined = user.date_joined 
  var trimmedDate = date_joined.substring(0, 10);
  if(user.is_active == true){
      if(is_deleted==true){
          $('#recycle_bin_table_employee').append(
              `
              <tr>
                  <th scope="row">${i+1}</th>
                  <th scope="row" style="display:none">${user.id}</th>       
                  <th scope="row" style="display:none">${user_role_id}</th>
                  <td><div id="action_column_rb_${i+1}"><button class="btn btn-light" onclick="action_recycle_bin('action_column_rb_${i+1}','${user.id}','${user_role_id}')" style="background:#c4c1e0">...</button></div></td>
                  <td>${userID}</td>
                  <td>${user.username}</td>
                  <td>${user.first_name}</td>
                  <td>${user.last_name}</td>
                  <td>${user.email}</td>
                  <td>${user_role_name}</td>
                  <td id="status_button_row_${user.id}">
                      <button class="btn btn-secondary" id = "status_button_${user.id}" onclick='user_is_active("status_button_${user.id}","${user.is_active}","${user.id}")' style="background:#c4c1e0;color:green" type="button" aria-expanded="false">
                          <i class="fa-solid fa-check"></i>
                      </button>
                  </td>
                  <td id="is_deleted_button_row_${user.id}">
                      <button class="btn btn-secondary" id = "is_deleted_button_${user.id}" onclick='is_deleted_button_("#is_deleted_button_${user.id}","${user.is_deleted}",Number(${user.id}))' style="background:#c4c1e0;color:green" type="button" aria-expanded="false">
                          <i class="fa-solid fa-check"></i>
                      </button>
                  </td>
                  <td>${trimmedDate}</td>
              </tr>
              `
          )
      }
      else{
          $('#recycle_bin_table_employee').append(
              `
              <tr>
                  <th scope="row">${i+1}</th>
                  <th scope="row" style="display:none">${user.id}</th>       
                  <th scope="row" style="display:none">${user_role_id}</th>
                  <td><div id="action_column_rb_${i+1}"><button class="btn btn-light" onclick="action_recycle_bin('action_column_rb_${i+1}','${user.id}','${user_role_id}')" style="background:#c4c1e0">...</button></div></td>
                  <td>${userID}</td>
                  <td>${user.username}</td>
                  <td>${user.first_name}</td>
                  <td>${user.last_name}</td>
                  <td>${user.email}</td>
                  <td>${user_role_name}</td>
                  <td id="status_button_row_${user.id}">
                      <button class="btn btn-secondary" id = "status_button_${user.id}" onclick='user_is_active("status_button_${user.id}","${user.is_active}","${user.id}")' style="background:#c4c1e0;color:green" type="button" aria-expanded="false">
                          <i class="fa-solid fa-check"></i>
                      </button>
                  </td>
                  <td id="is_deleted_button_row_${user.id}">
                      <button class="btn btn-secondary" id = "is_deleted_button_${user.id}" onclick='is_deleted_button_("#is_deleted_button_${user.id}","${user.is_deleted}",Number(${user.id}))' style="background:#c4c1e0;color:red" type="button" aria-expanded="false">
                          <i class="fa-solid fa-xmark"></i>
                      </button>
                  </td>
                  <td>${trimmedDate}</td>
              </tr>
              `
          )
      }
  }
  else{
      if(is_deleted==true){
          $('#recycle_bin_table_employee').append(
              `
              <tr>
                  <th scope="row">${i+1}</th>
                  <th scope="row" style="display:none">${user.id}</th>       
                  <th scope="row" style="display:none">${user_role_id}</th>
                  <td><div id="action_column_rb_${i+1}"><button class="btn btn-light" onclick="action_recycle_bin('action_column_rb_${i+1}','${user.id}','${user_role_id}')" style="background:#c4c1e0">...</button></div></td>
                  <td>${userID}</td>
                  <td>${user.username}</td>
                  <td>${user.first_name}</td>
                  <td>${user.last_name}</td>
                  <td>${user.email}</td>
                  <td>${user_role_name}</td>
                  <td id="status_button_row_${user.id}">
                      <button class="btn btn-secondary" id = "status_button_${user.id}" onclick='user_is_active("status_button_${user.id}","${user.is_active}","${user.id}")' style="background:#c4c1e0;color:red" type="button" aria-expanded="false">
                          <i class="fa-solid fa-xmark"></i>
                      </button>
                  </td>
                  <td id="is_deleted_button_row_${user.id}">
                      <button class="btn btn-secondary" id = "is_deleted_button_${user.id}" onclick='is_deleted_button_("#is_deleted_button_${user.id}","${user.is_deleted}",Number(${user.id}))' style="background:#c4c1e0;color:green" type="button" aria-expanded="false">
                          <i class="fa-solid fa-check"></i>
                      </button>
                  </td>
                  <td>${trimmedDate}</td>
              </tr>
              `
          )
      }
      else{
          $('#recycle_bin_table_employee').append(
              `
              <tr>
                  <th scope="row">${i+1}</th>
                  <th scope="row" style="display:none">${user.id}</th>       
                  <th scope="row" style="display:none">${user_role_id}</th>
                  <td><div id="action_column_rb_${i+1}"><button class="btn btn-light" onclick="action_recycle_bin('action_column_rb_${i+1}','${user.id}','${user_role_id}')" style="background:#c4c1e0">...</button></div></td>
                  <td>${userID}</td>
                  <td>${user.username}</td>
                  <td>${user.first_name}</td>
                  <td>${user.last_name}</td>
                  <td>${user.email}</td>
                  <td>${user_role_name}</td>
                  <td id="status_button_row_${user.id}">
                      <button class="btn btn-secondary" id = "status_button_${user.id}" onclick='user_is_active("status_button_${user.id}","${user.is_active}","${user.id}")' style="background:#c4c1e0;color:red" type="button" aria-expanded="false">
                          <i class="fa-solid fa-xmark"></i>
                      </button>
                  </td>
                  <td id="is_deleted_button_row_${user.id}">
                      <button class="btn btn-secondary" id = "is_deleted_button_${user.id}" onclick='is_deleted_button_("#is_deleted_button_${user.id}","${user.is_deleted}",Number(${user.id}))' style="background:#c4c1e0;color:red" type="button" aria-expanded="false">
                          <i class="fa-solid fa-xmark"></i>
                      </button>
                  </td>
                  <td>${trimmedDate}</td>
              </tr>
              `
          )
      }
  }
}
function action_recycle_bin(element_id,user_id,userrole_id){
  $(`#${element_id}`).empty()
  $(`#${element_id}`).append(`
  <div class="col-lg-6 col-md-6 col-sm-12">
  <button class="btn btn-primary" onclick="restore_user('${user_id}')"><i class="fa-solid fa-trash-can-arrow-up"></i></button>
  </div>
  <div class="col-lg-6 col-md-6 col-sm-12">
  <button class="btn btn-danger" onclick="delete_user_permanently('${user_id}')"><i class="fa-solid fa-skull-crossbones"></i></button>
  </div>
  `)
}
function restore_user(user_id){
  var data = {
    user_id:user_id
  }
  fetch(
    hr_app_restore_user_url,{
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
    if(data.status==200){
      //reset table before updating table
      $('#table_data').empty()
      $('#recycle_bin_table_employee').empty()
      //update user table
      get_all_employee_created_by_hr()
      get_all_deleted_ursers_by_hr()
      get_deleted_users_count()
      Swal.fire({
          position: "top-end",
          icon: "success",
          title: "User deleted",
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
//delete user permanently
function delete_user_permanently(user_id){
  var data = {
    user_id:user_id,
  }
  const swalWithBootstrapButtons = Swal.mixin({
    customClass: {
      confirmButton: "btn btn-danger",
      cancelButton: "btn btn-success"
    },
    buttonsStyling: false
  });
  swalWithBootstrapButtons.fire({
    title: "Are you sure?",
    text: "You won't be able to revert this!",
    icon: "warning",
    showCancelButton: true,
    confirmButtonText: "Yes, delete it!",
    cancelButtonText: "No, cancel!",
    reverseButtons: true
  }).then((result) => {
    if (result.isConfirmed) {
        //put the code to delete data apermanently here
        fetch(
          hr_app_delete_user_permanently_url,{
            method:'POST',
            credentials:'same-origin',
            headers:{
              'X-Requested-With':'XMLHttpRequest',
              'X-CSRFToken':getCookie("csrftoken"),
            },
            body:JSON.stringify({payload:data}),
          }
        ).then(response=>response.json())
        .then(data=>{
          if(data.status==200){
            //reset table before updating table
            $('#table_data').empty()
            $('#recycle_bin_table_employee').empty()
            //update user table
            get_all_employee_created_by_hr()
            get_all_deleted_ursers_by_hr()
            get_deleted_users_count()
            Swal.fire({
                position: "top-end",
                icon: "success",
                title: "User deleted permanently",
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
    } else if (
      /* Read more about handling dismissals below */
      result.dismiss === Swal.DismissReason.cancel
    ) {
      swalWithBootstrapButtons.fire({
        title: "Cancelled",
        text: "Operation aborted :)",
        icon: "error"
      });
    }
  });
}
//GET ALL DELETED USERS FROM RECYCLE BIN ENDS

//GET DELETED USER'S COUNT RECYCLE BIN BUTTON 
function get_deleted_users_count(){
  fetch(
    hr_app_get_all_deleted_user_count_url,{
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
      // console.log(data.context)
      // console.log(data.context.deleted_users_count) 
      $('#recycle_bin_btn').empty()
      if(data.context.deleted_users_count>=1){
        $('#recycle_bin_btn').text(data.context.deleted_users_count)
      }
      else{
        $('#recycle_bin_btn').empty()
        $('#recycle_bin_btn').text("...")
        //hide the recycle bin table
        $('#recyclebin_data_card').hide()
      }
    }
    else{
      $('#recycle_bin_btn').empty()
      $('#recycle_bin_btn').text("...")
    }
  })
}
//GET DELETED USER'S COUNT RECYCLE BIN BUTTON 

//HIDE/SHOW RECYCLEBIN TABLE ON recycle_bin_btn PRESS STARTS
$('body').on('click','#recycle_bin_btn',function(){
  hide_show_recycle_bin_table()
})
var recycle_bin_table_flag = false
function hide_show_recycle_bin_table(){
  var recycle_bin_button_val = $('#recycle_bin_btn').text()
  if (recycle_bin_button_val != "..."){
    if(recycle_bin_table_flag==true){
      //show table
      $('#recyclebin_data_card').show()
      recycle_bin_table_flag=false
    }
    else{
      //hide table
      $('#recyclebin_data_card').hide()
      recycle_bin_table_flag=true
    }
  }
  else{
    Swal.fire({
      icon: "error",
      title: "Error...",
      text: 'No Data in recycle bin',
    });
  }
}
//HIDE/SHOW RECYCLEBIN TABLE ON recycle_bin_btn PRESS ENDS