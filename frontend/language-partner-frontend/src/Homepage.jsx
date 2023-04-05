import React from "react";
import "./App.css";
import { Link } from "react-router-dom"

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
    <p className="text-center font-adelia text-6xl text-black ">Why learn a language with Language Partner</p>
    <div className="flex p-3">
    <img src = "https://www.busuu.com/user/pages/home/_02-how-it-works-revamp/homepage-learn-together-dt-2x.png" className="w-[40vw]"/>
    <div className="text-center font-adelia w-screen ">
      <div className="pt-8">
      <p className="text-[#6c7483] m-3">AN INTERACTIVE COMMUNITY</p>
      <p className="text-[#252b2f] m-3">Learn more together</p>
      <p className="text-[#262c30] m-3">Go beyond the textbook. Practise pronunciation, gain cultural insights and exchange local language tips with our global community of learners. </p>
      </div>
      </div>  
    </div>
    <div className="flex p-3">
      {/* */}
    
    <div className="text-center font-adelia w-screen ">
      <div className="pt-8">
      <p className="text-[#6c7483] m-3">LESSONS FEATURING REAL PEOPLE</p>
      <p className="text-[#252b2f] m-3">Learn for real life</p>
      <p className="text-[#262c30] m-3">Say goodbye to outdated phrases and hello to skills that take you places. Learn language for every day with regularly updated content, video flashcards with real people and helpful cultural insights. </p>
      </div>
      </div> 
   <img src = "https://www.busuu.com/user/pages/home/_02-how-it-works-revamp/homepage-learn-real-life-dt-2x.png" className="w-[40vw]"/>
    </div>
  </div>
</div>
    )
}