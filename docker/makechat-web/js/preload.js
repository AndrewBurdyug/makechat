var xhr = new XMLHttpRequest();
var user = null;
xhr.open('GET', '/api/ping', false);
xhr.send();
if (xhr.status == 401) location.replace('/login');
if (xhr.status == 200) user = JSON.parse(xhr.responseText);
