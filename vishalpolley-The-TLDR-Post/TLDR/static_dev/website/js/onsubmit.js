$("#submit").on('click', function(e){    //submit button pressed
    e.preventDefault();
    if($("form")[0].checkValidity()){
    openNav();
    $('.overlay-content').html('<br/><br/><i style="text-align: center;" class="fa fa-spinner fa-pulse fa-3x fa-fw"></i>');
    $.ajax({
        type:"POST",
        url:"/",       // request handelling page
        data:{                        // data to be sent
            url:$('#search').val(),
        },
        dataType:"html",        // response return type of the page
        success : function(json) {
            $('#search').val(''); // remove the value from the input
            $('#results').html("<p> </p>"); // add the error to the dom
            $('.overlay-content').html('');
            var data = JSON.parse(json);
            var arr = $.map(data.summary, function(el) { return el });
            // console.log(data); // log the returned json to the console
            // console.log(data.url); 
            // console.log(data.summary);
            // console.log(data.title);
            if(data.summary == null){
                data.summary = "Sorry, We failed to fetch the News !!";
            }
            $(".overlay-content").prepend("<h3>"+data.title+"</h3><a href='"+data.url+"' target='_blank'>"+data.url+"</a><br/><p>"+data.summary+"</p><br/><br/>");
            // console.log("success"); // another sanity check
        },    
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            closeNav();
            $('#results').html("<p>Oops! We have encountered an error !!</p>"); // add the error to the dom
            // console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    })
}else{
    $('#results').html("<p>Please fill out the field !!</p>");
}
});  

$(document).keyup(function(e) {
    if (e.which == 27) {
        closeNav(); 
        $('#search').val('');
    }
});