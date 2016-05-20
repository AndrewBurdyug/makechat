var xhr = new XMLHttpRequest();
xhr.open('GET', '/api/ping', false);
xhr.send();
if (xhr.status == 401) location.replace('/login');
