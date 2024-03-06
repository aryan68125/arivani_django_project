/* Mecellaneous code starts*/

/* check if the inputs in the marks form is a valid number or a float number starts */
function isValidNumber(value) {
    // Use regular expression to check if the value is a valid number or float
    // This pattern allows for an optional negative sign, followed by digits,
    // an optional decimal point, and optional digits after the decimal point.
    var numberRegex = /^-?\d*\.?\d+$/;

    return numberRegex.test(value);
}
/* check if the inputs in the marks form is a valid number or a float number ends */

/* Get CSRF token starts */
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
/* Get CSRF token ends */

/* show marks_settings, marks and student tables starts */
$('body').on('click','#marks_button',function(){
    $('#student_table_data').empty()
    $('#student_info_table').empty();
    $('#marks_settings_form').empty();
    $('#marks_table_container').empty();
    create_marks_table_container();
    read_marks();
})
function create_marks_table(){
}
$('body').on('click','#student_button',function(){
    $('#student_table_data').empty();
    $('#student_info_table').empty();
    $('#marks_settings_form').empty();
    $('#marks_table_container').empty();
    create_student_table_container();
    read_student_data();
})

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
                    <button class="btn btn-primary mb-1" onclick="set_marks(
                        '${data.context[i].student_ID}','${data.context[i].Student_Name}')"><i class="fa-regular fa-file"></i></button>
                  </td>
            </tr>
            `
        );
}

function create_marks_table_container(){
    $('#marks_table_container').append(
        `
        <div class="table-responsive table_style">
        <table class="table">
          <thead>
            <tr>
              <th scope="col">Sr no</th>
              <th scope="row" style="display:none;">marks_ID</th>
              <th scope="row" style="display:none;">marks_settings_ID</th>
              <th scope="row" style="display:none;">Student_ID</th>
              <th>Student name</th>
              <th>Maths</th>
              <th>Physics</th>
              <th>Chemistry</th>
              <th>Computer</th>
              <th>English</th>
              <th>Hindi</th>
              <th>Total marks obtained</th>
              <th>Passing marks per subject</th>
              <th>Total marks per subject</th>
              <th>Passing percentage</th>
              <th>Percentage</th>
              <th>Pass</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody id="marks_info_table">
            
          </tbody>
        </table>
      </div>
        `
    )
}
function create_marks_table(data,i,Total_marks_per_subject,passing_marks_per_subject,passing_percentage){
    var icon = `<i class="fa-solid fa-xmark text-danger"></i>`;
    if(data.pass_fail == true){
        icon = `<i class="fa-solid fa-check text-success"></i>`;
    }
    else{
        icon = `<i class="fa-solid fa-xmark text-danger"></i>`;
    }
    $('#marks_info_table').append(
        `
        <tr>
              <td>${i+1}</td>
              <td scope="row" style="display:none;">${data.marks_ID}</td>
              <td scope="row" style="display:none;">${data.Student_ID}</td>
              <td>${data.Student_name}</td>
              <td>${data.Maths}</td>
              <td>${data.Physics}</td>
              <td>${data.Chemistry}</td>
              <td>${data.Computer}</td>
              <td>${data.English}</td>
              <td>${data.Hindi}</td>
              <td>${data.Total_marks_obtained}</td>
              <td>${passing_marks_per_subject}</td>
              <td>${Total_marks_per_subject}</td>
              <td>${passing_percentage}</td>
              <td>${data.Percentage}</td>
              <td>${icon}</td>
              <td>
                <button class="btn btn-primary mb-1" onclick="set_marksID('${data.marks_ID}',
                '${data.Student_name}',
                '${data.Maths}',
                '${data.Physics}',
                '${data.Chemistry}',
                '${data.Computer}',
                '${data.English}',
                '${data.Hindi}',
                )"><i class="fa-solid fa-pen"></i></button>
                <button class="btn btn-danger mb-1" onclick="delete_marks(${data.marks_ID})"><i class="fa-solid fa-trash"></i></button>
              </td>
        </tr>
        `
    );
    //onclick="read_marks('${data.context[i].student_ID}','${data.context[i].marks_ID}')"
}

$('body').on('click','#marks_settings_button',function(){
    $('#student_table_data').empty();
    $('#student_info_table').empty();
    $('#marks_settings_form').empty();
    $('#marks_table_container').empty();
    create_marks_settings_form();
})
function create_marks_settings_form(){
    $('#marks_settings_form').append(
        `
        <div class="container">
        <div class="mb-2">
            <div class="row">
              <h3>Marks settings</h3>
            </div>
            <div class="row">
              <div class="col-lg-4 col-md-6 col-sm-12">
                <div class="mb-3">
                  <label for="Total_marks_per_subject" class="form-label">Total marks per subject</label>
                  <input type="text" class="form-control form_inputs" id="Total_marks_per_subject">
                </div>
              </div>
              <div class="col-lg-4 col-md-6 col-sm-12">
                <div class="mb-3">
                  <label for="passing_percentage" class="form-label">Passing Percentage</label>
                  <input type="text" class="form-control form_inputs" id="passing_percentage">
                </div>
              </div>
            </div>
            <div class="row">
                  <div class="button_container">
                    <button class="btn btn-success mb-1 mx-1" id="submit_settings_button">Save Settings</button>
                    <button class="btn btn-danger mb-1 mx-1" id="cancel_settings_button">Cancel</button>
                  </div>              
            </div>
          </div>
        `
    );
}
/* reset marks settings form starts */
$('body').on('click','#cancel_settings_button',function(){
    reset_marks_setting_form();
})
function reset_marks_setting_form(){
    $('#passing_percentage').val("");
    $('#passing_marks_per_subject').val("");
    $('#Total_marks_per_subject').val("");
}
/* reset marks settings form ends */

/* show marks_settings, marks and student tables ends */

/* set_marks to the student starts */
var studentID=0;
var StudentName="";
function set_marks(student_ID,Student_Name){
    studentID = student_ID;
    StudentName = Student_Name;
    $('#student_name').empty();
    $('#student_name').text(`${StudentName}'s marks`);
    reset_marks_form();
}
/* set_marks to the student ends */

