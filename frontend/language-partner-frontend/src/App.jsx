import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Hompage from './Homepage'
import Signup from './Signup'
import Login from './Login'
function App() {
  return (
    <>
    <Login />
    <Signup />
    <Hompage />
    </>
  )
}

export default App
