$('body').ready(function(){
    get_student_data()
    $('#hide_student').hide()
})
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
  function create_student_table_container()
  {
      $('#student_table_data').append(
          `
          <div class="table-responsive table_style">
          <table class="table">
            <thead>
              <tr>
                <th scope="col">Sr no</th>
                <th scope="row" style="display:none;">student_ID</th>
                <th>Student's Name</th>
                <th>Roll No</th>
                <th>Mobile</th>
                <th>Father's Name</th>
                <th>email</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody id="student_info_table">
              
            </tbody>
          </table>
        </div>
          `
      )
  }
  function create_student_table(data,i){
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
                      <button class="btn btn-primary mb-1" onclick="set_attendance(
                          '${data.context[i].student_ID}','${data.context[i].Student_Name}')"><i class="fa-regular fa-file"></i></button>
                    </td>
              </tr>
              `
          );
  }
function get_student_data(){
    fetch(
        get_student_data_url,{
            method:'POST',
            credentials:'same-origin',
            headers:{
                "X-Requested-With":"XMLHttpRequest",
                "X-CSRFToken":getCookie("csrftoken")
            }
        }
    ).then(response=>response.json())
    .then(data=>{
        for(var i=0;i<data.context.length;i++){
            create_student_table(data,i)
        }
    })
}
$('body').on('click','#select_student',function(){
    $('#student_info_table').empty()
    $('#attendance_table_data').empty()
    $('#attendance_info_table').empty()
    create_student_table_container()
    get_student_data()
})

$('body').on('click','#show_attendance',function(){
    $('#student_table_data').empty()
    $('#student_info_table').empty()
    $('#attendance_table_data').empty()
    $('#attendance_info_table').empty()
    create_attendance_table_container()
    read_attandance()
})

function reset_attendance_form(){
    $('#date_picker').val("");
    $('#present').val("");
}
$('body').on('click','#cancel',function(){
    reset_attendance_form()
})
var selected_date;
$('body').on('change','#date_picker',function(){
    var date = $('#date_picker').val();
    selected_date = date
    console.log(selected_date);
})
var attendance_ID_ = 0;
$('body').on('click','#submit',function(){
    if(attendance_ID_ == 0)
    {
        insert_attendance()
        selected_date="";
        student_ID_=0;
        Student_Name_="";
        attendance_ID_=0;
        reset_attendance_form()
    }
    else{
        update_attendance()
        selected_date="";
        student_ID_=0;
        Student_Name_="";
        attendance_ID_=0;
    }
})
var student_ID_;
var Student_Name_
function set_attendance(student_ID,Student_Name){
    student_ID_ = student_ID;
    Student_Name_ = Student_Name;
    console.log(`student_ID_ = ${student_ID_}, Student_Name_ = ${Student_Name_}`)
}
function insert_attendance(){
    var no_of_days_present = $('#present').val();
    var date_selected = selected_date;
    var data ={
        no_of_days_present : no_of_days_present,
        date_selected:date_selected,
        student_ID:student_ID_,
        Student_Name:Student_Name_
    }
    fetch(insert_attendance_data_url,
        {
            method:'POST',
            credentials:"same-origin",
            headers:{
                "X-Requested-With":"XMLHttpRequest",
                "X-CSRFToken":getCookie("csrftoken")
            },
            body:JSON.stringify({'payload':data})
        }).then(response=>response.json())
        .then(data=>{
          if(data.status==200){
            read_attandance()
            Swal.fire({
              position: "top-end",
              icon: "success",
              title: "Marks settings has been saved",
              showConfirmButton: false,
              timer: 1500
            },{
              
            });
          }
          else if(data.status==500){
            Swal.fire({
              icon: "error",
              title: "Oops...",
              text: "No Student Assigned to the attendance",
            });
          }
        })
}

function create_attendance_table_container()
{
    $('#attendance_table_data').append(
        `
        <div class="table-responsive table_style">
        <table class="table">
          <thead>
            <tr>
              <th scope="col">Sr no</th>
              <th scope="row" style="display:none;">ATTENDANCE ID</th>
              <th scope="row" style="display:none;">STUDENT ID</th>
              <th>Student's Name</th>
              <th>DATE OF ATTENDANCE</th>
              <th>NUMBER OF DAYS PRESENT</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody id="attendance_info_table">
            
          </tbody>
        </table>
      </div>
        `
    )
}
function create_attendance_table(data,i){
        $('#attendance_info_table').append(
            `
            <tr ondblclick="open_student_detail('${data.context[i].attendance_ID}')">
                  <td>${i+1}</td>
                  <td scope="row" style="display:none;">${data.context[i].student_ID_id}</td>
                  <td>${data.context[i].Student_Name}</td>
                  <td>${data.context[i].date}</td>
                  <td>${data.context[i].no_of_days_present}</td>
                  <td>
                    <button class="btn btn-dark mb-1" onclick="set_update_attendance(
                        '${data.context[i].attendance_ID}','${data.context[i].student_ID_id}','${data.context[i].Student_Name}','${data.context[i].date}','${data.context[i].no_of_days_present}')"><i class="fa-solid fa-pen"></i></i>
                    </button>
                    <button class="btn btn-danger mb-1" onclick="delete_attendance(
                        '${data.context[i].attendance_ID}')"><i class="fa-solid fa-trash"></i>
                    </button>
                  </td>
            </tr>
            `
        );
}
function read_attandance(){
    fetch(
        read_attendance_data_url,{
            method:'POST',
            credentials:'same-origin',
            headers:{
                "X-Requested-With":'XMLHttpRequest',
                "X-CSRFToken":getCookie("csrftoken")
            }
        }
    ).then(response => response.json())
    .then(data=>{
        $('#attendance_info_table').empty()
        for(var i=0;i<data.context.length;i++){
            create_attendance_table(data,i)
        }
    })
}
function set_update_attendance(attendance_ID, student_ID, Student_Name,date, no_of_days_present){
    $('#student_name').text("")
    $('#student_name').text(Student_Name)
    student_ID_ = student_ID;
    attendance_ID_ = attendance_ID;
    $('#date_picker').val(date)
    $('#present').val(no_of_days_present)
}
function update_attendance(){
    var data = {
        attendance_ID : attendance_ID_,
        student_ID : student_ID_,
        date : $('#date_picker').val(),
        no_of_days_present : $('#present').val()
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
            update_attendance_data_url,{
                method:'POST',
                credentials:'same-origin',
                headers:{
                    'X-Requested-With':'XMLHttpRequest',
                    'X-CSRFToken':getCookie("csrftoken")
                },
                body : JSON.stringify({payload : data})
            }
        ).then(response => response.json())
        .then(data => {
            console.log(data)
            read_attandance()
        })
        } else if (result.isDenied) {
          Swal.fire("Changes are not saved", "", "info");
        }
      });
}
function delete_attendance(attendance_ID){
    var data = {
        attendance_ID : attendance_ID
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
          fetch(delete_attendance_data_url,{
            method:'POST',
            credentials:'same-origin',
            headers:{
                "X-Requested-With":"XMLHttpRequest",
                "X-CSRFToken":getCookie("csrftoken")
            },
            body:JSON.stringify({payload:data})
        }).then(response => response.json())
        .then(data=>{
            console.log(data)
            read_attandance()    
        })
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