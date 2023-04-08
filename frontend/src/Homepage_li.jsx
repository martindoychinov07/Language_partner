import React from "react";
import "./App.css";
import { Link } from "react-router-dom";

export default function Hompage_li(){
    return(
 <div className="w-screen">
  {/* */}
  <div className="navbar sticky top-0 bg-purple-50 text-black font-adelia">
    <div className="flex-1">
        <a className="btn btn-ghost normal-case text-xl font-adelia">Ivo</a>
    </div>
    <div className="flex-none">
        <ul className="menu menu-horizontal px-1">
        <li><a>Find Friends</a></li>
        <Link to = "/chat"><li><a>Chats</a></li></Link>
        </ul>
    </div>
  </div>
  <div>
    <div className="flex-1">
        <ul className="mt-5 ml-5 px-1 flex-initial">
            <li><a className="text-[25px] font-adelia">What's hot:</a></li>
        </ul>
    </div>
  </div>
</div>
    )
}