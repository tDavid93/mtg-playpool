import React, { useState } from 'react';
import axios from 'axios';

const LoginComp = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

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
        console.log('response: ', response);
        const accessToken = response.data.accessToken;
        localStorage.setItem('accessToken', accessToken);
        window.location.replace("/");
        // Handle successful login
      } catch (error) {
        // Handle login error
      }
    };

    return (
      <div>
        <h2>Login</h2>
        <form onSubmit={handleSubmit}>
          <label>username</label>
          <input type="text" value={username} onChange={handleEmailChange} />
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