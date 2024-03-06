var data_ ;
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
$('body').ready(function(){
    var data = {
        student_name:$('#student_name').text(),
        email:$('#email').text(),
    Maths : $(`#Maths`).text(),
    Physics : $(`#Physics`).text(),
    Chemistry : $(`#Chemistry`).text(),
    Computer : $(`#Computer`).text(),
    English : $(`#English`).text(),
    Total_marks_obtained : $(`#Total_marks_obtained`).text(),
    Total_Marks : $(`#Total_Marks`).text(),
    Percentage : $(`#Percentage`).text(),
    passing_percentage : $(`#passing_percentage`).text(),
    pass_fail : $(`#pass_fail`).text(),
    date : $('#date').text(),
    no_of_days_present : $('#no_of_days_present').text(),
    }
    data_  = data
})
function create_marks_card(marks){
    var icon = `<i class="fa-solid fa-xmark text-danger"></i>`;
    if(marks.pass_fail == "True"){
        icon = `<i class="fa-solid fa-check text-success"></i>`;
    }
    else{
        icon = `<i class="fa-solid fa-xmark text-danger"></i>`;
    }
    $('#marks_card').append(
        `
        <div class="card-deck">
        <div class="card mb-4" style="width: 22rem;">
            <div class="card-body">
              <h5 class="card-title">${marks.student_name}'s Marks</h5>
              <h6 class="card-subtitle mb-2 text-muted">Marks Detail</h6>
              <div class="row">
                <p class="card-text">Maths : ${marks.Maths}</p>
            </div>
            <div class="row">
                <p class="card-text">Physics : ${marks.Physics}</p>
            </div>
            <div class="row">
                <p class="card-text">Chemistry : ${marks.Chemistry}</p>
            </div>
            <div class="row">
                <p class="card-text">Computer : ${marks.Computer}</p>
            </div>
            <div class="row">
                <p class="card-text">English : ${marks.English}</p>
            </div>
            <div class="row">
                <p class="card-text">Hindi : ${marks.English}</p>
            </div>
            <div class="row">
                <p class="card-text">Total_marks_obtained : ${marks.Total_marks_obtained}</p>
            </div>
            <div class="row">
                <p class="card-text">Total_Marks : ${marks.Total_Marks}</p>
            </div>
            <div class="row">
                <p class="card-text">Percentage : ${marks.Percentage}</p>
            </div>
            <div class="row">
                <p class="card-text">passing_percentage : ${marks.passing_percentage}</p>
            </div>
            <div class="row">
                <p class="card-text">Pass : ${icon}</p>
            </div>
              <button class="btn btn-primary my-1" id="hide_marks">Hide</button>
              <button class="btn btn-primary my-1" id="send_marks">Send Marks</button>
            </div>
          </div>
    </div>
        `
    )
}
$('body').on('click','#show_marks',function(){
    show_marks();
})
function show_marks(){
    if (data_.Maths == "" && data_.Physics == "" && data_.Chemistry == "" && data_.Computer == "" && data_.English == "" && data_.Total_marks_obtained == "" && data_.Total_Marks == "" && data_.Percentage == "" && data_.passing_percentage == "" && data_.pass_fail == ""){
        Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "Marks does not exist!"
          });
    }
    else{
        create_marks_card(data_)
    }
}
$('body').on('click','#hide_marks',function(){
    $('#marks_card').empty()
    $('#marks_card').empty()
})

$('body').on('click','#show_attendance',function(){
    show_attendance();
})
function show_attendance(){
    if (data_.date == "" && data_.no_of_days_present == ""){
        Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "Attedance does not exist!"
          });
    }
    else{
        create_attendance_card(data_)
    }
}
function create_attendance_card(attendance){
    $('#attendance_card').append(
        `
        <div class="card-deck">
        <div class="card mb-4" style="width: 22rem;">
            <div class="card-body">
              <h5 class="card-title">${attendance.student_name}'s attendance</h5>
              <h6 class="card-subtitle mb-2 text-muted">Marks Detail</h6>
              <div class="row">
                <p class="card-text">Maths : ${attendance.date}</p>
            </div>
            <div class="row">
                <p class="card-text">Physics : ${attendance.no_of_days_present}</p>
            </div>
              <button class="btn btn-primary my-1" id="hide_attendance">Hide</button>
            </div>
          </div>
    </div>
        `
    )
}
$('body').on('click','#hide_attendance',function(){
    $('#attendance_card').empty()
})
/* Send email using SMTP from django using Gmail account */
$('body').on('click','#send_marks',function(){
    send_marksSMTP(data_.email, data_.student_name, data_.Maths, data_.Physics, data_.Chemistry, data_.Computer, data_.English, data_.Total_marks_obtained, data_.Total_Marks, data_.Percentage, data_.passing_percentage, data_.pass_fail)
})
function send_marksSMTP(email, student_name, Maths, Physics, Chemistry, Computer, English, Total_marks_obtained, Total_Marks, Percentage, passing_percentage, pass_fail){
    console.log(email)
    var data = {
        email : email,
        student_name:student_name,
        Maths:Maths,
        Physics:Physics,
        Chemistry:Chemistry,
        Computer:Computer,
        English:English,
        Total_marks_obtained:Total_marks_obtained,
        Total_Marks:Total_Marks,
        Percentage:Percentage,
        passing_percentage:passing_percentage,
        pass_fail:pass_fail,
    }
    fetch(
        send_email_url,{
            method:'POST',
            credentials:'same-origin',
            headers:{
                'X-Requested-With':'XMLHttpRequest',
                'X-CSRFToken' : getCookie('csrftoken')
            },
            body:JSON.stringify({payload:data})
        }
    ).then(request=>request.json())
    .then(data=>{
        console.log(data)
        Swal.fire({
            position: "top-end",
            icon: "success",
            title: "Marks sent!!",
            showConfirmButton: false,
            timer: 1500
          },{
            
          });
    })
}
/* Send email using SMTP from django using Gmail account */