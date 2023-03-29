import React from "react";
import "./App.css";
export default function Signup() {
    function handleSubmit(event) {
        event.preventDefault();
        const displayName = event.target[0].value;
    const email = event.target[1].value;
    const password = event.target[2].value;
    console.log(displayName,email, password);
    }
  return (
    <div className = "w-screen flex items-center justify-center h-screen bg-white">
        
        <div className = "w-[50vw] text-center">
        <p className="text-center text-black font-black text-2xl">ADD YOUR DETAILS HERE</p>
        <form onSubmit={handleSubmit}>
          <input type="text" placeholder="Name" className="input input-bordered input-info w-full max-w-xs bg-white my-3" />
          <input required type="email" placeholder="email" className="input input-bordered input-info w-full max-w-xs my-3 bg-white"/>
          <input required type="password" placeholder="password"  className="input input-bordered input-info w-full max-w-xs my-3 bg-white"/>
          <button className = "btn btn-outline btn-info m-auto">Sign up</button>
        </form>
        </div>
    </div>
  )
}