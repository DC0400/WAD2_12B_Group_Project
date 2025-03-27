const clientId = "8033023b2d8c496195b5c1c161d0e825";
const params = new URLSearchParams(window.location.search);
const code = params.get("code");

//localStorage.clear();

//let accessToken = localStorage.getItem("access_token");
// if (!accessToken) {
    if (!code) {
        redirectToAuthCodeFlow(clientId);
    } else {
        getAccessToken(clientId, code).then(token => {
            if (token) {
                localStorage.setItem("access_token", token);
                loadData(token);
            } else {
                console.error("Failed to retrieve access token");
            }
        });
    }
// } else {
//     loadData(accessToken);
// }

async function loadData(token) {
    const profile = await fetchProfile(token);
    //console.log(profile);
    sendProfileToServer(profile);
    if(populateUI(profile)){
        sendPhotoToServer(profile);
    }
    sendSpotifyUsernameToServer(profile);

    const topTracks = await fetchTopTracks(token);
    sendDataToServer(topTracks);
    populateSongs(topTracks.items)

    const listeningMinutes = await fetchMinutes(token);
    sendDataToServerMinutes(listeningMinutes.items);
    calculateMinutes(listeningMinutes.items);
}

export async function redirectToAuthCodeFlow(clientId){
    const verifier = generateCodeVerifier(128);
    const challenge = await generateCodeChallenge(verifier);

    localStorage.setItem("verifier", verifier);

    const params = new URLSearchParams();
    params.append("client_id", clientId);
    params.append("response_type", "code");
    params.append("redirect_uri", "http://127.0.0.1:8000/callback");
    params.append("scope", "user-read-private user-read-email user-top-read user-read-recently-played");
    params.append("code_challenge_method", "S256");
    params.append("code_challenge", challenge);

    document.location = `https://accounts.spotify.com/authorize?${params.toString()}`;
}

function generateCodeVerifier(length) {
    let text = '';
    let possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

    for (let i = 0; i < length; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
}

async function generateCodeChallenge(codeVerifier) {
    const data = new TextEncoder().encode(codeVerifier);
    const digest = await window.crypto.subtle.digest('SHA-256', data);
    return btoa(String.fromCharCode.apply(null, [...new Uint8Array(digest)]))
        .replace(/\+/g, '-')
        .replace(/\//g, '_')
        .replace(/=+$/, '');
}

export async function getAccessToken(clientId, code) {
    const verifier = localStorage.getItem("verifier");

    const params = new URLSearchParams();
    params.append("client_id", clientId);
    params.append("grant_type", "authorization_code");
    params.append("code", code);
    params.append("redirect_uri", "http://127.0.0.1:8000/callback");
    params.append("code_verifier", verifier);

    const result = await fetch("https://accounts.spotify.com/api/token", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: params
    });

    const data = await result.json();

    if (data.access_token) {
        //localStorage.setItem("access_token", data.access_token); // Save token
        return data.access_token;
    } else {
        console.error("Error getting access token:", data);
        return null;
    }
}

async function fetchTopTracks(token) {
    const response = await fetch("https://api.spotify.com/v1/me/top/tracks?time_range=short_term&limit=10", {
        method: "GET",
        headers: { Authorization: `Bearer ${token}` }
    });

    const data = await response.json();

    if (!data.items) {
        console.error("Error fetching top tracks:", data);
        return null;
    }

    return data;

    // const totalListeningTimeMs = data.items.reduce((sum, track) => sum + track.duration_ms, 0);
    // const totalListeningMinutes = Math.round(totalListeningTimeMs / 60000);
    //
    // console.log(`Total listening time: ${totalListeningMinutes} minutes`);
    //
    // return { tracks: data.items, totalListeningMinutes };
}

async function fetchProfile(token) {
    const result = await fetch("https://api.spotify.com/v1/me", {
        method: "GET", headers: { Authorization: `Bearer ${token}` }
    });

    return await result.json();
}

async function fetchMinutes(token){
    let url = new URL("https://api.spotify.com/v1/me/player/recently-played?limit=50")
    url.searchParams.append('before', Date.now().toString());

    const result = await fetch(url.toString(), {
        method: "GET",
        headers: { Authorization: `Bearer ${token}` }
    });

    const minutes = await result.json();

    if (!minutes.items) {
        console.error("Error fetching top tracks:", minutes);
        return null;
    }

    return minutes
}

async function sendDataToServer(data) {
    const response = await fetch("http://127.0.0.1:8000/rankedify/api/receive_tracks/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        console.log("Data successfully sent to the server.");
    } else {
        console.error("Failed to send data to the server.");
    }
}

async function sendDataToServerMinutes(data) {
    let totalMinutes = 0;

    data.forEach(items => {
        totalMinutes += items.track.duration_ms;
    })

    //totalMinutes = totalMinutes / 60000;
    totalMinutes = Math.round(totalMinutes / 60000);

    const response = await fetch("http://127.0.0.1:8000/rankedify/api/receive_minutes/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(totalMinutes)
    });

    if (response.ok) {
        console.log("Data successfully sent to the server.");
    } else {
        console.error("Failed to send data to the server.");
    }
}

