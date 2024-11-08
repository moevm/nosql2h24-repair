import axios from 'axios'
/* eslint-disable */
async function sendDataRegistration(data) {
    try {
        // Отправляем данные на сервер
        const response = await axios.post('http://172.18.0.4:8000/api/auth/register', data, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        console.log('Data sent successfully:', response.data);
    } catch (error) {
        console.error('Error sending data:', error);
    }
}