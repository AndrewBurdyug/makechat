setInterval(function (){
    xhr.open('GET', '/api/ping', true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return;
        if (xhr.status == 401) location.replace('/login');
    };
    xhr.send();
}, 60000);
