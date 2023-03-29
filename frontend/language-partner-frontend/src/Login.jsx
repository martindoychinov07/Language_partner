import React from "react";
import "./App.css";

export default function Login(){
    function handleSubmit(event){
        event.preventDefault();
    }
    return(
        <div className = "w-screen flex items-center justify-center h-screen bg-white">
            <div className = "w-[50vw] text-center">
            <p className="text-center text-black font-black text-2xl">WELLCOME BACK</p>
                <form onSubmit={handleSubmit}>
                    <input required type="email" placeholder="email" className="input input-bordered input-info w-full max-w-xs my-3 bg-white"/>
                    <input required type="password" placeholder="password"  className="input input-bordered input-info w-full max-w-xs my-3 bg-white"/>
                    <button className = "btn btn-outline btn-info m-auto">Login</button>
                </form>
            </div>
        </div>
    )
}