/* reset student's marks form starts */
$('body').on('click','#cancel_button',function(){
    reset_marks_form()
})
function reset_marks_form(){
    $('#Maths').val("");
    $('#Physics').val("");
    $('#Chemistry').val("");
    $('#Computer').val("");
    $('#English').val("");
    $('#Hindi').val("");
}
/* reset student's marks form ends */

/* Mecellaneous code ends*/


/* Read Student Data starts */
function read_student_data(){
    fetch(
        read_student_data_url,{
            method:'POST',
            credentials:'same-origin',
            headers:{
                "X-Requested-With" : "XMLHttpRequest",
                "X-CSRFToken" : getCookie("csrftoken")
            }
        }
    ).then(response=>response.json())
    .then(data=>{
        $("#student_info_table").empty()
        for(var i=0;i<data.context.length;i++){
            create_student_table(data,i);
        }
    })
}
/* Read Student Data ends */

/* CRUD operations on marks settings */
$('body').on('click','#submit_settings_button',function(){
    insert_marks_settings();
    recalculate_pass();
})
function insert_marks_settings(){
    var marks_settings_ID = 1;
    var passing_percentage = $('#passing_percentage').val();
    var passing_marks_per_subject = $('#passing_marks_per_subject').val();
    var Total_marks_per_subject = $('#Total_marks_per_subject').val();
    if (isValidNumber(marks_settings_ID) && isValidNumber(passing_percentage)){
        var data = {
            marks_settings_ID : marks_settings_ID,
            passing_percentage : passing_percentage,
            passing_marks_per_subject : passing_marks_per_subject,
            Total_marks_per_subject:Total_marks_per_subject
        }
        fetch(
            marks_settings_data_url,{
                method:"POST",
                credentials:"same-origin",
                headers:{
                    "X-Requested-With":"XMLHttpRequest",
                    "X-CSRFToken":getCookie("csrftoken"),
                },
                body:JSON.stringify({'payload':data})
            }
        ).then(response=>response.json())
        .then(data=>{
            Swal.fire({
                position: "top-end",
                icon: "success",
                title: "Marks settings has been saved",
                showConfirmButton: false,
                timer: 1500
              },{
                
              });
            reset_marks_setting_form();
        });
    }
    else{
        Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "Input fields are either empty or the values entered are not numbers"
          });
    }
}
function recalculate_pass(){
    var passing_percentage;
    fetch(
        recalculate_pass_fail_data_url,{
            method:'POST',
            credentials:'same-origin',
            headers:{
                'X-Requested-With':'XMLHttpRequest',
                'X-CSRFToken':getCookie("csrftoken")
            }
        }
    ).then(response=>response.json())
    .then(data=>{
        console.log(data);
        // passing_percentage = data.Marks_Settings[0].passing_percentage
    });
}
/* CRUD operations on marks settings */

