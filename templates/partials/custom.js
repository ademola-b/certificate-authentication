$(document).ready(function(){
    $('#print').click(function(){
        console.log("print");
        $('#cert').printThis();
    })
})