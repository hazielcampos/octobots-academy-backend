const loginForm = document.querySelector('#loginForm');
const registerForm = document.querySelector('#registerForm');

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = loginForm.username.value;
    const password = loginForm.password.value;

    const response = await fetch('http://localhost:8000/auth/login/', {
        method: 'POST',
        headers: {
            'Content-Type': "x-www-form-urlencoded",
        },
        body: new URLSearchParams({
            username: username,
            password: password
        })
    });

    const data = await response.json();
    if (response.ok) {
        alert('Login successful!');
    } else {
        alert('Login failed: ' + data.detail);
    }
});