/* Marks CRUD operations starts */
$('body').on('click','#submit_button',function(){
    if(Number($(`#marks_ID_`).text())!=0){
        update_marks();
        $(`#marks_ID_`).empty();
        studentID=0;
        StudentName="";
    }
    else{
        if(studentID!=0){
            insert_marks();
            studentID=0;
            StudentName="";
            $(`#marks_ID_`).empty();
        }
        else{
            Swal.fire({
                icon: "error",
                title: "Oops...",
                text: "Need a Student to assign marks"
              });
        }
    }
})
/* insert update marks data starts */
function insert_marks(){
    var Student_name = StudentName;
    var Maths = $('#Maths').val();
    var Physics = $('#Physics').val();
    var Chemistry = $('#Chemistry').val();
    var Computer = $('#Computer').val();
    var English = $('#English').val();
    var Hindi = $('#Hindi').val();
    if (isValidNumber(Maths) && isValidNumber(Physics) && isValidNumber(Chemistry) && isValidNumber(Computer) && isValidNumber(English) && isValidNumber(Hindi)) {
        var data = {
            student_ID : studentID,
            Student_name : Student_name,
            Maths : $('#Maths').val(),
            Physics : $('#Physics').val(),
            Chemistry : $('#Chemistry').val(),
            Computer : $('#Computer').val(),
            English : $('#English').val(),
            Hindi : $('#Hindi').val(),
        }
        fetch(
            insert_marks_data_url,
            {
                method:'POST',
                credentials : 'same-origin',
                headers:{
                    "X-Requested-With":"XMLHttpRequest",
                    "X-CSRFToken" : getCookie("csrftoken"),
                },
                body : JSON.stringify({payload : data})
            }
        ).then(response=>response.json())
        .then(data=>{
            Swal.fire({
                position: "top-end",
                icon: "success",
                title: "Marks data has been saved",
                showConfirmButton: false,
                timer: 1500
              },{
                
              });
            reset_marks_form();
            $('#marks_info_table').empty()
            read_marks();
        });
    } else {
        Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "Input fields are either empty or the values entered are not numbers"
          });
    }
}
function set_marksID(marks_ID,Student_name,Maths,Physics,Chemistry,Computer,English,Hindi){
    $(`#marks_ID_`).text(marks_ID);
    StudentName = Student_name;
    $('#student_name').empty();
    $('#student_name').text(`${StudentName}'s marks`);
    var Maths = $('#Maths').val(Maths);
    var Physics = $('#Physics').val(Physics);
    var Chemistry = $('#Chemistry').val(Chemistry);
    var Computer = $('#Computer').val(Computer);
    var English = $('#English').val(English);
    var Hindi = $('#Hindi').val(Hindi);
}
function update_marks(){
    //marks ID is not updating even though it sends success response
    console.log(Number($(`#marks_ID_`).text()));
        var data = {
            marks_ID : Number($(`#marks_ID_`).text()),
            Maths : $('#Maths').val(),
            Physics : $('#Physics').val(),
            Chemistry : $('#Chemistry').val(),
            Computer : $('#Computer').val(),
            English : $('#English').val(),
            Hindi : $('#Hindi').val(),
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
                update_marks_data_url,
                {
                    method:'POST',
                    credentials : 'same-origin',
                    headers:{
                        "X-Requested-With":"XMLHttpRequest",
                        "X-CSRFToken" : getCookie("csrftoken"),
                    },
                    body : JSON.stringify({payload : data})
                }
            ).then(response=>response.json())
            .then(data=>{
                console.log(data);
                $('#marks_info_table').empty()
                read_marks();
                reset_marks_form();
                $(`#marks_ID_`).empty();
            });
            } else if (result.isDenied) {
              Swal.fire("Changes are not saved", "", "info");
            }
          });
}
/* insert update marks data ends */

/* Read Data starts*/
function read_marks(){
    fetch(
        read_marks_data_url,{
            method:'POST',
            credentials:'same-origin',
            headers:{
                'X-Requested-With':'XMLHttpRequest',
                'X-CSRFToken' : getCookie('csrftoken')
            }
        }
    ).then(response=>response.json())
    .then(data=>{
        for(var i=0;i<data.read_marks_data.length;i++){
            create_marks_table(data.read_marks_data[i],i,
                data.read_marks_settings[0].Total_marks_per_subject,
                data.read_marks_settings[0].passing_marks_per_subject,
                data.read_marks_settings[0].passing_percentage
                )
        }
    })
}
/* Read Data ends*/

/* Delete Marks starts */
function delete_marks(marks_ID){
    data = {
        marks_ID:marks_ID
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
            delete_marks_data_url,{
                method:'POST',
                credentials:'same-origin',
                headers:{
                    'X-Requested-With':'XMLHttpRequest',
                    'X-CSRFToken':getCookie("csrftoken")
                },
                body:JSON.stringify({payload:data})
            }
        ).then(request=>request.json())
        .then(data=>{
            console.log(data)
            $('#marks_info_table').empty()
            read_marks();
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
/* Delete Marks ends */
/* Marks CRUD operations ends */