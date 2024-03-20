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
    get_all_hr_data()
    get_all_manager()
    select_hr_table_row()
    select_manager_table_row()
})
function get_all_hr_data(){
    fetch(
        get_all_hr_manager_views_url,{
            method:'POST',
            credentials:'same-origin',
            headers:{
                'X-Requested-With':'XMLHttpRequest',
                'X-CSRFToken': getCookie("csrftoken")
            }
        }
    ).then(response=>response.json())
    .then(data=>{
        if (data.status==200){
            // console.log(data)
            // //array of django_contrib_user_model_data extra user profile data
            // console.log(data.user_list[0]) 
            // //django user account data from django.contrib.user model
            // console.log(data.user_list[0].user) 
            $('#table_data_hr').empty()
            for(var i=0;i<data.user_list.length;i++){
                create_hr_table(data.user_list[i],data.user_list[i].user,i)
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
function create_hr_table(user_profile_data,django_contrib_user_model_data,i){
    // //array of django_contrib_user_model_data extra user profile data
    // console.log(data.django_contrib_user_model_data[0]) 
    // //django user account data from django.contrib.user model
    // console.log(data.django_contrib_user_model_data[0].user) 
    date_joined = django_contrib_user_model_data.date_joined 
    var trimmedDate = date_joined.substring(0, 10);
    if(django_contrib_user_model_data.is_active == true){
        if(user_profile_data.is_deleted==true){
            $('#table_data_hr').append(
                `
                <tr>
                    <th scope="row">${i+1}</th>
                    <th scope="row" style="display:none">${django_contrib_user_model_data.id}</th>       
                    <th scope="row" style="display:none">${user_profile_data.user_role}</th>
                    <td>${user_profile_data.employeeID}</td>
                    <td>${django_contrib_user_model_data.username}</td>
                    <td>${django_contrib_user_model_data.first_name}</td>
                    <td>${django_contrib_user_model_data.last_name}</td>
                    <td>${django_contrib_user_model_data.email}</td>
                    <td>${user_profile_data.user_role_name}</td>
                    <td id="status_button_row_${django_contrib_user_model_data.id}">
                        <button class="btn btn-secondary" id = "status_button_${django_contrib_user_model_data.id}" onclick='user_is_active("status_button_${django_contrib_user_model_data.id}","${django_contrib_user_model_data.is_active}","${django_contrib_user_model_data.id}")' style="background:#c4c1e0;color:green" type="button" aria-expanded="false">
                            <i class="fa-solid fa-check"></i>
                        </button>
                    </td>
                    <td id="is_deleted_button_row_${django_contrib_user_model_data.id}">
                        <button class="btn btn-secondary" id = "is_deleted_button_${django_contrib_user_model_data.id}" onclick='is_deleted_button_("#is_deleted_button_${django_contrib_user_model_data.id}","${django_contrib_user_model_data.is_deleted}",Number(${django_contrib_user_model_data.id}))' style="background:#c4c1e0;color:green" type="button" aria-expanded="false">
                            <i class="fa-solid fa-check"></i>
                        </button>
                    </td>
                    <td>${trimmedDate}</td>
                </tr>
                `
            )
        }
        else{
            $('#table_data_hr').append(
                `
                <tr>
                    <th scope="row">${i+1}</th>
                    <th scope="row" style="display:none">${django_contrib_user_model_data.id}</th>       
                    <th scope="row" style="display:none">${user_profile_data.user_role}</th>
                    <td>${user_profile_data.employeeID}</td>
                    <td>${django_contrib_user_model_data.username}</td>
                    <td>${django_contrib_user_model_data.first_name}</td>
                    <td>${django_contrib_user_model_data.last_name}</td>
                    <td>${django_contrib_user_model_data.email}</td>
                    <td>${user_profile_data.user_role_name}</td>
                    <td id="status_button_row_${django_contrib_user_model_data.id}">
                        <button class="btn btn-secondary" id = "status_button_${django_contrib_user_model_data.id}" onclick='user_is_active("status_button_${django_contrib_user_model_data.id}","${django_contrib_user_model_data.is_active}","${django_contrib_user_model_data.id}")' style="background:#c4c1e0;color:green" type="button" aria-expanded="false">
                            <i class="fa-solid fa-check"></i>
                        </button>
                    </td>
                    <td id="is_deleted_button_row_${django_contrib_user_model_data.id}">
                        <button class="btn btn-secondary" id = "is_deleted_button_${django_contrib_user_model_data.id}" onclick='is_deleted_button_("#is_deleted_button_${django_contrib_user_model_data.id}","${django_contrib_user_model_data.is_deleted}",Number(${django_contrib_user_model_data.id}))' style="background:#c4c1e0;color:red" type="button" aria-expanded="false">
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
            $('#table_data_hr').append(
                `
                <tr>
                    <th scope="row">${i+1}</th>
                    <th scope="row" style="display:none">${django_contrib_user_model_data.id}</th>                    
                    <th scope="row" style="display:none">${user_profile_data.user_role}</th>
                    <td>${user_profile_data.employeeID}</td>
                    <td>${django_contrib_user_model_data.username}</td>
                    <td>${django_contrib_user_model_data.first_name}</td>
                    <td>${django_contrib_user_model_data.last_name}</td>
                    <td>${django_contrib_user_model_data.email}</td>
                    <td>${user_profile_data.user_role_name}</td>
                    <td id="status_button_row_${django_contrib_user_model_data.id}">
                        <button class="btn btn-secondary" id = "status_button_${django_contrib_user_model_data.id}" onclick='user_is_active("#status_button_${django_contrib_user_model_data.id}","${django_contrib_user_model_data.is_active}",Number(${django_contrib_user_model_data.id}))' style="background:#c4c1e0;color:red" type="button" aria-expanded="false">
                            <i class="fa-solid fa-xmark"></i>
                        </button>
                    </td>
                    <td id="is_deleted_button_row_${django_contrib_user_model_data.id}">
                        <button class="btn btn-secondary" id = "is_deleted_button_${django_contrib_user_model_data.id}" onclick='is_deleted_button_("#is_deleted_button_${django_contrib_user_model_data.id}","${django_contrib_user_model_data.is_deleted}",Number(${django_contrib_user_model_data.id}))' style="background:#c4c1e0;color:green" type="button" aria-expanded="false">
                            <i class="fa-solid fa-check"></i>
                        </button>
                    </td>
                    <td>${trimmedDate}</td>
                </tr>
                `
            )
        }
        else{
            $('#table_data_hr').append(
                `
                <tr>
                    <th scope="row">${i+1}</th>
                    <th scope="row" style="display:none">${django_contrib_user_model_data.id}</th>                    
                    <th scope="row" style="display:none">${user_profile_data.user_role}</th>
                    <td>${user_profile_data.employeeID}</td>
                    <td>${django_contrib_user_model_data.username}</td>
                    <td>${django_contrib_user_model_data.first_name}</td>
                    <td>${django_contrib_user_model_data.last_name}</td>
                    <td>${django_contrib_user_model_data.email}</td>
                    <td>${user_profile_data.user_role_name}</td>
                    <td id="status_button_row_${django_contrib_user_model_data.id}">
                        <button class="btn btn-secondary" id = "status_button_${django_contrib_user_model_data.id}" onclick='user_is_active("#status_button_${django_contrib_user_model_data.id}","${django_contrib_user_model_data.is_active}",Number(${django_contrib_user_model_data.id}))' style="background:#c4c1e0;color:red" type="button" aria-expanded="false">
                            <i class="fa-solid fa-xmark"></i>
                        </button>
                    </td>
                    <td id="is_deleted_button_row_${django_contrib_user_model_data.id}">
                        <button class="btn btn-secondary" id = "is_deleted_button_${django_contrib_user_model_data.id}" onclick='is_deleted_button_("#is_deleted_button_${django_contrib_user_model_data.id}","${django_contrib_user_model_data.is_deleted}",Number(${django_contrib_user_model_data.id}))' style="background:#c4c1e0;color:red" type="button" aria-expanded="false">
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
// MULTI-SELECT EMPLOYEES FROM EMPLOYEE TABLE STARTS------->
var saved_selected_hr = [];
var saved_selected_hr_show_in_form = []
function select_hr_table_row() {
    // Event handler for clicking on table rows
    $('#table_data_hr').on('click', 'tr', function() {
        // Get the employee ID from the clicked row
        var hrID = $(this).find('th:nth-child(2)').text();
        var hr_f_name = $(this).find('td:eq(2)').text();
        var hr_l_name = $(this).find('td:eq(3)').text();
        var hr_name = hr_f_name + " " + hr_l_name
        var hr_ID = $(this).find('td:eq(0)').text();
        var hr_list_item = hr_ID + " " + hr_name

        // Check if the row already has the 'table-primary' class
        if ($(this).hasClass('table-primary')) {
            // Remove the 'table-primary' class from the row
            $(this).removeClass('table-primary');

            // Remove the employee ID from the array
            var index = saved_selected_hr.indexOf(hrID);
            if (index !== -1) {
                saved_selected_hr.splice(index, 1);
            }
            //Remove element from select_employee_table_row array
            var index2 = saved_selected_hr_show_in_form.indexOf(hr_list_item)
            if (index2!=-1){
                saved_selected_hr_show_in_form.splice(index2, 1);
            }
        } else {
            // Add the 'table-primary' class to the row
            $(this).addClass('table-primary');

            // Add the employee ID to the array
            saved_selected_hr.push(hrID);
            saved_selected_hr_show_in_form.push(hr_list_item);
        }

        // Log the array with selected employee IDs
        // console.log(saved_selected_employee);
        // console.log(saved_selected_employee_show_in_form)
        set_items_multi_slect_dropdown()
    });
    
}
function set_items_multi_slect_dropdown(){
    $('#select_hr').empty()
    for(var i=0;i<saved_selected_hr_show_in_form.length;i++){
        create_multi_select(saved_selected_hr_show_in_form[i])
    }
}
function create_multi_select(items){
    $('#select_hr').append(`
    <option value="">${items}</option>
    `)
}
// MULTI-SELECT EMPLOYEES FROM EMPLOYEE TABLE ENDS------->
function get_all_manager(){
    fetch(
        get_all_manager_manager_views_url,{
            method:'POST',
            credentials:'same-origin',
            headers:{
                'X-Requested-With':'XMLHttpRequest',
                'X-CSRFtoken':getCookie("csrftoken")
            }
        }
    ).then(response=>response.json())
    .then(data=>{
        if(data.status==200){
            // console.log("hr's list")
            // console.log(data)
            // //array of django_contrib_user_model_data extra user profile data
            // console.log(data.user_list[0]) 
            // //django user account data from django.contrib.user model
            // console.log(data.user_list[0].user) 
            $('#table_data_manager').empty()
            for(var i=0;i<data.user_list.length;i++){
                create_manager_table(data.user_list[i],data.user_list[i].user,i)
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
function create_manager_table(user_profile_data,django_contrib_user_model_data,i){
    // //array of django_contrib_user_model_data extra user profile data
    // console.log(data.django_contrib_user_model_data[0]) 
    // //django user account data from django.contrib.user model
    // console.log(data.django_contrib_user_model_data[0].user) 
    date_joined = django_contrib_user_model_data.date_joined 
    var trimmedDate = date_joined.substring(0, 10);
    if(django_contrib_user_model_data.is_active == true){
        if(user_profile_data.is_deleted==true){
            $('#table_data_manager').append(
                `
                <tr>
                    <th scope="row">${i+1}</th>
                    <th scope="row" style="display:none">${django_contrib_user_model_data.id}</th>       
                    <th scope="row" style="display:none">${user_profile_data.user_role}</th>
                    <td>${user_profile_data.employeeID}</td>
                    <td>${django_contrib_user_model_data.username}</td>
                    <td>${django_contrib_user_model_data.first_name}</td>
                    <td>${django_contrib_user_model_data.last_name}</td>
                    <td>${django_contrib_user_model_data.email}</td>
                    <td>${user_profile_data.user_role_name}</td>
                    <td id="status_button_row_${django_contrib_user_model_data.id}">
                        <button class="btn btn-secondary" id = "status_button_${django_contrib_user_model_data.id}" onclick='user_is_active("status_button_${django_contrib_user_model_data.id}","${django_contrib_user_model_data.is_active}","${django_contrib_user_model_data.id}")' style="background:#c4c1e0;color:green" type="button" aria-expanded="false">
                            <i class="fa-solid fa-check"></i>
                        </button>
                    </td>
                    <td id="is_deleted_button_row_${django_contrib_user_model_data.id}">
                        <button class="btn btn-secondary" id = "is_deleted_button_${django_contrib_user_model_data.id}" onclick='is_deleted_button_("#is_deleted_button_${django_contrib_user_model_data.id}","${django_contrib_user_model_data.is_deleted}",Number(${django_contrib_user_model_data.id}))' style="background:#c4c1e0;color:green" type="button" aria-expanded="false">
                            <i class="fa-solid fa-check"></i>
                        </button>
                    </td>
                    <td>${trimmedDate}</td>
                </tr>
                `
            )
        }
        else{
            $('#table_data_manager').append(
                `
                <tr>
                    <th scope="row">${i+1}</th>
                    <th scope="row" style="display:none">${django_contrib_user_model_data.id}</th>       
                    <th scope="row" style="display:none">${user_profile_data.user_role}</th>
                    <td>${user_profile_data.employeeID}</td>
                    <td>${django_contrib_user_model_data.username}</td>
                    <td>${django_contrib_user_model_data.first_name}</td>
                    <td>${django_contrib_user_model_data.last_name}</td>
                    <td>${django_contrib_user_model_data.email}</td>
                    <td>${user_profile_data.user_role_name}</td>
                    <td id="status_button_row_${django_contrib_user_model_data.id}">
                        <button class="btn btn-secondary" id = "status_button_${django_contrib_user_model_data.id}" onclick='user_is_active("status_button_${django_contrib_user_model_data.id}","${django_contrib_user_model_data.is_active}","${django_contrib_user_model_data.id}")' style="background:#c4c1e0;color:green" type="button" aria-expanded="false">
                            <i class="fa-solid fa-check"></i>
                        </button>
                    </td>
                    <td id="is_deleted_button_row_${django_contrib_user_model_data.id}">
                        <button class="btn btn-secondary" id = "is_deleted_button_${django_contrib_user_model_data.id}" onclick='is_deleted_button_("#is_deleted_button_${django_contrib_user_model_data.id}","${django_contrib_user_model_data.is_deleted}",Number(${django_contrib_user_model_data.id}))' style="background:#c4c1e0;color:red" type="button" aria-expanded="false">
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
            $('#table_data_manager').append(
                `
                <tr>
                    <th scope="row">${i+1}</th>
                    <th scope="row" style="display:none">${django_contrib_user_model_data.id}</th>                    
                    <th scope="row" style="display:none">${user_profile_data.user_role}</th>
                    <td>${user_profile_data.employeeID}</td>
                    <td>${django_contrib_user_model_data.username}</td>
                    <td>${django_contrib_user_model_data.first_name}</td>
                    <td>${django_contrib_user_model_data.last_name}</td>
                    <td>${django_contrib_user_model_data.email}</td>
                    <td>${user_profile_data.user_role_name}</td>
                    <td id="status_button_row_${django_contrib_user_model_data.id}">
                        <button class="btn btn-secondary" id = "status_button_${django_contrib_user_model_data.id}" onclick='user_is_active("#status_button_${django_contrib_user_model_data.id}","${django_contrib_user_model_data.is_active}",Number(${django_contrib_user_model_data.id}))' style="background:#c4c1e0;color:red" type="button" aria-expanded="false">
                            <i class="fa-solid fa-xmark"></i>
                        </button>
                    </td>
                    <td id="is_deleted_button_row_${django_contrib_user_model_data.id}">
                        <button class="btn btn-secondary" id = "is_deleted_button_${django_contrib_user_model_data.id}" onclick='is_deleted_button_("#is_deleted_button_${django_contrib_user_model_data.id}","${django_contrib_user_model_data.is_deleted}",Number(${django_contrib_user_model_data.id}))' style="background:#c4c1e0;color:green" type="button" aria-expanded="false">
                            <i class="fa-solid fa-check"></i>
                        </button>
                    </td>
                    <td>${trimmedDate}</td>
                </tr>
                `
            )
        }
        else{
            $('#table_data_manager').append(
                `
                <tr>
                    <th scope="row">${i+1}</th>
                    <th scope="row" style="display:none">${django_contrib_user_model_data.id}</th>                    
                    <th scope="row" style="display:none">${user_profile_data.user_role}</th>
                    <td>${user_profile_data.employeeID}</td>
                    <td>${django_contrib_user_model_data.username}</td>
                    <td>${django_contrib_user_model_data.first_name}</td>
                    <td>${django_contrib_user_model_data.last_name}</td>
                    <td>${django_contrib_user_model_data.email}</td>
                    <td>${user_profile_data.user_role_name}</td>
                    <td id="status_button_row_${django_contrib_user_model_data.id}">
                        <button class="btn btn-secondary" id = "status_button_${django_contrib_user_model_data.id}" onclick='user_is_active("#status_button_${django_contrib_user_model_data.id}","${django_contrib_user_model_data.is_active}",Number(${django_contrib_user_model_data.id}))' style="background:#c4c1e0;color:red" type="button" aria-expanded="false">
                            <i class="fa-solid fa-xmark"></i>
                        </button>
                    </td>
                    <td id="is_deleted_button_row_${django_contrib_user_model_data.id}">
                        <button class="btn btn-secondary" id = "is_deleted_button_${django_contrib_user_model_data.id}" onclick='is_deleted_button_("#is_deleted_button_${django_contrib_user_model_data.id}","${django_contrib_user_model_data.is_deleted}",Number(${django_contrib_user_model_data.id}))' style="background:#c4c1e0;color:red" type="button" aria-expanded="false">
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
//SELECT HR FROM HR TABLE SINGLE-SELECT STARTS------->
var saved_selected_manager = [];

function select_manager_table_row() {
    $('#select_hr').empty()
    $('#table_data_manager').on('click', 'tr', function() {
        // Get the value of the clicked row
        var managerId = $(this).find('th:nth-child(2)').text().trim();

        if ($(this).hasClass('table-primary')) {
            // If the row is already selected, deselect it
            $(this).removeClass('table-primary');
            // Clear the selected value
            saved_selected_manager = [];
            $('#managerID').val("");
            $('#name').val("");
            get_all_subordinates_assigned_to_manager(managerID)
        } else {
            // Remove the green background from previously selected row
            $('#table_data_manager tr.table-primary').removeClass('table-primary');
            // Add green background to the clicked row
            $(this).addClass('table-primary');
            // Store the selected value
            saved_selected_manager = [managerId];
            // Update form when a hr is selected
            var managerID = $(this).find('td:eq(0)').text().trim();
            $('#managerID').val(managerID);
    
            var manager_name = $(this).find('td:eq(2)').text().trim();
            $('#name').val(manager_name);
            
            get_all_subordinates_assigned_to_manager(managerID)
        }

        // console.log(saved_selected_Hr);
    });
}
//SELECT HR FROM HR TABLE SINGLE-SELECT ENDS------->

//GET USER ID AND SUBORDINATE ID AND SEND IT TO THE BACKEND STARTS------>******
$('body').on('click','#save_button',function(){
    collect_selected_manager_and_hr()
})
function collect_selected_manager_and_hr(){
    var data = {
        saved_selected_hr:saved_selected_hr,
        saved_selected_manager:saved_selected_manager
    }
    if (saved_selected_manager.length != 0){
        // console.log(data)
        fetch(
            assign_subordinates_manager_views_url,{
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
                reset_update_form()
                Swal.fire({
                    position: "top-end",
                    icon: "success",
                    title: "Hr assigned to the manager",
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
    else{
        Swal.fire({
            icon: "error",
            title: "Error...",
            text: 'Either Hr or Manager not selected!!',
          });
    }
}
function reset_update_form(){
    $('#select_hr').empty()
    $('#select_hr').append(
        `
        <option value="">--No Employee--</option>
        `
    )
    $('#name').val("")
    $('#managerID').val("")
    get_all_hr_data()
}
//GET USER ID AND SUBORDINATE ID AND SEND IT TO THE BACKEND ENDS------>******

//get all subordinates assigned to the manager STARTS
function get_all_subordinates_assigned_to_manager(managerID){
    var data = {
        managerID : managerID
    }
    fetch(
        get_all_assigned_subordinates_manager_url,{
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
            // console.log(data.context[0])
            //subordinates assigned to the manager
            // console.log(data.context[0].subordinates)
            //subordinate id
            // console.log(data.context[0].subordinates[0].id)
            $('#select_hr').empty()
            var options =[];
            var rowCount = $('#table_data_hr tr').length;
            for (var j = 0; j < rowCount; j++) {
                var table_hr_id = $('#table_data_hr tr:eq(' + j + ') th:nth-child(2)').text().trim();
                var row = $('#table_data_hr tr:eq(' + j + ')');
                var found = false;
                for(var i = 0; i < data.context[0].subordinates.length; i++){
                    if(data.context[0].subordinates[i].id == table_hr_id){
                        found = true;
                        var id = data.context[0].subordinates[i].id
                        var option = id.toString() + " " + data.context[0].subordinates[i].first_name + " " + data.context[0].subordinates[i].last_name
                        options.push(option)
                        break;
                    }
                }

                if(found){
                    row.addClass('table-primary');
                } else {
                    row.removeClass('table-primary');
                }
            }
            for(var k = 0 ; k<options.length;k++){
                $('#select_hr').append(
                    `
                    <option value="">${options[k]}</option>
                    `
                )
            }
        }
        else{

        }
    })
}
//get all subordinates assigned to the manager ENDS