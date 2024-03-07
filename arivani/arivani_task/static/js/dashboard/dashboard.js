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
 var data = {
    hrID : hrID,
    name:name
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
                console.log("update data")
                data.id = ID
                update_data(data)
            }
            else{
                console.log("insert data")
                send_data(data)
            }
        }
    }
}
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
            // console.log(data.context)
            $('#table_data').empty()
            for(var i=0;i<data.context.length;i++){
                create_table(data.context[i],i)
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
//create table 
function create_table(data,i){
//    console.log(data)
//    console.log(i)
      $('#table_data').append(
        `
        <tr>
                <th scope="row">${i+1}</th>
                <th scope="row" style="display:none">${data.id}</th>
                <td><div id="action_column_${i+1}"><button class="btn btn-light" onclick="action('action_column_${i+1}','${data.id}','${data.HrID}','${data.name}')" style="background:#c4c1e0">...</button></div></td>
                <td>${data.HrID}</td>
                <td>${data.name}</td>
        </tr>
        `
      )
}
function action(element_id,id,HrID,name){
    console.log("action button clicked")
    $(`#${element_id}`).empty()
    $(`#${element_id}`).append(`
    <button class="btn btn-danger" onclick="delete_data('${id}')"><i class="fa-solid fa-trash"></i></button>
    <button class="btn btn-light" style="background:#8dc6ff" onclick="populate_form('${id}','${HrID}','${name}')"><i class="fa-solid fa-pen"></i></button>
    `)
}

function populate_form(id,HrID,name){
    ID = 0
    ID = id
    $('#hrID').val(`${HrID}`)
    $('#name').val(`${name}`)
    $('#acc_title').empty()
    $('#acc_title').append(
        `
        Update Hr
        `
    )
}
function update_data(data){
    
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
        console.log(data)
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
        text: "You won't be able to revert this!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
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