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
            let text = $("#favourite-song").val()
            postSave(text)
            isReadonly = true;
        }
    });
});

async function postSave(text){
    const result = await fetch(window.location.origin + "/rankedify/profile/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            //"X=CSRFToken": getCSRFToken()
        },
        body: JSON.stringify(text)
    });

    if(result.ok){
        console.log("Data successfully sent to the server.");
    } else {
        console.error("Failed to send data to the server.");
    }
}

function getCSRFToken(){
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith("csrftoken=")) {
                cookieValue = cookie.substring("csrftoken=".length, cookie.length);
                break;
            }
        }
    }
    return cookieValue;
}