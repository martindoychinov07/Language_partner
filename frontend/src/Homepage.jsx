import React from "react";
import "./App.css";
import { Link } from "react-router-dom";

export default function Hompage(){
    return(
 <div className="w-screen bg-blue-600">
  {/* */}
            <div className="navbar sticky top-0 bg-purple-50 text-black font-adelia">
  <div className="flex-1">
    <a className="btn btn-ghost normal-case text-xl font-adelia">Language Partner</a>
  </div>
  <div className="flex-none">
    <ul className="menu menu-horizontal px-1">
      <li><a>How it works</a></li>
      <Link to = "/signup"><li><a>Get started</a></li></Link>
      <Link to = "/login"><li><a>Log in</a></li></Link>;
    </ul>
  </div>
</div>
            {/*end of navbar */}
  <div className="w-screen flex">
    <div className="flex-1"><img src = "https://www.busuu.com/user/pages/home/_01-header/busuu-header-hello.png" className="w-[50vw]"/></div>
    <div className="flex-1 font-adelia">
        <h1 className="text-white text-5xl p-8">New language, new opportunities, new you</h1>
        <p className="text-white p-8">Get access to compact lessons from the experts and connect with a community of native speakers to help you master words faster</p>
        <Link to = "/signup"><button className="btn bg-[#11ee92] text-black hover:bg-green-300 px-8 mx-8">Get Started</button></Link>
    </div>
  </div>
{/*end of main */}
  <div className="bg-white">
    <p className="text-center font-adelia text-6xl text-black ">Practise the language of your choice with Language Partner</p>
    <div className="flex p-3">
    <div className="text-center font-adelia w-screen ">
      <div className="pt-8">
      <p className="text-[#262c30] m-3">Language Partner is a free app that allows you to practice oral communication in a foreign language with a native speaker partner of your choice. </p>
      </div>
      </div>  
    </div>
    <div className="flex p-3">
      {/* */}
    
    <div className="text-center font-adelia w-screen ">
      <div className="pt-8">
      <p className="text-[#262c30] m-3">If you have difficulty communicating in a foreign language, Language Partner is the place to practice and improve by practicing the language every day. With Language Partner, you can meet people from all over the world, communicate in any language you choose, build on and improve your knowledge and skills. With Language Partner, passive knowledge of the target language becomes active and you have the opportunity to practise vocabulary in your area of interest. Language Partner helps you build confidence and self-esteem, which are particularly important in oral communication. With Language Partner, you overcome the boundaries and anxieties you experience during your meetings with business partners and employees when they take place in a foreign language.</p>
      </div>
      </div> 
    </div>
  </div>
</div>
    )
}