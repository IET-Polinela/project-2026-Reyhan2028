const BASE_URL = 'http://127.0.0.1:8000';

function requestAPI(endpoint, method = 'GET', bodyData = null) {
    const headers = {
        'Content-Type': 'application/json'
    };

    const token = localStorage.getItem('access_token');
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const config = {
        method: method,
        headers: headers
    };

    if (bodyData) {
        config.body = JSON.stringify(bodyData);
    }

    return fetch(`${BASE_URL}${endpoint}`, config)
        .then(response => {
            if (!response.ok) {
                throw new Error('Gagal melakukan permintaan ke server API.');
            }
            if (response.status === 204) return null;
            return response.json();
        });
}