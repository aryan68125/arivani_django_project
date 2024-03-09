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
    get_deleted_count_hr()
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
    // console.log("action button clicked")
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
        // console.log(data)
        //call create table function here
        $('#recycle_bin_table_data').empty()
        for(var i=0;i<data.data.length;i++){
            // console.log(data.data[i])
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
    //    console.log(data)
    //    console.log(i)
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
    console.log("action button clicked")
    $(`#${element_id}`).empty()
    $(`#${element_id}`).append(`
    <button class="btn btn-danger" onclick="delete_data_permanently_rb('${id}')"><i class="fa-solid fa-skull-crossbones"></i></button>
    <button class="btn btn-primary" style="background:#8dc6ff" onclick="restore_data_rb('${id}')"><i class="fa-solid fa-trash-can-arrow-up"></i></button>
    `)
}

function restore_data_rb(id){
    // console.log("Data to be restored")
    // console.log(id)
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