$(document).ready(function() {
    //Styling used on each page
    $("html").addClass("bg-gradient-to-b from-green-800 h-full to-green-400");
    $("body").addClass("bg-gradient-to-b from-green-800 h-full to-green-400");
    $(".link").addClass("font-medium text-zinc-950 underline italic hover:no-underline")
    $(".button").addClass("bg-green-500 hover:bg-green-700 text-white font-bold py-1 px-1 rounded")
    $("#page-body").addClass("h-[91%]")

    //nav bar
    $("nav").addClass("mx-auto bg-gray-800 flex w-full h-[9%] select-none");
    $("#logo").addClass("px-4 text-green-500 font-semibold h-full flex items-center cursor-default");
    $(".nav-item").addClass("px-4 text-green-50 font-semibold h-full cursor-pointer hover:bg-green-600 transition duration-300 flex items-center");
    
    //home.html
    $(".leaderboard-container").addClass("min-w-[650px] max-h-[250px] min-h-[250px] border-[3px] border-zinc-900 mx-auto rounded bg-gray-900 mt-[5%] mb-[5%] lg:mb-[0%] text-gray-300 font-semibold");
    //home.html: searchbar
    $(".leaderboard-search").addClass("border-b-[2px] pl-1 border-zinc-950 pt-[2px] pb-[2px]")
    $(".leaderboard-search-box").addClass("rounded-lg w-32 pl-2 pr-2")
    //home.html: entry
    $(".leaderboard").addClass("relative h-[89%]")
    $(".non-user-entries").addClass("overflow-auto h-[60%]")
    $(".leaderboard-user-entry").addClass("flex h-12 w-full border-t-[2px] [&_:is(span)]:pl-[3px] bg-gray-800 border-zinc-950 absolute bottom-0")
    $(".leaderboard-entry").addClass("flex h-12 border-b-[2px] [&_:is(span)]:pl-[3px] border-zinc-950");
    $(".leaderboard-entry-title").addClass("border-b-[3px]")
    $(".leaderboard-position").addClass("w-1/12 flex-none border-r-[3px] border-zinc-950")
    $(".leaderboard-username").addClass("w-1/2 flex-1 border-r-[3px] border-zinc-950 pt-[12px]")
    $(".leaderboard-listening-time").addClass("w-1/3 flex-1 pt-[12px]")

    //home.html/profile.html
    $(".page-splitter").addClass("flex flex-col justify-center lg:justify-normal lg:flex-row h-full")
    $(".page-seperator-line").addClass("border-b lg:border-l")
    $(".graph").addClass("max-w-[510px] h-max-[250px] h-min-[250px] mx-auto bg-gray-900 mt-[5%] p-[px] rounded")

    //error-page.html
    $(".message-container").addClass("m-auto w-96")
    $("h2").addClass("text-lg")

    //profile.html
    $(".profile-info-container").addClass("max-w-[500px] flex justify-between space-x-4")
    $(".field-title").addClass("self-start")
    $(".text-field").addClass("self-end")
    $(".edit-button").addClass("w-40")
    //Top songs
    $("#top_songs_title").addClass()
    $("#top_songs").addClass("h-[400px] w-[400px] overflow-auto")
    $(".profile-info-container").addClass("w-full")

    //friends.html
    $(".friends-page-content").addClass("mt-[5%] ml-[5%]")
    $(".user-table").addClass("w-[650px] max-h-[250px] border-[3px] border-zinc-900 rounded bg-gray-900 text-gray-300 font-semibold mb-12")
    $(".user-entries").addClass("h-[100px] overflow-auto")
    $(".friends-entry").addClass("border-t-[2px] cursor-pointer hover:bg-gray-700")
    $(".friends-title").addClass("rounded-tl")
    $(".user-lists").addClass("h-[100px] overflow-auto")
    $(".user-entry").addClass("w-1/2 flex-1 border-zinc-950")

    //Log_in.html/ signup.html Styling
    $(".login-and-create-account-form").addClass("ps-40 pt-8")
    $(".input-title").addClass("w-24 text-right text-green-50 font-semibold")
    $(".input-container").addClass("flex space-x-8")
    $(".text-field").addClass("w-64 border-zinc-950 rounded px-2 py-1 mb-2")
})

