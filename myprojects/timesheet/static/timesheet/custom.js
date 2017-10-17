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


$(document).on('click',"a.timesheetlist",function(event){
    event.preventDefault();
    updateURL = "/timesheetset1/" + this.id;
    console.log(updateURL);
    $.ajax({
        type:"GET",
        url: updateURL,
        success: function(result){
            console.log('trying to open modal');
            $("#div2").html(result);
            $('#Modal2').modal();
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
    $(document).on('submit','.timesheetsetAjaxForm',function(event){
            event.preventDefault();
            console.log("form submitted!  Update a Car works");
            $.ajax({
                type:"POST",
                url: "/timesheetset1/" + this.id+ "/",
                data:$('.timesheetsetAjaxForm').serialize(),
                success: function(result){
                console.log("form posted!  Update a Car works");
                $('#Modal2').modal('hide');
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


//------------------------------------------------------------
// jQuery for arrow keys and editing idea from here:
// http://stackoverflow.com/questions/22817451/use-arrow-keys-to-navigate-an-html-table

var currCell = $('td').first();
var editing = false;

// User clicks on a cell
$('td').click(function () {
    currCell = $(this);

    var col = $(this).parent().children().index($(this)) + 1;
    var row = $(this).parent().parent().children().index($(this).parent()) + 1;
    // alert('Row: ' + row + ', Column: ' + col + ', Value: ' + currCell.html());
    // console.log(col);
    // console.log(row);
    //   edit();
});

// Show edit box
function edit() {
    editing = true;
    currCell.toggleClass("editing");
    $('#edit').show();
    $('#edit #text').val(currCell.html());
    $('#edit #text').select();
}

// User saves edits
$('#edit form').submit(function (e) {
    editing = false;
    e.preventDefault();
    // Ajax to update value in database
    $.get('#', '', function () {
        $('#edit').hide();
        currCell.toggleClass("editing");
        currCell.html($('#edit #text').val());
        currCell.focus();
    });
});

// User navigates table using keyboard
//$('table').keydown(function (e) {
$('table#example1').keydown(function (e) {
    //$('ul#example1 li').keydown(function (e) {
    //alert(2);
    console.log('keypressed in table');
    var c = "";
    if (e.which == 39) {
        // Right Arrow
        c = currCell.next();
    } else if (e.which == 37) {
        // Left Arrow
        c = currCell.prev();
    } else if (e.which == 38) {
        // Up Arrow
        c = currCell.closest('tr').prev().find('td:eq(' + currCell.index() + ')');
    } else if (e.which == 40) {
        // Down Arrow
        c = currCell.closest('tr').next().find('td:eq(' + currCell.index() + ')');
    } else if (!editing && (e.which == 13 || e.which == 32 || e.which == 113)) {
        // Enter, Spacebar, F2 - edit cell
        e.preventDefault();
        edit();
    } else if (!editing && (e.which == 9 && !e.shiftKey)) {
        // Tab
        e.preventDefault();
        c = currCell.next();
    } else if (!editing && (e.which == 9 && e.shiftKey)) {
        // Shift + Tab
        e.preventDefault();
        c = currCell.prev();
    }

    // If we didn't hit a boundary, update the current cell
    if (c.length > 0) {
        currCell = c;
        currCell.focus();
    }
});

// User can cancel edit by pressing escape
$('#edit').keydown(function (e) {
    if (editing && e.which == 27) {
        editing = false;
        $('#edit').hide();
        currCell.toggleClass("editing");
        currCell.focus();
    }
});
