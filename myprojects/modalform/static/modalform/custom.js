    function updateList(){
        $.ajax({
            type:"GET",
            url: "/modalform/",
            success: function(result){
                console.log(result);
                $("#carlist").html(result);
        }});
    }


$(document).on('click',"#createcar",function(event){
    event.preventDefault();
    $.ajax({
        type:"GET",
        url: "/modalform/create/",
        success: function(result){
        $("#div1").html(result);
        $('#Modal1').modal();
    }});
});


$(document).on('click',"a",function(event){
    event.preventDefault();
    // updateURL = "/timesheetset1/" + this.id;
    updateURL = "/modalform/update/" + this.id;

    console.log(updateURL);
    $.ajax({
        type:"GET",
        url: updateURL,
        success: function(result){
            console.log('trying to open modal');
            $("#div1").html(result);
            $('#Modal1').modal();
    }});
});
// <!-- Create a Car works -->
    $(document).on('submit','#createcarform',function(event){
            event.preventDefault();
            // console.log(url);
            console.log("form submitted! Create a Car works");
            $.ajax({
                type:"POST",
                url: "/modalform/create/",
                data:$('#createcarform').serialize(),
                success: function(result){
                    console.log("form posted! Create a Car works");
                    $("#Modal1").modal('hide');
                    updateList();
            }});
        });

// <!-- Update a Car works -->
    $(document).on('submit','.carupdateform',function(event){
            event.preventDefault();
            console.log("form submitted!  Update a Car works");
            $.ajax({
                type:"POST",
                url: "/modalform/updatee/" + this.id,
                data:$('.carupdateform').serialize(),
                success: function(result){
                console.log("form posted!  Update a Car works");
                $('#Modal1').modal('hide');
                updateList();
            }});
        });


        // using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