async function sendProfileToServer(data) {
    const response = await fetch("http://127.0.0.1:8000/rankedify/api/receive_profile/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    if (response.ok) {
        console.log("Data successfully sent to the server.");
    } else {
        console.error("Failed to send data to the server.");
    }
}

async function sendPhotoToServer(data){
    let url = data.images[0].url;
    const response = await fetch("http://127.0.0.1:8000/rankedify/api/receive_photo/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(url)
    })

    if (response.ok) {
        console.log("Data successfully sent to the server.");
    } else {
        console.error("Failed to send data to the server.");
    }
}

async function sendSpotifyUsernameToServer(data){
    let spotify_username = data.id;
    const response = await fetch("http://127.0.0.1:8000/rankedify/api/receive_spotify_username/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(spotify_username)
    })

    if (response.ok) {
        console.log("Data successfully sent to the server.");
    } else {
        console.error("Failed to send data to the server.");
    }
}

// function populateUI(profile){
//     document.getElementById("displayName").innerText = profile.display_name;
//     if (profile.images[0]) {
//         const profileImage = new Image(200, 200);
//         profileImage.src = profile.images[0].url;
//         document.getElementById("avatar").appendChild(profileImage);
//         document.getElementById("imgUrl").innerText = profile.images[0].url;
//     }
//     document.getElementById("id").innerText = profile.id;
//     document.getElementById("email").innerText = profile.email;
//     document.getElementById("uri").innerText = profile.uri;
//     document.getElementById("uri").setAttribute("href", profile.external_urls.spotify);
//     document.getElementById("url").innerText = profile.href;
//     document.getElementById("url").setAttribute("href", profile.href);
// }

function populateUI(profile){
    //document.getElementById("displayName").innerText = profile.display_name;
    if(profile.images[0]){
        const profileImage = new Image(200, 200);
        profileImage.src = profile.images[0].url;
        document.getElementById("avatar").appendChild(profileImage);
        //document.getElementById("imgUrl").innerText = profile.images[0].url;

        return true;
    }
    //document.getElementById("id").innerText = profile.id;
}

function populateSongs(top_songs){
    const trackList = document.getElementById("track-list");
    trackList.innerHTML = "";

    top_songs.forEach(track => {
        const trackElement = document.createElement("div");
        trackElement.innerHTML = `
            <img src="${track.album.images[0].url}" width="50"  alt="Album Art"/>
            <strong>${track.name}</strong> - ${track.artists.map(artist => artist.name).join(", ")}
        `;
        trackList.appendChild(trackElement);
    });
}

function calculateMinutes(recentlyListened){
    let totalMinutes = 0;

    recentlyListened.forEach(items => {
        totalMinutes += items.track.duration_ms;
    })

    //totalMinutes = totalMinutes / 60000;
    totalMinutes = Math.round(totalMinutes / 60000);

    // const elements = document.getElementById("listeningMinutes");
    // elements.innerHTML = "";
    //
    // recentlyListened.forEach(items => {
    //     const element = document.createElement("div");
    //     element.innerHTML = `
    //         <strong>${items.track.duration_ms}</strong><br>
    //     `;
    //     elements.appendChild(element)
    // });

    document.getElementById("listeningMinutes").innerHTML = totalMinutes.toString() + " Minutes";
}