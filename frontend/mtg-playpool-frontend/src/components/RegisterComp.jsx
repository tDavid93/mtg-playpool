import React, { useState, useRef } from 'react';
import axios from 'axios';
import UseAuth from '../hooks/useAuth';
import { Link, useNavigate, useLocation } from 'react-router-dom';

const RegisterComp = () => {
    const { setAuth } = UseAuth();  
  const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');


    const navigate = useNavigate();
    const location = useLocation();
    const from = location.state?.from?.pathname || "/";

        const userRef = useRef();
    const errRef = useRef();

    const [user, setUser] = useState('');
    const [pwd, setPwd] = useState('');
    const [errMsg, setErrMsg] = useState('');

    const handleEmailChange = (e) => {
      setUsername(e.target.value);
    };

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    };

    const handleSubmit = async (e) => {
      e.preventDefault();
      console.log('username: ', username);
      console.log('password: ', password);
      try {
        const response = await axios.post(
            '/api/signup',
                    {
                    username: username,
                    password: password
                    },
                    {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                      }});
        console.log('response: ', response.data);
        
        navigate('/login', { replace: true });
      } catch (error) {
        // Handle login error
      }
    };

    return (
      <div>
        <h2>Signup</h2>
        <form onSubmit={handleSubmit}>
          <label>username</label>
          <input type="text" value={username} onChange={handleEmailChange} />
          <br />
          <label>Password:</label>
          <input type="password" value={password} onChange={handlePasswordChange} />
          <br />
          <button type="submit">Register</button>
        </form>
      </div>
    );
  };

  export default RegisterComp;