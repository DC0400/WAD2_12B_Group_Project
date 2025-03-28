async function toggleFriendButtonStatus(friendButton) {
        let button_text = friendButton.textContent || friendButton.innerText;

        if (button_text.includes("Add Friend")) {
            const result = await fetch(window.location.origin + "/new_friend/", {
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
            const result = await fetch(window.location.origin + "/remove_friend/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(username_var)
            });

            if (result.ok) {
                console.log("Data successfully sent to the server.");

                friendButton.textContent = "Add Friend"
                friendButton.innerText = "Add Friend"
            } else {
                console.error("Failed to send data to the server.");
            }
        }
    }