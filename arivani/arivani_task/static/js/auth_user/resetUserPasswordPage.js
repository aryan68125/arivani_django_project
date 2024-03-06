$('body').on('click','#verifyLink',function(){
    var username = $('username').val()
    data = {
        username:username
    }
    validate(data)
})
function validate(data){
    if (data.username == ""){
        Swal.fire({
            icon: "error",
            title: "Error...",
            text: "username needed!",
          });
    }
    else{
        send_data(data)
    }
}
function send_data(data){
    fetch(
    n6
    )
}