import React, { useState } from 'react';
import "./App.css";

export default function Chat() {
  const [messages, setMessages] = useState([]);

  const [newMessage, setNewMessage] = useState('');

  const handleInputChange = (event) => {
    setNewMessage(event.target.value);
  };
  
  const handleSendClick = () => {
    const newId = messages.length + 1;
    const newMessages = [...messages, { id: newId, text: newMessage }];
    setMessages(newMessages);
    setNewMessage('');
  };

  return (
    // Navbar
    <div className='w-screen h-screen'>
      <div className='flex-initial navbar bg-purple-50 text-black font-adelia justify-between'>
      <ul className="menu menu-horizontal px-1">
        <li>
          <button>
            <img src='https://upload.wikimedia.org/wikipedia/commons/3/34/Home-icon.svg' className='w-10 h-10'></img>
          </button>
        </li>
      </ul>
        <ul className="menu menu-horizontal px-1">
          <li><a>Sign up</a></li> 
          <li><a>Log in</a></li>
      </ul>
      </div>
      {/* end of navbar */}
      {/* list of chats */}
      <div className=' bg-purple-50 text-black font-adelia w-60 h-[87vh] mb-[0px] mr-[0px]'>
        <h1 className='ml-5'>Chats:</h1>
        <h1 className='ml-5 mt-1'>Paco</h1>
      </div>
      {/* end of list of chats */}
      {/* send messages */}
      <ul className='absolute top-[100px] left-[900px]'>
        {messages.map((message) => (
          <li key={message.id} className='chat-bubble w-[200px] mb-1'>{message.text}</li>
        ))}
      </ul> 
      <input type="text" value={newMessage} onChange={handleInputChange} className="bg-gray-50 border absolute bottom-5 left-[493px] border-gray-300 text-gray-900 text-sm rounded-lg w-60 focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="Enter a message" required />
      <ul className="menu menu-horizontal px-1 absolute bottom-3 left-[750px]">
      <li>
      <button onClick={handleSendClick} className=''>
        <img src='https://icon-library.com/images/send-icon/send-icon-0.jpg' className='w-10 h-10' />
      </button>
      </li>
      </ul>
      {/* end of send messages */}
      {/* <ul className='absolute top-[100px] left-[900px]'>
        {messages.map((message) => (
          <li className='chat-bubble w-[100px] mb-1'>{data.message_recieved}</li>
        ))}
      </ul>  */}
    </div>
  );
}
