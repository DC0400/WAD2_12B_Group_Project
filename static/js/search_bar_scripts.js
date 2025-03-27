$(document).ready(function() {
    //Leaderboard user-search
    $(".leaderboard-search-box").on("input", function() {
        let searchText = $(".leaderboard-search-box").val()
        $(".non-user-entries").children().each(function () {
            if ($(this).children(".leaderboard-username").text().toLowerCase().replace(/ /g,'').startsWith(searchText,0)) {
                $(this).show()
            } else {
                $(this).hide()
            }
        })
    })

    $("#user-search").on("input", function() {
        let searchText = $("#user-search").val()
        $("#user-entries").children().each(function() {
            if ($(this).children().eq(0).text().toLowerCase().replace(/ /g,'').startsWith(searchText,0)) {
                $(this).show()
            } else {
                $(this).hide()
            }
        })
    })
})