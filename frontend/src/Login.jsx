import React from "react";
import "./App.css";
import { Link } from "react-router-dom";
import axios from "axios";
import { useNavigate } from 'react-router-dom';

export default function Login(){
    async function handleSubmit(event){
        event.preventDefault();
        const displayName = event.target[0].value;
        const email = event.target[1].value;
        const password = event.target[2].value
        navigate = useNavigate()
        try {
            const axios_response = await axios.post("http://localhost:5000/api/login",{
                name:displayName,
                email:email,
                password:password
            })
            console.log(axios_response)
            navigate('/about');
        }catch(err){
            console.log(axios_response)
        }
    }
    return(
        <div className = "w-screen flex items-center justify-center h-screen bg-white">
            <div className = "w-[50vw] text-center">
            <p className="text-center text-black font-black text-2xl">WELLCOME BACK</p>
                <form onSubmit={handleSubmit}>
                    <input required type="text" placeholder="name" className="input input-bordered input-info w-full max-w-xs my-3 bg-white"/>
                    <input required type="email" placeholder="email" className="input input-bordered input-info w-full max-w-xs my-3 bg-white"/>
                    <input required type="password" placeholder="password"  className="input input-bordered input-info w-full max-w-xs my-3 bg-white"/>
                    <button className = "btn btn-outline btn-info m-auto">Login</button>
                </form>
                <div className="flex-initial">
                <p className="text-center text-black font-black text-2xl">Don't have an account</p>
                <Link to = "/signup"><p className="text-center text-blue-600 font-black text-2xl">Sign up</p></Link>
                </div>
            </div>
        </div>
    )
}