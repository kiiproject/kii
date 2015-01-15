// Foundation JavaScript
// Documentation can be found at: http://foundation.zurb.com/docs
$(document).foundation();


// hide/show navigation 

$('#show-nav').on('click', function(e){
    $('body').toggleClass('show-nav');
    e.preventDefault();
});