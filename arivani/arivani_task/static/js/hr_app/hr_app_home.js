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
function areAllNumbers(str) {
    // Regular expression to match only numbers
    const regex = /^[0-9]+$/;
    
    // Check if the string contains only numbers
    return regex.test(str);
}
function reset_form(){
    $('#hrID').val("")
    $('#name').val("")
    $('#acc_title').empty()
    $('#acc_title').append(
        `
        Add Hr
        `
    )
}
ID= 0
$('body').on('click','#save_button',function(){
 var hrID = $('#hrID').val()
 var name = $('#name').val()
 var employee_under_Hr = $('#select_employee').val()
 var data = {
    hrID : hrID,
    name:name,
    employee_under_Hr:employee_under_Hr,
 }
 validate(data)
})
function validate(data){
    if (data.hrID=="" && data.name==""){
            // Show the element
            $("#hrID_error").show();
            $("#name_error").show();

            // Hide the element after 5 seconds
            setTimeout(function() {
            $("#hrID_error").hide();
            $("#name_error").hide();
            }, 3000); // 5000 milliseconds = 5 seconds
    }
    else{
        if (data.hrID==""){
            // Show the element
            $("#hrID_error").show();

            // Hide the element after 5 seconds
            setTimeout(function() {
            $("#hrID_error").hide();
            }, 3000); // 5000 milliseconds = 5 seconds
        }
        else if(!areAllNumbers(data.hrID)){
            // Show the element
            $("#hrID_number_error").show();

            // Hide the element after 5 seconds
            setTimeout(function() {
            $("#hrID_number_error").hide();
            }, 3000); // 5000 milliseconds = 5 seconds
        }
        else if(data.hrID<=0){
            // Show the element
            $("#hrID_positive_number_error").show();

            // Hide the element after 5 seconds
            setTimeout(function() {
            $("#hrID_positive_number_error").hide();
            }, 3000); // 5000 milliseconds = 5 seconds
        }
        else if(data.name==""){
            $("#name_error").show();
            // Hide the element after 5 seconds
            setTimeout(function() {
                $("#name_error").hide();
                }, 3000); // 5000 milliseconds = 5 seconds
        }
        else{
            if (ID!=0){
                //update data
                data.id = ID
                update_data(data)
            }
            else{
                send_data(data)
            }
        }
    }
}
/* Create options for selector dynamically */
function create_options_multi_select_SELECTOR(data,i){
    $('#select_employee').append(
        `
        <option value="${data.id}">${data.name}</option>
        `
    )
}
/* Create options for selector dynamically */
function send_data(data){
    fetch(
        insert_data_url,{
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
        if (data.status==201){
            get_data()
            reset_form()
            Swal.fire({
                position: "top-end",
                icon: "success",
                title: "insert data success",
                showConfirmButton: false,
                timer: 1500,
            })
        }
        else{
            Swal.fire({
                position: "top-end",
                icon: "error",
                title: data.error,
                showConfirmButton: false,
                timer: 1500,
            })
        }
    })
}
$('body').ready(function(){
    get_data()
})
function get_data(){
    fetch(
        get_all_data_url,{
            method:'GET',
            credentials:'same-origin',
        }
    ).then(response=>response.json())
    .then(data=>{
        if (data.status==200){
            //get data from db
            //get all employees from employee tables
            $('#select_employee').empty()
            for(var i=0;i<data.employees.length;i++){
                create_options_multi_select_SELECTOR(data.employees[i],i)
            }
            //get all employee counts that are working under hr
            // console.log(data.employees_under_hr_count)
            //access values based on keys in an object
            // console.log(data.employees_under_hr_count['41'])
            // console.log(data.employees_under_hr_count[`${data.context[13].id}`])
            //get all hr's from hr table
            // console.log(data.context)
            // console.log(data.context[0])
            // console.log(data.context[13].id)
            $('#table_data').empty()
            for(var i=0;i<data.context.length;i++){
                // console.log(data.context[i].name)
                //     console.log(i)
                //     console.log(data.context[i].id)
                if (data.employees_under_hr_count[`${data.context[i].id}`]){
                    create_table(data.context[i],i,data.employees_under_hr_count[`${data.context[i].id}`])
                    
                }
                else{
                    create_table(data.context[i],i)
                }
            }
        }
        else{
            Swal.fire({
                position: "top-end",
                icon: "error",
                title: data.error,
                showConfirmButton: false,
                timer: 1500,
            })
        }
    })
    get_deleted_count_hr()
}
//create table 
function create_table(data,i,number_of_employees_under_hr){
    if (number_of_employees_under_hr){
        // console.log(number_of_employees_under_hr)
        $('#table_data').append(
            `
            <tr>
                    <th scope="row">${i+1}</th>
                    <th scope="row" style="display:none">${data.id}</th>
                    <td><div id="action_column_${i+1}"><button class="btn btn-light" onclick="action('action_column_${i+1}','${data.id}','${data.HrID}','${data.name}')" style="background:#c4c1e0">...</button></div></td>
                    <td>${data.HrID}</td>
                    <td>${data.name}</td>
                    <td><div id="employee_under_hr_column_${i+1}"><button class="btn btn-light" onclick="open_employee_list_under_hr('${data.id}')" style="background:#c4c1e0">${number_of_employees_under_hr}</button></div></td>
            </tr>
            `
          )
    }
    else{
        $('#table_data').append(
            `
            <tr>
                    <th scope="row">${i+1}</th>
                    <th scope="row" style="display:none">${data.id}</th>
                    <td><div id="action_column_${i+1}"><button class="btn btn-light" onclick="action('action_column_${i+1}','${data.id}','${data.HrID}','${data.name}')" style="background:#c4c1e0">...</button></div></td>
                    <td>${data.HrID}</td>
                    <td>${data.name}</td>
                    <td><div id="employee_under_hr_column_${i+1}"><button class="btn btn-light" style="background:#c4c1e0">...</button></div></td>
            </tr>
            `
          )
    }
}
function action(element_id,id,HrID,name){
    $(`#${element_id}`).empty()
    $(`#${element_id}`).append(`
    <button class="btn btn-danger" onclick="delete_data('${id}')"><i class="fa-solid fa-trash"></i></button>
    <button class="btn btn-light" style="background:#8dc6ff" onclick="populate_form('${id}','${HrID}','${name}')"><i class="fa-solid fa-pen"></i></button>
    `)
}
/* open a new page that has the list of all the employees that are working under hr */
function open_employee_list_under_hr(hr_pk){
    var data={
        hr_pk:hr_pk
    }
    // first send hr's primary key then go to the next page
    fetch(
        send_hr_id_to_open_employee_under_hr_page_url,{
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
            window.location.href=employees_under_hr_page_url
        }
        else if(data.status=400){
            Swal.fire({
                position: "top-end",
                icon: "error",
                title: data.error,
                showConfirmButton: false,
                timer: 1500,
            })
        }
        else if(data.status==500){
            Swal.fire({
                position: "top-end",
                icon: "error",
                title: data.error,
                showConfirmButton: false,
                timer: 1500,
            })
        }
    })
}
/* open a new page that has the list of all the employees that are working under hr */
selected_employee = []
function reset_employee_multi_select_dropdown(){
    fetch(
        send_all_employees_reset_dropdown_multiSelect_url,{
            method:'POST',
            credentials:'same-origin',
            headers:{
                'X-Requested-With':'XMLHttpRequest',
                'X-CSRFToken':getCookie("csrftoken")
            },
        }
    ).then(response=>response.json())
    .then(data=>{
        if (data.status==200){
            for(var i=0;i<data.context.length;i++){
                create_options_multi_select_SELECTOR(data.context[i],i)
            }
            for(var i=0;i<selected_employee.length;i++){
                $("#select_employee option[value='" + selected_employee[i] + "']").prop("selected", true);
            } 
        }
        else{
            Swal.fire({
                position: "top-end",
                icon: "error",
                title: data.error,
                showConfirmButton: false,
                timer: 1500,
            })
        }
    })
}
function populate_form(id,HrID,name){
    ID = 0
    ID = id
    $('#hrID').val(`${HrID}`)
    $('#name').val(`${name}`)
    // TESTING get all the employees working under hr and set it to the select field that has multi-select capability
    
    var data = {
        id : ID
    }
    fetch(
        send_all_employees_under_hr_UPDATE_url,{
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
            //set the multi-select field to the employees under hr
            $('#select_employee').empty()
            reset_employee_multi_select_dropdown()
            selected_employee.length = 0;
            for(var i=0;i<data.context.length;i++){                
                selected_employee.push(data.context[i].id)
            }     
        }
        else{
            //do nothing show error
            Swal.fire({
                position: "top-end",
                icon: "error",
                title: data.error,
                showConfirmButton: false,
                timer: 1500,
            })
        }
    })
