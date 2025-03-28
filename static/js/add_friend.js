async function toggleFriendButtonStatus(friendButton) {
        let button_text = friendButton.textContent || friendButton.innerText;

        if (button_text == "Add Friend") {
            console.log(window.location.origin);
            const result = await fetch(window.location.origin + "/rankedify/add_friend/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(username_var)
            });

            if (result.ok) {
                console.log("Data successfully sent to the server.");

                friendButton.textContent = "Unfriend"
                friendButton.innerText = "Unfriend"
            } else {
                console.error("Failed to send data to the server.");
            }
        } else {
            friendButton.textContent = "Add Friend"
            friendButton.innerText = "Add Friend"
        }
    }