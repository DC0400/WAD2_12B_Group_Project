$(document).ready(function() {
    //Styling used on each page
    $("html").addClass("bg-gradient-to-b from-green-800 h-full to-green-400");
    $("body").addClass("bg-gradient-to-b from-green-800 h-full to-green-400");
    $(".link").addClass("font-medium text-zinc-950 underline italic hover:no-underline")
    $(".button").addClass("bg-green-500 hover:bg-green-700 text-white font-bold py-1 px-1 rounded")

    //nav bar
    $("nav").addClass("mx-auto bg-gray-800 flex w-full h-16 select-none");
    $("#logo").addClass("px-4 text-green-500 font-semibold h-full flex items-center cursor-default");
    $(".nav-item").addClass("px-4 text-green-50 font-semibold h-full cursor-pointer hover:bg-green-600 transition duration-300 flex items-center");
    
    //home.html
    $(".leaderboard-container").addClass("w-[500px] border mx-auto rounded bg-blue-500")
    $(".leaderboard-categories").addClass("flex border-b")
    $(".leaderboard-categories-option").addClass("cursor-pointer hover:bg-blue-700 w-1/3")
    $(".leaderboard-search").addClass("border-b-[2px] border-zinc-950 pt-[2px] pb-[2px]")
    $(".leaderboard-search-box").addClass("rounded-lg w-32 pl-2 pr-2")
    $(".leaderboard-entry").addClass("flex space-x-4 h-full");
    $(".leaderboard-position").addClass("w-1/6 flex-none")
    $(".leaderboard-username").addClass("w-1/2 flex-1")
    $(".leaderboard-listening-time").addClass("w-1/3 flex-1")

    //Log_in.html/ signup.html Styling
    $(".login-and-create-account-form").addClass("ps-40 pt-8")
    $(".input-title").addClass("input-title w-24 text-right text-green-50 font-semibold")
    $(".input-container").addClass("flex space-x-8")
    $(".text-field").addClass("w-64 border rounded px-2 py-1 mb-2")
})