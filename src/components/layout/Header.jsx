// import { link } from "framer-motion/client";
import React, { useState, useEffect } from "react";
import { Link, NavLink } from 'react-router-dom';
import { IoMdClose, IoIosHome, IoMdPricetags } from "react-icons/io";
import { RiBloggerFill } from "react-icons/ri";
import { AiFillProduct } from "react-icons/ai";
import { FaBars } from "react-icons/fa6";

const navLinks = [
  { id: 1, icon: <IoIosHome /> ,    name: 'Home',    href: '/' },
  { id: 2, icon: <AiFillProduct />, name: 'Product', href: '/product' },
  { id: 3, icon: <IoMdPricetags />, name: 'Pricing', href: '/pricing' },
  { id: 4, icon: <RiBloggerFill />, name: 'Blog',    href: '/blog' }
];

const buttons = [
  { name: 'SignUp', href: '/register', style:'md:bg-[#024059] md:text-white bg-[#fff] px-8 py-2  md:px-6 py-2  my-4    rounded hover:bg-[#024059]' },
  { name: 'Login', href: '/login', style:'text-white bg-[#8C6046] px-8 py-2   md:px-6 md:py-2  my-4  rounded hover:bg-[#8C6046]' },
];

export default function Header() {
  const [scrolled, setScrolled] = useState(false);

  const [isNavVisible, setNavVisible] = useState(false);

  const toggleNav = () => {
    setNavVisible(!isNavVisible);
  };



  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 50) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };


    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);


 
  return (
    <>
      <button className="cst_close w-6 h-6 md:hidden absolute top-5 left-5  block text-center font-bold text-gray-800 text-3xl text-center cursor-pointer" onClick={toggleNav}>
        <FaBars />
      </button>

      <nav className={`transition-all duration-300  sidebar ${isNavVisible ? "hidden" : "flex"}  ${scrolled ? 'md:bg-gradient-to-r from-[#d9ebec] via-[#BED9E3] to-[#82C0D9] bg-[#024059]' : 'md:bg-gradient-to-r from-[#d9ebec] via-[#BED9E3] to-[#82C0D9] bg-[#024059]'} md:flex fixed top-0 md:left-0  z-50   md:h-20 md:w-full  h-screen w-64`}>
        <div className="container mx-auto py-5 px-6 sm:px-3 md:px-12 flex flex-col md:flex-row items-center justify-between">
          <div className="flex">
          <div className="text-2xl  font-bold md:text-gray-800 text-white md:text-center text-start px-4">
              <Link to='/'><img src="/images/logo_1.png" className="invert md:invert-0"/></Link>
          </div>

            <button className="cst_close w-6 h-6 md:hidden  block text-center font-bold text-white text-3xl text-center cursor-pointer" onClick={toggleNav}>
            <IoMdClose />
          </button>
        </div>

        <div className="flex lg:space-x-6 md:space-x-4  space-y-  flex-col md:flex-row  w-full justify-center">
          {navLinks.map((id) => (
            <NavLink
              key={id.name}
              to={id.href}
              className="md:text-gray-600 md:hover:text-gray-800 md:font-normal  text-white  font-semibold flex items-center mx-2  md:px-3 lg:px-6 md:py-2  py-5 "
              activeClassName="text-[#6D310E]"
              style={({ isActive }) => isActive ? { textDecoration: 'underline' } : undefined
              }
            >
              <span className="md:hidden flex text-lg">{id.icon}</span>
              <span className="mx-2 md:mx-0">{id.name}</span>
            </NavLink>
          ))}
        </div>


        <div className=" flex md:space-x-4  md:flex-row flex-col md:px-4   px-0  md:text-center text-start  md:w-56 w-full my-3">
          {buttons.map((button) => (
            <Link to={button.href} key={button.name}>
              <button className={button.style}>
                {button.name}
              </button>
            </Link>
          ))}
        </div>



        <div className="md:hidden">
          <button className="text-gray-800 focus:outline-none">

          </button>
        </div>
      </div>
    </nav>


    </>

  );
}
