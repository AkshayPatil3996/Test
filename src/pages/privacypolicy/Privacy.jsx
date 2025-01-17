import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Accordion from '../../components/accordion/Accordion';
import { Link } from 'react-router-dom';

export default function Privacyolicy() {

  const accordionData = [
    {
      id: 1,
      path: '',
      title: "What is Flowbite?",
      content:
        "Flowbite is an open-source library of interactive components built on top of Tailwind CSS including buttons, dropdowns, modals, navbars, and more.",
    },
    {
      id: 2,
      path: '',
      title: "Is there a Figma file available?",
      content:
        "Flowbite is first conceptualized and designed using the Figma software so everything you see in the library has a design equivalent in our Figma file.",
    },
    {
      id: 3,
      path: '',
      title: "Is there a Figma file available?",
      content:
        "Flowbite is first conceptualized and designed using the Figma software so everything you see in the library has a design equivalent in our Figma file.",
    },

  ];


  const [activeItem, setActiveItem] = useState('terms');

  const handleSidebarItemClick = (item) => {
    setActiveItem(item);
  };

  return (
    <>
      <div className="mt-20">
        <div className="bg-gradient-to-r from-[#024059] to-[#0489BF] md:px-8 md:py-24 p-3 relative overflow-hidden">
          <div className="flex flex-col md:flex-row items-center pl-6 xl:pl-96 md:justify-between gap-8">
            {/* Left side content */}
            <div className="text-white md:py-10 md:px-4 p-2 text-center md:text-left">
              <h3 className="text-4xl font-semibold">Opula</h3>
              <h5 className="text-3xl font-semibold mt-4">Privacy Policy</h5>
              <p className="text-xl text-center font-normal mt-4 italic">
                We value your privacy
              </p>
            </div>

            {/* Right side with image */}
            <div className="flex justify-center lg:pr-48 md:justify-end">
              <img
                src="../images/amico.webp"
                alt="terms and condition"
                className="w-48 h-48 md:w-80 md:h-80"
              />
            </div>
          </div>
          <div className='absolute' style={{ backgroundImage: 'url("../images/section-break.png")', backgroundRepeat: 'round', height: '100px', width: '100%', }}>
          </div>
        </div>

        {/* Main Content */}
        <div className="container mx-auto px-4 sm:px-12 md:px-28 py-8  my-5">

          <div className="flex flex-col lg:flex-row gap-8">
            {/* Sidebar */}
            <div className="flex flex-col space-y-4 items-center  sm:p-6 p-2 rounded-lg">
              <h4 className='text-left w-100 text-lg text-sky-400 font-bold'>Legal Information</h4>
              <Link to='/terms'>
                <button
                  className={`min-w-64 max-w-64 flex items-center shadow-lg text-cyan-950 font-normal text-lg cursor-pointer py-2 bg-[#D9D9D9] px-6 rounded-full transition-all duration-300 
                ${activeItem === 'terms' ? 'bg-[#D9D9D9]' : ''}`}
                  onClick={() => handleSidebarItemClick('terms')}
                  tabIndex="0"
                >
                  <img src="../images/valid-document.png" style={{ width: '20px', height: '20px', margin: '0 5px' }} />
                  <span className='text-base text-nowrap'>Tearm and condition Policy</span>
                </button>
              </Link>
              <Link to='/privacy/policy'><button
                className={`min-w-64 max-w-64  flex items-center shadow-lg text-cyan-950 font-normal text-lg cursor-pointer py-2 bg-[#D9D9D9] px-6 rounded-full transition-all duration-300 
                ${activeItem === 'privacy' ? 'bg-[#D9D9D9] text-white' : ''}`}
                onClick={() => handleSidebarItemClick('privacy')}
                tabIndex="0"
              >
                <img src="../images/valid-document.png" style={{ width: '20px', height: '20px', margin: '0 5px' }} />
                <span className='text-base text-nowrap'>Privacy Policy</span>
              </button>
              </Link>
            </div>

            {/* Content */}
            <div className="flex-1  sm:p-6 p-2 rounded-lg">
              <p className="text-[#000000] font-normal pb-5">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et
                dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip
                ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
                fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt
                mollit anim id est laborum.
              </p>
              <p className="text-[#000000] font-normal pb-5">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et
                dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip
                ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
                fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt
                mollit anim id est laborum.
              </p>
              <Accordion data={accordionData} />

              <p className="text-[#000000] font-normal pb-5">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et
                dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip
                ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
                fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt
                mollit anim id est laborum.
              </p>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

