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
function reset_form(){
    $('#employeeID').val("")
    $('#name').val("")  
}
$('body').ready(function(){
    get_employees_under_hr()
})
var ID = 0
function get_employees_under_hr(){
    fetch(
        employee_under_hr_list_url,{
            method:'POST',
            credentials:'same-origin',
            headers:{
                'X-Requested-With':'XMLHttpRequest',
                'X-CSRFToken':getCookie('csrftoken')
            }
            
        }
    ).then(response=>response.json())
    .then(data=>{
        if(data.status==200){
            console.log(data.context)
            $('#hr_name_container').empty()
            $('#hr_name_container').text(" " + data.hr_name.hr_name)
            $('#table_data').empty()
            for (var i=0;i<data.context.length;i++){
                create_employee_under_hr_table(data.context[i][0],i)
            }
            //create a table to show all the employees that are working under this particular hr
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
function create_employee_under_hr_table(data,i){
    $('#table_data').append(
        `
        <tr>
        <th scope="row">${i+1}</th>
        <th scope="row" style="display:none">${data.id}</th>
        <td><div id="action_column_rb_${i+1}"><button class="btn btn-light" onclick="action_rb('action_column_rb_${i+1}','${data.id}','${data.employeeID}','${data.name}')" style="background:#c4c1e0">...</button></div></td>
        <td>${data.employeeID}</td>
        <td>${data.name}</td>
</tr>
        `
    )
}

function action_rb(table_row_id,employee_pk,employeeID,employee_name){
    //remove the button and replace it with edit button here
    $(`#${table_row_id}`).empty()
    $(`#${table_row_id}`).append(`
      <button class="btn btn-light" style="background:#8dc6ff" onclick="populate_form('${employee_pk}','${employeeID}','${employee_name}')"><i class="fa-solid fa-pen"></i></button>
    `)
}

function populate_form(employee_pk,employeeID,employee_name){
    ID=0
    ID = employee_pk
    $('#employeeID').val(employeeID)
    $('#name').val(employee_name)   
}

$('body').on('click','#save_button',function(){
    var employeeID = $('#employeeID').val()
    var employee_name = $('#name').val() 
    var data={
        id:ID,
        employeeID:employeeID,
        employee_name:employee_name
    } 
    validate(data)
})

function validate(data){
    if(data.employeeID == "" || data.employee_name==""){
        Swal.fire({
            position: "top-end",
            icon: "error",
            title: "Employee ID or Employee name is empty",
            showConfirmButton: false,
            timer: 1500,
        })
    }
    else{
        send_data(data)
    } 
}

function send_data(data){
    fetch(
        Update_employee_under_hr_url,{
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
            get_employees_under_hr()
            reset_form()
            Swal.fire({
                position: "top-end",
                icon: "success",
                title: "Employee updated",
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
$('body').on('click','#back_button',function(){
    go_back()
})
function go_back(){
    window.location.href = hr_home_url
}