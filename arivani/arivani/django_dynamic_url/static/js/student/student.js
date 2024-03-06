var ID=0;
/* Miscellaneous code starts */
$('body').on('click','#cancel_button',function(){
    reset_form();
})
function reset_form(){
    $('#Student_Name').val("")
    $('#Father_Name').val("")
    $('#roll_no').val("")
    $('#mobile').val("")
    $('#email').val("")
}
//get CSRF Token from the cookies
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
 function populate_form(student_ID,Student_Name,Father_Name,roll_no,mobile,email){
    ID=student_ID;
    $('#Student_Name').val(Student_Name);
    $('#Father_Name').val(Father_Name);
    $('#roll_no').val(roll_no);
    $('#mobile').val(mobile);
    $('#email').val(email);
 }
 function validation(){
    if ($('#Student_Name').val()=="" || $('#Father_Name').val()=="" || $('#roll_no').val()=="" || $('#mobile').val()=="" || $('#email').val()==""){
        Swal.fire({
            icon: "error",
            title: "Form Error",
            text: "Fields in the form cannot be empty!",
          });
          return false;
    }
    else{
        return true;
    }
 }
/* Miscellaneous code ends */

/* Insert/Update data starts */
$(`body`).on('click','#submit_button',function(){
    if(ID!=0){
        console.log('update data');
        update_data();
        reset_form();
        ID=0;
    }
    else{
        console.log('insert data');
        insert_data();
        reset_form();
    }
})
function insert_data(){
    var flag = validation();
    if(flag == true){
        var data = {
            Student_Name : $('#Student_Name').val(),
            Father_Name : $('#Father_Name').val(),
            roll_no : $('#roll_no').val(),
            mobile : $('#mobile').val(),
            email : $('#email').val(),
        }
        fetch(
            insert_data_url,{
                method : 'POST',
                credentials : 'same-origin',
                headers : {
                    'X-Requested-With' : 'XMLHttpRequest',
                    'X-CSRFToken' : getCookie('csrftoken'),
                },
                body : JSON.stringify({payload : data})
            }
        ).then(response=>response.json())
        .then(
            data=>{
                Swal.fire({
                    position: "top-end",
                    icon: "success",
                    title: "Student data has been saved",
                    showConfirmButton: false,
                    timer: 1500
                  },{
                    
                  });
                read_data();
                reset_form();
            }
        )
    }
}
/* Insert/Update data ends */

/* Read data starts here */
$('body').ready(function(){
    $('#student_info_table').empty();
    read_data();
})
function read_data(){
    fetch(
        read_data_url,{
            method : 'POST',
            credentials : 'same-origin',
            headers : {
                'X-Requested-With' : 'XMLHttpRequest',
                'X-CSRFToken' : getCookie('csrftoken'),
            }
        }
    ).then(
        response=>response.json()
    ).then(
        data=>{
            $('#student_info_table').empty();
            for(var i=0;i<data.context.length;i++){
                $('#student_info_table').append(
                    `
                    <tr ondblclick="open_student_detail('${data.context[i].student_ID}')">
                          <td>${i+1}</td>
                          <td scope="row" style="display:none;">${data.context[i].student_ID}</td>
                          <td>${data.context[i].Student_Name}</td>
                          <td>${data.context[i].Father_Name}</td>
                          <td>${data.context[i].roll_no}</td>
                          <td>${data.context[i].mobile}</td>
                          <td>${data.context[i].email}</td>
                          <td>
                            <button class="btn btn-dark mb-1" onclick="populate_form(
                                '${data.context[i].student_ID}',
                                '${data.context[i].Student_Name}',
                                '${data.context[i].Father_Name}',
                                '${data.context[i].roll_no}',
                                '${data.context[i].mobile}',
                                '${data.context[i].email}')"><i class="fa-solid fa-pen"></i></button>
                            <button class="btn btn-danger mb-1" onclick="delete_data('${data.context[i].student_ID}')"><i class="fa-solid fa-trash"></i></button>
                          </td>
                    </tr>
                    `
                )
            }
        }
    )
}
/* Read data ends here */

/* update data starts */
function update_data(){
    var data = {
        student_ID : ID,
        Student_Name : $('#Student_Name').val(),
        Father_Name : $('#Father_Name').val(),
        roll_no : $('#roll_no').val(),
        mobile : $('#mobile').val(),
        email : $('#email').val(),
    }
    Swal.fire({
        title: "Do you want to save the changes?",
        showDenyButton: true,
        showCancelButton: true,
        confirmButtonText: "Save",
        denyButtonText: `Don't save`
      }).then((result) => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
          Swal.fire("Saved!", "", "success");
        fetch(
            update_data_url,
            {
                method : "POST",
                credentials : "same-origin",
                headers:{
                    "X-Requested-With" : "XMLHttpRequest",
                    "X-CSRFToken" : getCookie("csrftoken"),
                },
                body : JSON.stringify({payload : data})
            }
        ).then(response=>response.json())
        .then(data=>{
            console.log(data);
            read_data();
        })
        } else if (result.isDenied) {
          Swal.fire("Changes are not saved", "", "info");
        }
      });
}
/* update data ends */

/* Delete data starts */
function delete_data(ID){
    var data ={
        student_ID : ID
    }
    const swalWithBootstrapButtons = Swal.mixin({
        customClass: {
          confirmButton: "btn btn-success",
          cancelButton: "btn btn-danger"
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
          swalWithBootstrapButtons.fire({
            title: "Deleted!",
            text: "Delete File operation success",
            icon: "success"
          },
          fetch(
            delete_data_url,{
                method:'POST',
                credentials:'same-origin',
                headers:{
                    'X-Requested-With':'XMLHttpRequest',
                    'X-CSRFToken':getCookie('csrftoken')
                },
                body : JSON.stringify({payload:data})
            }
        ).then(response=>response.json())
        .then(
            data=>{
                read_data();
                ID=0;
            }
        )
          );
        } else if (
          /* Read more about handling dismissals below */
          result.dismiss === Swal.DismissReason.cancel
        ) {
          swalWithBootstrapButtons.fire({
            title: "Cancelled",
            text: "Delete file operation aborted",
            icon: "error"
          });
        }
      });
}
/* Delete data ends */

/* open new page and send ID via django dynamic links starts */
function open_student_detail(ID){
        var data ={
            student_ID : ID
        }

        fetch(
            student_detail_data_url,{
                method:'POST',
                credentials:'same-origin',
                headers:{
                    'X-Requested-With':'XMLHttpRequest',
                    'X-CSRFToken':getCookie('csrftoken')
                },
                body : JSON.stringify({payload:data})
            }
        ).then(response => {
            return response.json();
        }).then(data => {
            console.log(data);  // Log the response data for debugging
            // Perform actions with the response data, e.g., rendering the student details
            window.location.href = "student_details" + `/${ID}`;
        })
}
/* open new page and send ID via django dynamic links ends */