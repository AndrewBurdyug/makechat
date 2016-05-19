var xhr = new XMLHttpRequest();
xhr.open('GET', '/api/home', false);
xhr.send();
if (xhr.status == 401) location.replace('/login');
