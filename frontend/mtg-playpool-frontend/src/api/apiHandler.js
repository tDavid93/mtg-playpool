import axios from 'axios';
import {Navigate} from 'react-router-dom';


const fetchLocalToken = () => {
    const token = localStorage.getItem('token');
    if (token) {
        {<Navigate to="/login" />}
    }
    return token;
    }

const apiHandler = axios.create({
    baseURL: 'http://localhost:8050/api',
    headers: {
        Authorization: fetchLocalToken(),
    },
});

export default apiHandler;

