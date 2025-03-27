$(document).ready( function() {
    var isReadonly = true;
    $(".edit-button").on("click", function() {
        if (isReadonly){
            $(this).html("Save")
            $("#favourite-song").removeAttr("readonly")
            isReadonly = false;
        } else {
            $(this).html("Edit")
            $("#favourite-song").attr('readonly', true)
            isReadonly = true;
        }
    });
});