// TESTING

    $('#acc_title').empty()
    $('#acc_title').append(
        `
        Update Hr
        `
    )
}
function update_data(data){
    console.log(data)
    fetch(
        update_data_url,{
            method:'PUT',
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
            get_data()
            reset_form()
            Swal.fire({
                position: "top-end",
                icon: "success",
                title: "Update data success!!",
                showConfirmButton: false,
                timer: 1500,
            })
        }
        else{
            Swal.fire({
                position: "top-end",
                icon: "error",
                title: data.error,
                showConfirmButton: false,
                timer: 1500,
            })
        }
    })
}

function delete_data(id){
    var data = {
        id:id
    }
    Swal.fire({
        title: "Are you sure?",
        text: "Move to recycle bin!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Yes, delete it!"
      }).then((result) => {
        if (result.isConfirmed) {
            fetch(
                delete_data_url,
                {
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
                if(data.status=200){
                    get_data()
                    get_recyclebin_data()
                    Swal.fire({
                        position: "top-end",
                        icon: "success",
                        title: "Data Deleted!!",
                        showConfirmButton: false,
                        timer: 1500,
                    })
                }
                else{
                    Swal.fire({
                        position: "top-end",
                        icon: "error",
                        title: data.error,
                        showConfirmButton: false,
                        timer: 1500,
                    })
                }
            })
        }
      });
}


