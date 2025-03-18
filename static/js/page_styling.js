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
    $(".leaderboard-container").addClass("w-[650px] max-h-[250px] border-[3px] border-zinc-900 mx-auto rounded bg-gray-900 mt-[5%] text-gray-300 font-semibold")
    $(".leaderboard-categories").addClass("flex border-b-[3px] border-zinc-950")
    $(".leaderboard-categories-option").addClass("select-none cursor-pointer text-center w-1/3 hover:bg-green-700")
    //home.html: searchbar
    $(".leaderboard-search").addClass("border-b-[2px] pl-1 border-zinc-950 pt-[2px] pb-[2px]")
    $(".leaderboard-search-box").addClass("rounded-lg w-32 pl-2 pr-2")
    //home.html: entry
    $(".leaderboard-entry").addClass("flex h-full border-b-[2px] [&_:is(span)]:pl-[3px] border-zinc-950");
    $(".leaderboard-entry-title").addClass("border-b-[3px]")
    $(".leaderboard-position").addClass("w-1/12 flex-none border-r-[3px] border-zinc-950")
    $(".leaderboard-username").addClass("w-1/2 flex-1 border-r-[3px] border-zinc-950")
    $(".leaderboard-listening-time").addClass("w-1/3 flex-1")

    //home.html/profile.html
    $(".page-splitter").addClass("flex h-full")

    //friends.html
    $(".friends").addClass("h-[100px] overflow-auto")
    $(".friends-container").addClass("w-[650px] max-h-[250px] border-[3px] border-zinc-900 mx-auto rounded bg-gray-900 mt-[5%] text-gray-300 font-semibold")
    $(".friends-entry").addClass("border-t-[2px]")
    $(".friends-friend").addClass("w-1/2 flex-1 border-r-[3px] border-zinc-950")

    //Log_in.html/ signup.html Styling
    $(".login-and-create-account-form").addClass("ps-40 pt-8")
    $(".input-title").addClass("input-title w-24 text-right text-green-50 font-semibold")
    $(".input-container").addClass("flex space-x-8")
    $(".text-field").addClass("w-64 border-zinc-950 rounded px-2 py-1 mb-2")
})

//home.html leaderboard category buttons handling 
//doesn't work currently
$(".leaderboard-categories-option").click(function() {
    let options = $(".leaderboard-categories").children();

    console.log("this is running")
    options.each(function() {
        $(this).removeClass("bg-blue-700"); // Remove the class from all siblings
    });


    $(this).addClass("bg-blue-700"); // Add the class to the clicked element
});

// friends.html list of users