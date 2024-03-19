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
    get_user_profile()
    get_all_deleted_users()
    get_deleted_user_count()
    get_role_list()
    $('#recycle_bin_table').hide()
    $('#employeeID').prop('disabled', true);
})
function get_user_profile(){
    fetch(
        get_user_accounts_data_url,{
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
            // console.log(data.user_list[0]) //user profile
            // console.log(data.user_list[0].user) //user data user.id means user's pk 
            $('#table_data').empty()
            for(var i = 0 ; i<data.user_list.length;i++){
                // console.log(data.user_list[i]) //user profile
                // console.log(data.user_list[i].user)
                // console.log(data.user_list[i].is_deleted)
                // console.log(data.user_list[i].user) //user data user.id means user's pk 
                if (data.user_list[i].is_deleted == false){
                    create_table(data.user_list[i],data.user_list[i].user,i)
                }
            }
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
function create_table(user_profile_data,user_list,i){
    // user_profile_data = data.user_list[0],   user_list = data.user_list[0].user, user_pk = data.user_list[0].user.id
    // console.log(user_list.is_active)
    // console.log(user_list.id)
    // console.log(user_profile_data.is_deleted)
    //trimming date
    date_joined = user_list.date_joined 
    var trimmedDate = date_joined.substring(0, 10);
    if(user_list.is_active == true){
        if(user_profile_data.is_deleted==true){
            $('#table_data').append(
                `
                <tr>
                    <th scope="row">${i+1}</th>
                    <th scope="row" style="display:none">${user_list.id}</th>       
                    <th scope="row" style="display:none">${user_profile_data.user_role}</th>
                    <td><div id="action_column_rb_${i+1}"><button class="btn btn-light" onclick="action_rb('action_column_rb_${i+1}','${user_list.id}','${user_profile_data.user_role}','${user_profile_data.employeeID}','${user_list.username}','${user_list.first_name}','${user_list.last_name}','${user_list.email}')" style="background:#c4c1e0">...</button></div></td>
                    <td>${user_profile_data.employeeID}</td>
                    <td>${user_list.username}</td>
                    <td>${user_list.first_name}</td>
                    <td>${user_list.last_name}</td>
                    <td>${user_list.email}</td>
                    <td>${user_profile_data.user_role_name}</td>
                    <td id="status_button_row_${user_list.id}">
                        <button class="btn btn-secondary" id = "status_button_${user_list.id}" onclick='user_is_active("status_button_${user_list.id}","${user_list.is_active}","${user_list.id}")' style="background:#c4c1e0;color:green" type="button" aria-expanded="false">
                            <i class="fa-solid fa-check"></i>
                        </button>
                    </td>
                    <td id="is_deleted_button_row_${user_list.id}">
                        <button class="btn btn-secondary" id = "is_deleted_button_${user_list.id}" onclick='is_deleted_button_("#is_deleted_button_${user_list.id}","${user_list.is_deleted}",Number(${user_list.id}))' style="background:#c4c1e0;color:green" type="button" aria-expanded="false">
                            <i class="fa-solid fa-check"></i>
                        </button>
                    </td>
                    <td>${trimmedDate}</td>
                </tr>
                `
            )
        }
        else{
            $('#table_data').append(
                `
                <tr>
                    <th scope="row">${i+1}</th>
                    <th scope="row" style="display:none">${user_list.id}</th>       
                    <th scope="row" style="display:none">${user_profile_data.user_role}</th>
                    <td><div id="action_column_rb_${i+1}"><button class="btn btn-light" onclick="action_rb('action_column_rb_${i+1}','${user_list.id}','${user_profile_data.user_role}','${user_profile_data.employeeID}','${user_list.username}','${user_list.first_name}','${user_list.last_name}','${user_list.email}')" style="background:#c4c1e0">...</button></div></td>
                    <td>${user_profile_data.employeeID}</td>
                    <td>${user_list.username}</td>
                    <td>${user_list.first_name}</td>
                    <td>${user_list.last_name}</td>
                    <td>${user_list.email}</td>
                    <td>${user_profile_data.user_role_name}</td>
                    <td id="status_button_row_${user_list.id}">
                        <button class="btn btn-secondary" id = "status_button_${user_list.id}" onclick='user_is_active("status_button_${user_list.id}","${user_list.is_active}","${user_list.id}")' style="background:#c4c1e0;color:green" type="button" aria-expanded="false">
                            <i class="fa-solid fa-check"></i>
                        </button>
                    </td>
                    <td id="is_deleted_button_row_${user_list.id}">
                        <button class="btn btn-secondary" id = "is_deleted_button_${user_list.id}" onclick='is_deleted_button_("#is_deleted_button_${user_list.id}","${user_list.is_deleted}",Number(${user_list.id}))' style="background:#c4c1e0;color:red" type="button" aria-expanded="false">
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
        if(user_profile_data.is_deleted==true){
            $('#table_data').append(
                `
                <tr>
                    <th scope="row">${i+1}</th>
                    <th scope="row" style="display:none">${user_list.id}</th>                    
                    <th scope="row" style="display:none">${user_profile_data.user_role}</th>
                    <td><div id="action_column_rb_${i+1}"><button class="btn btn-light" onclick="action_rb('action_column_rb_${i+1}','${user_list.id}','${user_profile_data.user_role}','${user_profile_data.employeeID}','${user_list.username}','${user_list.first_name}','${user_list.last_name}','${user_list.email}')" style="background:#c4c1e0">...</button></div></td>
                    <td>${user_profile_data.employeeID}</td>
                    <td>${user_list.username}</td>
                    <td>${user_list.first_name}</td>
                    <td>${user_list.last_name}</td>
                    <td>${user_list.email}</td>
                    <td>${user_profile_data.user_role_name}</td>
                    <td id="status_button_row_${user_list.id}">
                        <button class="btn btn-secondary" id = "status_button_${user_list.id}" onclick='user_is_active("#status_button_${user_list.id}","${user_list.is_active}",Number(${user_list.id}))' style="background:#c4c1e0;color:red" type="button" aria-expanded="false">
                            <i class="fa-solid fa-xmark"></i>
                        </button>
                    </td>
                    <td id="is_deleted_button_row_${user_list.id}">
                        <button class="btn btn-secondary" id = "is_deleted_button_${user_list.id}" onclick='is_deleted_button_("#is_deleted_button_${user_list.id}","${user_list.is_deleted}",Number(${user_list.id}))' style="background:#c4c1e0;color:green" type="button" aria-expanded="false">
                            <i class="fa-solid fa-check"></i>
                        </button>
                    </td>
                    <td>${trimmedDate}</td>
                </tr>
                `
            )
        }
        else{
            $('#table_data').append(
                `
                <tr>
                    <th scope="row">${i+1}</th>
                    <th scope="row" style="display:none">${user_list.id}</th>                    
                    <th scope="row" style="display:none">${user_profile_data.user_role}</th>
                    <td><div id="action_column_rb_${i+1}"><button class="btn btn-light" onclick="action_rb('action_column_rb_${i+1}','${user_list.id}','${user_profile_data.user_role}','${user_profile_data.employeeID}','${user_list.username}','${user_list.first_name}','${user_list.last_name}','${user_list.email}')" style="background:#c4c1e0">...</button></div></td>
                    <td>${user_profile_data.employeeID}</td>
                    <td>${user_list.username}</td>
                    <td>${user_list.first_name}</td>
                    <td>${user_list.last_name}</td>
                    <td>${user_list.email}</td>
                    <td>${user_profile_data.user_role_name}</td>
                    <td id="status_button_row_${user_list.id}">
                        <button class="btn btn-secondary" id = "status_button_${user_list.id}" onclick='user_is_active("#status_button_${user_list.id}","${user_list.is_active}",Number(${user_list.id}))' style="background:#c4c1e0;color:red" type="button" aria-expanded="false">
                            <i class="fa-solid fa-xmark"></i>
                        </button>
                    </td>
                    <td id="is_deleted_button_row_${user_list.id}">
                        <button class="btn btn-secondary" id = "is_deleted_button_${user_list.id}" onclick='is_deleted_button_("#is_deleted_button_${user_list.id}","${user_list.is_deleted}",Number(${user_list.id}))' style="background:#c4c1e0;color:red" type="button" aria-expanded="false">
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
function user_is_active(is_active_button_id,user_is_active_status,user_id){
    // console.log(user_id)
    if (user_is_active_status == 'true'){
        $(`${is_active_button_id}`).html(
            '<i class="fa-solid fa-check"></i>'
        )
        $(`${is_active_button_id}`).css('color', 'green');
        //call the function to set status is_active
        set_user_is_active(user_id)
    }
    else{
        $(`${is_active_button_id}`).html(
            '<i class="fa-solid fa-xmark"></i>'
        )
        $(`${is_active_button_id}`).css('color', 'red');
        //call the function to set status is_active
        set_user_is_active(user_id)
    }
}
function set_user_is_active(user_id){
    var data={
        user_id:user_id
    }
    fetch(
        change_user_status_url,{
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
            //update user table
            get_user_profile()
            get_all_deleted_users()
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
function is_deleted_button_(is_deleted_button_id,user_id){
    // console.log("is_deleted")
    // console.log(user_id)
    // console.log(is_deleted_button_id)
}
function action_rb(element_id,user_id,userrole_id,employeeID,username,first_name,last_name,email){
    $(`#${element_id}`).empty()
    $(`#${element_id}`).append(`
    <button class="btn btn-danger" onclick="delete_user('${user_id}')"><i class="fa-solid fa-trash"></i></button>
    <button class="btn btn-light" style="background:#8dc6ff" onclick="populate_form('${user_id}','${userrole_id}','${employeeID}','${username}','${first_name}','${last_name}','${email}')"><i class="fa-solid fa-pen"></i></button>
    `)
}
//UPDATE USER DATA LOGIC STARTS
var user_id_backup = -1
var userrole_id_backup = -1
function populate_form(user_id,userrole_id,employeeID,username,first_name,last_name,email){
    user_id_backup = user_id
    userrole_id_backup = userrole_id
    $('#employeeID').val(employeeID)
    $('#username').val(username)
    $('#first_name').val(first_name)
    $('#last_name').val(last_name)
    $('#email').val(email)
    $('#select_user_role_input_box').val(userrole_id)
}
function create_role_selector_options_input_box(role_id,role_name){
    $('#select_user_role_input_box').append(
        `
        <option value="${role_id}">${role_name}</option>
        `
    )
}
$('body').on('click','#save_button',function(){
    var username = $('#username').val()
    var first_name = $('#first_name').val()
    var last_name = $('#last_name').val()
    var email = $('#email').val()
    var selected_role = $('#select_user_role_input_box').val()
    var data = {
        user_id : user_id_backup,
        userrole_id : userrole_id_backup,
        username:username,
        first_name:first_name,
        last_name:last_name,
        email:email,
        select_user_role_input_box:selected_role,
    }
    validate(data)
})
function validate(data){
    if(username == "" || first_name == "" || last_name == "" || email == "" || select_user_role_input_box=='-1'){
        Swal.fire({
            icon: "error",
            title: "Error...",
            text: 'Input Fields can nor be empty',
          });
    }
    else{
        send_data_update(data)
    }
}
function send_data_update(data){
    console.log("Send Data to update user")
    console.log(data)

    fetch(
        update_user_details_url,{
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
            //reset update form 
            reset_update_form()
            //reset table before updating table
            $('#table_data').empty()
            //update user table
            get_user_profile()
            get_all_deleted_users()
            Swal.fire({
                position: "top-end",
                icon: "success",
                title: "User data changed!",
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
function reset_update_form(){
    user_id_backup = -1
    userrole_id_backup = -1
    $('#employeeID').val("")
    $('#username').val("")
    $('#first_name').val("")
    $('#last_name').val("")
    $('#email').val("")
    $('#select_user_role_input_box').val("-1")
}
//UPDATE USER DATA LOGIC ENDS
//SOFT DELETE USER (send user to recycle bin)
function delete_user(user_id){
    data = {
        user_id:user_id
    }
    fetch(
        delete_user_accounts_url,{
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
            //update user table
            get_user_profile()
            get_all_deleted_users()
            $('#select_user_role_recycle_bin').val('-1')
            $('#select_user_role_user_table').val('-1')
            get_deleted_user_count()
            Swal.fire({
                position: "top-end",
                icon: "success",
                title: "User Deleted!",
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
//POPULATING ROLE DROPDOWN LIST STARTS
function get_role_list(){
    fetch(
        get_all_roles_list,{
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
            // console.log(data.context[0])
            $('#select_user_role_user_table').empty()
            $('#select_user_role_user_table').append(
                `
                <option value = "-1" selected>--Select User Role--</option>
                `
            )
            $('#select_user_role_recycle_bin').empty()
            $('#select_user_role_recycle_bin').append(
                `
                <option value = "-1" selected>--Select User Role--</option>
                `
            )
            $('#select_user_role_input_box').empty()
            $('#select_user_role_input_box').append(
                `
                <option value = "-1" selected>--Select User Role--</option>
                `
            )
            for(var i=0;i<data.context.length;i++){
                create_role_selector_options(data.context[i].id,data.context[i].roles)
                create_role_selector_options_recycle_bin(data.context[i].id,data.context[i].roles)
                create_role_selector_options_input_box(data.context[i].id,data.context[i].roles)
            }
        }
        else{

        }
    })
}
//POPULATING ROLE DROPDOWN LIST ENDS
//role selector near user table
function create_role_selector_options(role_id,role_name){
    $('#select_user_role_user_table').append(
        `
        <option value="${role_id}">${role_name}</option>
        `
    )
}
$('body').on('click','#select_user_role_user_table',function(){
    get_values_role_selector()
})
function get_values_role_selector(){
    var selected_role = $('#select_user_role_user_table').val()
    var data = {
        selected_role:selected_role
    }
    fetch(
        get_role_from_front_users_url,{
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
            console.log("Not deleted user")
            console.log(data)
            // console.log(data.context)
            // console.log(data.context.user_list.length)
            $('#table_data').empty()
            for(var i = 0 ; i<data.context.user_list.length;i++){
                if (data.context.user_list[i].is_deleted == false){
                    // create_table(data.user_list[i],data.user_list[i].user,i)
                    create_table(data.context.user_list[i],data.context.user_list[i].user,i)
                }
            }
        }
        else{
            
        }
    })
}







// recycle bin related functions
function get_all_deleted_users(){
    fetch(
        get_all_deleted_users_url,{
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
            // console.log(data)
            // console.log(data.user_list[0])
            // console.log(data.user_list[0].user)
            $('#table_data_deleted').empty()
            for(var i = 0 ; i<data.user_list.length;i++){
                // console.log(data.user_list[i])
                // console.log(data.user_list[i].user)
                // console.log(data.user_list[i].is_deleted)
                if (data.user_list[i].is_deleted == true){
                    // create_table(data.user_list[i],data.user_list[i].user,i)
                    create_recycle_bin_table(data.user_list[i],data.user_list[i].user,i)
                }
            }
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
$('body').on('click','#recycle_bin_button',function(){
    recycle_bin_button_fun()
})
var recycle_bin_table_flag = false
function recycle_bin_button_fun(){
    // console.log("recycle_bin_button clicked")
    if (recycle_bin_table_flag == true)
    {
        $('#recycle_bin_table').show()
        recycle_bin_table_flag = false
    }
    else{
        $('#recycle_bin_table').hide()
        recycle_bin_table_flag = true
    }
}
function get_deleted_user_count(){
    fetch(
        get_deleted_users_counts_url,{
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
            $('#recycle_bin_button').text(data.user_list)
        }
        else{

        }
    })
}
function create_recycle_bin_table(user_profile_data,user_list,i){
    // console.log(user_profile_data)
    // console.log(user_list)

    // user_profile_data = data.user_list[0],   user_list = data.user_list[0].user
    // console.log(user_list.is_active)
    // console.log(user_list.id)
    // console.log(user_profile_data.is_deleted)
    //trimming date
    date_joined = user_list.date_joined 
    var trimmedDate = date_joined.substring(0, 10);
    if(user_list.is_active == true){
        if(user_profile_data.is_deleted==true){
            $('#table_data_deleted').append(
                `
                <tr>
                    <th scope="row">${i+1}</th>
                    <th scope="row" style="display:none">${user_list.id}</th>       
                    <th scope="row" style="display:none">${user_profile_data.user_role}</th>
                    <td><div id="action_column${i+1}"><button class="btn btn-light" onclick="action('action_column${i+1}','${user_list.id}','${user_profile_data.user_role}')" style="background:#c4c1e0">...</button></div></td>
                    <td>${user_profile_data.employeeID}</td>
                    <td>${user_list.username}</td>
                    <td>${user_list.first_name}</td>
                    <td>${user_list.last_name}</td>
                    <td>${user_list.email}</td>
                    <td>${user_profile_data.user_role_name}</td>
                    <td id="status_button_row_${user_list.id}">
                        <button class="btn btn-secondary" id = "status_button_${user_list.id}" onclick='user_is_active("status_button_${user_list.id}","${user_list.is_active}","${user_list.id}")' style="background:#c4c1e0;color:green" type="button" aria-expanded="false">
                            <i class="fa-solid fa-check"></i>
                        </button>
                    </td>
                    <td id="is_deleted_button_row_${user_list.id}">
                        <button class="btn btn-secondary" id = "is_deleted_button_${user_list.id}" onclick='is_deleted_button_("#is_deleted_button_${user_list.id}","${user_list.is_deleted}",Number(${user_list.id}))' style="background:#c4c1e0;color:green" type="button" aria-expanded="false">
                            <i class="fa-solid fa-check"></i>
                        </button>
                    </td>
                    <td>${trimmedDate}</td>
                </tr>
                `
            )
        }
        else{
            $('#table_data_deleted').append(
                `
                <tr>
                    <th scope="row">${i+1}</th>
                    <th scope="row" style="display:none">${user_list.id}</th>       
                    <th scope="row" style="display:none">${user_profile_data.user_role}</th>
                    <td><div id="action_column${i+1}"><button class="btn btn-light" onclick="action('action_column${i+1}','${user_list.id}','${user_profile_data.user_role}')" style="background:#c4c1e0">...</button></div></td>
                    <td>${user_profile_data.employeeID}</td>
                    <td>${user_list.username}</td>
                    <td>${user_list.first_name}</td>
                    <td>${user_list.last_name}</td>
                    <td>${user_list.email}</td>
                    <td>${user_profile_data.user_role_name}</td>
                    <td id="status_button_row_${user_list.id}">
                        <button class="btn btn-secondary" id = "status_button_${user_list.id}" onclick='user_is_active("status_button_${user_list.id}","${user_list.is_active}","${user_list.id}")' style="background:#c4c1e0;color:green" type="button" aria-expanded="false">
                            <i class="fa-solid fa-check"></i>
                        </button>
                    </td>
                    <td id="is_deleted_button_row_${user_list.id}">
                        <button class="btn btn-secondary" id = "is_deleted_button_${user_list.id}" onclick='is_deleted_button_("#is_deleted_button_${user_list.id}","${user_list.is_deleted}",Number(${user_list.id}))' style="background:#c4c1e0;color:red" type="button" aria-expanded="false">
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
        if(user_profile_data.is_deleted==true){
            $('#table_data_deleted').append(
                `
                <tr>
                    <th scope="row">${i+1}</th>
                    <th scope="row" style="display:none">${user_list.id}</th>                    
                    <th scope="row" style="display:none">${user_profile_data.user_role}</th>
                    <td><div itable_data_deletedd="action_column${i+1}"><button class="btn btn-light" onclick="action('action_column${i+1}','${user_list.id}','${user_profile_data.user_role}')" style="background:#c4c1e0">...</button></div></td>
                    <td>${user_profile_data.employeeID}</td>
                    <td>${user_list.username}</td>
                    <td>${user_list.first_name}</td>
                    <td>${user_list.last_name}</td>
                    <td>${user_list.email}</td>
                    <td>${user_profile_data.user_role_name}</td>
                    <td id="status_button_row_${user_list.id}">
                        <button class="btn btn-secondary" id = "status_button_${user_list.id}" onclick='user_is_active("#status_button_${user_list.id}","${user_list.is_active}",Number(${user_list.id}))' style="background:#c4c1e0;color:red" type="button" aria-expanded="false">
                            <i class="fa-solid fa-xmark"></i>
                        </button>
                    </td>
                    <td id="is_deleted_button_row_${user_list.id}">
                        <button class="btn btn-secondary" id = "is_deleted_button_${user_list.id}" onclick='is_deleted_button_("#is_deleted_button_${user_list.id}","${user_list.is_deleted}",Number(${user_list.id}))' style="background:#c4c1e0;color:green" type="button" aria-expanded="false">
                            <i class="fa-solid fa-check"></i>
                        </button>
                    </td>
                    <td>${trimmedDate}</td>
                </tr>
                `
            )
        }
        else{
            $('#table_data_deleted').append(
                `
                <tr>
                    <th scope="row">${i+1}</th>
                    <th scope="row" style="display:none">${user_list.id}</th>                    
                    <th scope="row" style="display:none">${user_profile_data.user_role}</th>
                    <td><div class="row" id="action_column${i+1}"><button class="btn btn-light" onclick="action('action_column${i+1}','${user_list.id}','${user_profile_data.user_role}')" style="background:#c4c1e0">...</button></div></td>
                    <td>${user_profile_data.employeeID}</td>
                    <td>${user_list.username}</td>
                    <td>${user_list.first_name}</td>
                    <td>${user_list.last_name}</td>
                    <td>${user_list.email}</td>
                    <td>${user_profile_data.user_role_name}</td>
                    <td id="status_button_row_${user_list.id}">
                        <button class="btn btn-secondary" id = "status_button_${user_list.id}" onclick='user_is_active("#status_button_${user_list.id}","${user_list.is_active}",Number(${user_list.id}))' style="background:#c4c1e0;color:red" type="button" aria-expanded="false">
                            <i class="fa-solid fa-xmark"></i>
                        </button>
                    </td>
                    <td id="is_deleted_button_row_${user_list.id}">
                        <button class="btn btn-secondary" id = "is_deleted_button_${user_list.id}" onclick='is_deleted_button_("#is_deleted_button_${user_list.id}","${user_list.is_deleted}",Number(${user_list.id}))' style="background:#c4c1e0;color:red" type="button" aria-expanded="false">
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
function action(element_id,user_id,userrole_id){
    $(`#${element_id}`).empty()
    $(`#${element_id}`).append(`
    <div class="col-lg-6 col-md-6 col-sm-12">
    <button class="btn btn-primary" onclick="restore_user('${user_id}')"><i class="fa-solid fa-trash-can-arrow-up"></i></button>
    </div>
    <div class="col-lg-6 col-md-6 col-sm-12">
    <button class="btn btn-danger" onclick="delete_user_permanently('${user_id}')"><i class="fa-solid fa-trash"></i></button>
    </div>
    `)
}
function restore_user(user_id){
    // console.log(user_id)
    data={
        user_id:user_id
    }
    fetch(
        restore_user_url,{
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
            //update user table
            get_user_profile()
            get_all_deleted_users()
            get_deleted_user_count()
            $('#select_user_role_recycle_bin').val('-1')
            $('#select_user_role_user_table').val('-1')
            Swal.fire({
                position: "top-end",
                icon: "success",
                title: "User Restored!",
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
//role selector in recycle bin user table
function create_role_selector_options_recycle_bin(role_id,role_name){
    $('#select_user_role_recycle_bin').append(
        `
        <option value="${role_id}">${role_name}</option>
        `
    )
}
$('body').on('click','#select_user_role_recycle_bin',function(){
    get_values_role_selector_recycle_bin()
})
function get_values_role_selector_recycle_bin(){
    var selected_role = $('#select_user_role_recycle_bin').val()
    var data = {
        selected_role:selected_role
    }
    fetch(
        get_role_from_front_deleted_users_url,{
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
            // console.log(data)
            // console.log(data.context)
            // console.log(data.context.user_list.length)
            $('#table_data_deleted').empty()
            for(var i = 0 ; i<data.context.user_list.length;i++){
                if (data.context.user_list[i].is_deleted == true){
                    // create_table(data.user_list[i],data.user_list[i].user,i)
                    create_recycle_bin_table(data.context.user_list[i],data.context.user_list[i].user,i)
                }
            }
        }
        else{
            
        }
    })
}
//HARD DELETE USER (delete user account permanently)
function delete_user_permanently(user_id){
    var data={
        user_id:user_id,
    }
    fetch(
        hard_delete_user_accounts_url,{
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
        if (data.status==200){
            Swal.fire({
              title: "Are you sure?",
              text: "You won't be able to revert this!",
              icon: "warning",
              showCancelButton: true,
              confirmButtonColor: "#d33",
              cancelButtonColor: "#3085d6",
              confirmButtonText: "Yes, delete it!"
            }).then((result) => {
              if (result.isConfirmed) {
                //update user table
                get_user_profile()
                get_all_deleted_users()
                get_deleted_user_count()
                $('#select_user_role_recycle_bin').val('-1')
                $('#select_user_role_user_table').val('-1')
                Swal.fire({
                  title: "Deleted!",
                  text: "User Deleted Permanently!",
                  icon: "success"
                });
              }
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
// recycle bin related functions