import React from 'react';
import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import { useState } from 'react';
import './App.css';
import Homepage from './Homepage';
import Signup from './Signup';
import Login from './Login';
import Chat from './Chat';
import Hompage_li from './Homepage_li';
import PrivateRoute from './PrivateRoute';


export default function App(){
return (<Router>
      <Routes>
        <Route exact path="/login" Component={Login} />
        <Route path="/" Component={Homepage} />
        <Route path="/chat" Component={Chat} />
        <Route path="/signup" Component={Signup} />
        <Route path="/homepage_li" element={<PrivateRoute component={Hompage_li} />} />
      </Routes>
    </Router>)
}