import React, { useState, useRef } from 'react';
import axios from 'axios';
import UseAuth from '../hooks/useAuth';
import { Link, useNavigate, useLocation } from 'react-router-dom';

const LoginComp = () => {
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
            '/api/login',
                    {
                    username: username,
                    password: password
                    },
                    {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                      }});
        console.log('response: ', response.data.access_token);
        const accessToken = response.data.access_token;
        //TODO - get user info from backend
        const roles = 1;
        setAuth({ user, pwd, roles, accessToken });
        setUser('');
        setPwd('');
        navigate(from, { replace: true });
      } catch (error) {
        // Handle login error
      }
    };

    return (
      <div>
        <h2>Login</h2>
        <form onSubmit={handleSubmit}>
          <label>username</label>
          <input type="username" value={username} onChange={handleEmailChange} />
          <br />
          <label>Password:</label>
          <input type="password" value={password} onChange={handlePasswordChange} />
          <br />
          <button type="submit">Login</button>
        </form>
      </div>
    );
  };

  export default LoginComp;