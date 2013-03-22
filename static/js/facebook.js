// facebook.js
FB.init({
    appId: '268986189900174',
    frictionlessRequests: true,
    status: true,
    cookie: true
});

function sendRequestViaMultiFriendSelector () {
    FB.ui({
        method: 'apprequests',
        message: 'Check out Silk Tradr!'
    }, requestCallback);
}

function requestCallback (response) {
    // Handle callback here
    console.log(response)
}

function postToFeed (opts) {
    // calling the API ...
    var obj = {
        method: 'feed',
        redirect_uri: 'http://www.silktradr.com',
        link: 'http://www.silktradr.com',
        picture: 'PICTURE FROM LISTING',
        name: 'Silk Tradr',
        caption: 'LISTING DESCRIPTION',
        description: 'TITLE OF LISTING'
    };

    for (var k in obj) {
        if (opts[k]) {
            obj[k] = opts[k]
        }
    }

    function callback (response) {
        document.getElementById('msg').innerHTML = "Post ID: " + response['post_id'];
    }

    FB.ui(obj, callback);
}

