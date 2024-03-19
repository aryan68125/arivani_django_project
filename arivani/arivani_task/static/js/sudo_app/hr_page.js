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
    get_all_employees_data()
    get_all_hr()
    select_hr_table_row()
    select_employee_table_row()
})
function get_all_employees_data(){
    fetch(
        get_all_employees_url,{
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
            $('#table_data_employee').empty()
            for(var i=0;i<data.user_list.length;i++){
                create_employee_table(data.user_list[i],data.user_list[i].user,i)
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
function create_employee_table(user_profile_data,django_contrib_user_model_data,i){
    // //array of django_contrib_user_model_data extra user profile data
    // console.log(data.django_contrib_user_model_data[0]) 
    // //django user account data from django.contrib.user model
    // console.log(data.django_contrib_user_model_data[0].user) 
    date_joined = django_contrib_user_model_data.date_joined 
    var trimmedDate = date_joined.substring(0, 10);
    if(django_contrib_user_model_data.is_active == true){
        if(user_profile_data.is_deleted==true){
            $('#table_data_employee').append(
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
            $('#table_data_employee').append(
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
            $('#table_data_employee').append(
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
            $('#table_data_employee').append(
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
var saved_selected_employee = [];
var saved_selected_employee_show_in_form = []
function select_employee_table_row() {
    // Event handler for clicking on table rows
    $('#table_data_employee').on('click', 'tr', function() {
        // Get the employee ID from the clicked row
        var employeeID = $(this).find('th:nth-child(2)').text();
        var employee_ID = $(this).find('td:eq(2)').text();
        var employee_name = $(this).find('td:eq(0)').text();
        var emp_list_item = employee_name + " " + employee_ID

        // Check if the row already has the 'table-primary' class
        if ($(this).hasClass('table-primary')) {
            // Remove the 'table-primary' class from the row
            $(this).removeClass('table-primary');

            // Remove the employee ID from the array
            var index = saved_selected_employee.indexOf(employeeID);
            if (index !== -1) {
                saved_selected_employee.splice(index, 1);
            }
            //Remove element from select_employee_table_row array
            var index2 = saved_selected_employee_show_in_form.indexOf(emp_list_item)
            if (index2!=-1){
                saved_selected_employee_show_in_form.splice(index2, 1);
            }
        } else {
            // Add the 'table-primary' class to the row
            $(this).addClass('table-primary');

            // Add the employee ID to the array
            saved_selected_employee.push(employeeID);
            saved_selected_employee_show_in_form.push(emp_list_item);
        }

        // Log the array with selected employee IDs
        // console.log(saved_selected_employee);
        // console.log(saved_selected_employee_show_in_form)
        set_items_multi_slect_dropdown()
    });
    
}
function set_items_multi_slect_dropdown(){
    $('#select_employee').empty()
    for(var i=0;i<saved_selected_employee_show_in_form.length;i++){
        create_multi_select(saved_selected_employee_show_in_form[i])
    }
}
function create_multi_select(items){
    $('#select_employee').append(`
    <option value="">${items}</option>
    `)
}
// MULTI-SELECT EMPLOYEES FROM EMPLOYEE TABLE ENDS------->
function get_all_hr(){
    fetch(
        get_all_hr_url,{
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
//SELECT HR FROM HR TABLE SINGLE-SELECT STARTS------->
var saved_selected_Hr = [];

function select_hr_table_row() {
    $('#table_data_hr').on('click', 'tr', function() {
        // Get the value of the clicked row
        var hrId = $(this).find('th:nth-child(2)').text().trim();

        if ($(this).hasClass('table-primary')) {
            // If the row is already selected, deselect it
            $(this).removeClass('table-primary');
            // Clear the selected value
            saved_selected_Hr = [];
            $('#hrID').val("");
            $('#name').val("");
        } else {
            // Remove the green background from previously selected row
            $('#table_data_hr tr.table-primary').removeClass('table-primary');
            // Add green background to the clicked row
            $(this).addClass('table-primary');
            // Store the selected value
            saved_selected_Hr = [hrId];
            // Update form when a hr is selected
            var hrID = $(this).find('td:eq(0)').text().trim();
            $('#hrID').val(hrID);
    
            var hr_name = $(this).find('td:eq(2)').text().trim();
            $('#name').val(hr_name);
        }

        // console.log(saved_selected_Hr);
    });
}
//SELECT HR FROM HR TABLE SINGLE-SELECT ENDS------->

//GET USER ID AND SUBORDINATE ID AND SEND IT TO THE BACKEND STARTS------>******
$('body').on('click','#save_button',function(){
    collect_selected_hr_and_employees()
})
function collect_selected_hr_and_employees(){
    var data = {
        saved_selected_Hr:saved_selected_Hr,
        saved_selected_employee:saved_selected_employee
    }
    if (saved_selected_Hr.length != 0 && saved_selected_employee.length!=0){
        // console.log(data)
        fetch(
            assign_subordinates_url,{
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
    else{
        Swal.fire({
            icon: "error",
            title: "Error...",
            text: 'Either employee or hr not selected!!',
          });
    }
}
function reset_update_form(){
    $('#select_employee').empty()
    $('#select_employee').append(
        `
        <option value="">--No Employee--</option>
        `
    )
    $('#name').val("")
    $('#hrID').val("")
}
//GET USER ID AND SUBORDINATE ID AND SEND IT TO THE BACKEND ENDS------>******