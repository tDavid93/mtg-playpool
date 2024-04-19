import axios from 'axios';
const BASE_URL = 'http://localhost:8050/api';

export default axios.create({
    baseURL: BASE_URL
}); 

export const axiosPrivate = axios.create({
    baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8050/api',
    headers: { 'Content-Type': 'application/json' },
    withCredentials: true
});