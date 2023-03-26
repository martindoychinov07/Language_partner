import React from "react";
import "./App.css";
export default function Hompage(){
    return(
        <div className="w-screen bg-blue-600">
            <div className="navbar">
  <div className="flex-1">
    <a className="btn btn-ghost normal-case text-xl">Name </a>
  </div>
  <div className="flex-none">
    <ul className="menu menu-horizontal px-1">
      <li><a>How it works</a></li>
      <li><a>Get started</a></li>
      <li><a>Log in</a></li>
    </ul>
  </div>
</div>
            {/*end of navbar */}
<div className="w-screen flex">
    <div className="flex-1"><img src = "https://www.busuu.com/user/pages/home/_01-header/busuu-header-hello.png" className="w-[50vw]"/></div>
    <div className="flex-1">
        <h1 className="text-white fon">New language, new opportunities, new you</h1>
        <p>Get access to compact lessons from the experts and connect with a community of native speakers to help you master words faster</p>
        <button className="btn bg-[#11ee92] text-black hover:bg-green-300">Get Started</button>
    </div>
    {/*end of main */}

</div>
        </div>
    )
}