//Recycle bin functionality
$('body').ready(function(){
    get_deleted_count_hr()
})
function get_deleted_count_hr(){
    fetch(
        recycleBinData_hr_url,{
            method:'POST',
            credentials:'same-origin',
            headers:{
                'X-Requested-With':'XMLHttpRequest',
                'X-CSRFToken':getCookie("csrftoken"),
            }
        }
    ).then(response=>response.json())
    .then(data=>{
        if(data.status == 200){
            //show this data in the button
            $('#recycle_bin_btn').empty()
            $('#recycle_bin_btn').text(data.count)
        }
        else{
            $('#recycle_bin_btn').empty()
            $('#recycle_bin_btn').text("...") 
            $('#recyclebin_data_card').hide()
            // Swal.fire({
            //     position: "top-end",
            //     icon: "error",
            //     title: data.error,
            //     showConfirmButton: false,
            //     timer: 1500,
            // })
        }
    })
}
$('body').ready(function(){
    $('#recyclebin_data_card').hide()
})
var toggle_recycle_card_flage = 0
$('body').on('click','#recycle_bin_btn',function(){
    var recycle_bin_btn_count = $('#recycle_bin_btn').text()
    if (recycle_bin_btn_count>=1){
        //if recycle bin has some data then show card on button click
        if (toggle_recycle_card_flage == 0){
            $('#recyclebin_data_card').show()
            get_recyclebin_data()
            toggle_recycle_card_flage=1
        }
        else{
            $('#recyclebin_data_card').hide()
            toggle_recycle_card_flage=0
        }
        //call the function to show a card that will contain a table to show deleted data
    }
    else{
        Swal.fire({
            position: "top-end",
            icon: "error",
            title: 'recycle bin empty',
            showConfirmButton: false,
            timer: 1500,
        })
    }
})
function get_recyclebin_data(){
  fetch(
    recyclebin_Data_hr_url,
    {
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
        //call create table function here
        $('#recycle_bin_table_data').empty()
        for(var i=0;i<data.data.length;i++){
            create_recycil_bin_table(data.data[i],i)
        }
    }
    else{
        Swal.fire({
            position: "top-end",
            icon: "error",
            title: data.error,
            showConfirmButton: false,
            timer: 1500,
        })
    }
  })  
}
function create_recycil_bin_table(data,i){
          $('#recycle_bin_table_data').append(
            `
            <tr>
                    <th scope="row">${i+1}</th>
                    <th scope="row" style="display:none">${data.id}</th>
                    <td><div id="action_column_rb_${i+1}"><button class="btn btn-light" onclick="action_rb('action_column_rb_${i+1}','${data.id}','${data.HrID}','${data.name}')" style="background:#c4c1e0">...</button></div></td>
                    <td>${data.HrID}</td>
                    <td>${data.name}</td>
            </tr>
            `
          )
    }
function action_rb(element_id,id,HrID,name){
    $(`#${element_id}`).empty()
    $(`#${element_id}`).append(`
    <button class="btn btn-danger" onclick="delete_data_permanently_rb('${id}')"><i class="fa-solid fa-skull-crossbones"></i></button>
    <button class="btn btn-primary" style="background:#8dc6ff" onclick="restore_data_rb('${id}')"><i class="fa-solid fa-trash-can-arrow-up"></i></button>
    `)
}

function restore_data_rb(id){
    var data={
        id:id
    }
    fetch(
        restore_data_hr_url,{
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
            get_data()
            get_recyclebin_data()
            Swal.fire({
                position: "top-end",
                icon: "success",
                title: "Data Restored!!",
                showConfirmButton: false,
                timer: 1500,
            })
        }
        else{
            Swal.fire({
                position: "top-end",
                icon: "error",
                title: data.error,
                showConfirmButton: false,
                timer: 1500,
            })
        }
    })
}
function delete_data_permanently_rb(id){
    var data ={
        id:id
    }
    const swalWithBootstrapButtons = Swal.mixin({
        customClass: {
          confirmButton: "btn btn-danger",
          cancelButton: "btn btn-primary"
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
            fetch(
                delete_data_permanently_hr_url,
                {
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
                    get_deleted_count_hr()
                    get_recyclebin_data()
                    Swal.fire({
                        position: "top-end",
                        icon: "success",
                        title: "Data Deleted Permanently!!",
                        showConfirmButton: false,
                        timer: 1500,
                    })
                }
                else{
                    Swal.fire({
                        position: "top-end",
                        icon: "error",
                        title: data.error,
                        showConfirmButton: false,
                        timer: 1500,
                    })
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
//Recycle bin functionality