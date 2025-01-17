import React from 'react';
import { MdOutlineEmail } from "react-icons/md";
import { IoIosCall } from "react-icons/io";
import { FaLocationDot } from "react-icons/fa6";
import { FaTelegramPlane } from "react-icons/fa";
import Carousel1 from '../../components/carousel/Carousel1';



export default function Conatct () {
  const images = [
    {
      id:1,
      src:"images/carousel/crsl4.webp",
    },
    {
      id:2,
      src:"images/carousel/crsl5.webp",
    },
    {
      id:3,
      src:"images/carousel/crsl6.webp",
    },

  ];
 
  const contact = [{
    email: 'SaulDesign@gmail.com',
    number: "+91 123456789",
    address: "123 Street 456 House"


  }];


  return (
    <>
    {/* <Carousel1 data={images}/> */}

    

    <div className='container-fluid bg-[#ecf6fa]  py-20 h-100'>
      <div className='pt-10'>
        <h3 className='text-center text-4xl text-[#21343d] font-bold'>Contact Us</h3>
        <p className='text-center my-2 text-lg'>Feel free to connect with us</p>
      </div>

      <div className="m-6 p-4 max-w-6xl mx-auto border-2   bg-[#fff] rounded-lg shadow-2xl">
        <div className="grid grid-cols-1 sm:grid-cols-6 md:grid-cols-12 gap-8 border-[#193541] " >
        
            <div className="bg-gradient-to-r from-[#3b92b4] via-[#024059] to-[#0489BF] rounded-lg p-6 col-span-4 md:col-span-4" style={{
              backgroundImage: 'url(images/bgimage/bg5.png)',
              backgroundSize: 'cover', 
              backgroundPosition: 'center', 
              backgroundRepeat: 'no-repeat', 
              backgroundColor: '#155E75',
              width: '100%', 
              
            }} >
            <h4 className="text-white text-xl font-semibold">Coordinates for <span className='text-[#b2e1f3]'>Correspondence</span></h4>

            <div className="mt-4 text-white" >
              <p className="mb-16 mt-28 flex items-center"><strong className='mx-3 pt-1'><MdOutlineEmail /></strong> {contact[0].email}</p>
              <p className="mb-16 flex items-center"><strong className='mx-3 pt-1'><IoIosCall /></strong> {contact[0].number}</p>
              <p className="mb-40 flex items-center"><strong className='mx-3 pt-1'><FaLocationDot /></strong> {contact[0].address}</p>
            </div>
          </div>

          {/* Right Side*/}
          <div className="flex flex-col justify-center p-6 col-span-8 md:col-span-8">
            <h2 className="text-xl text-center font-semibold text-[#333] mb-4">Get in Touch</h2>

            <form>
              {/* First Name */}
              <div className="mb-4">
                <label htmlFor="firstname" className="block text-sm font-medium text-[#21343d]">First Name</label>
                <input
                  type="text"
                  id="firstname"
                  name="firstname"
                  className="w-full bg-transparent px-4 py-2 border border-[#0489BF] rounded-md focus:outline-none focus:ring-2 focus:ring-[#0489BF]"
                  placeholder="Enter your first name"
                  required
                />
              </div>

              {/* Last Name */}
              <div className="mb-4">
                <label htmlFor="lastname" className="block text-sm font-medium text-[#21343d]">Last Name</label>
                <input
                  type="text"
                  id="lastname"
                  name="lastname"
                  className="w-full bg-transparent px-4 py-2 border border-[#0489BF] rounded-md focus:outline-none focus:ring-2 focus:ring-[#0489BF]"
                  placeholder="Enter your last name"
                  required
                />
              </div>

              {/* Email */}
              <div className="mb-4">
                <label htmlFor="email" className="block text-sm font-medium text-[#21343d]">Email</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  className="w-full bg-transparent px-4 py-2 border border-[#0489BF] rounded-md focus:outline-none focus:ring-2 focus:ring-[#0489BF]"
                  placeholder="Enter your email"
                  required
                />
              </div>

              {/* Phone Number */}
              <div className="mb-4">
                <label htmlFor="phone" className="block text-sm font-medium text-[#21343d]">Phone Number</label>
                <input
                  type="tel"
                  id="phone"
                  name="phone"
                  className="w-full bg-transparent px-4 py-2 border border-[#0489BF] rounded-md focus:outline-none focus:ring-2 focus:ring-[#0489BF]"
                  placeholder="Enter your phone number"
                  required
                />
              </div>

              {/* Radio Button */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-[#21343d]">Select Subject</label>
                <div className="flex items-center space-x-4">
                  <div className="flex items-center">
                    <input
                      type="radio"
                      id="emailContact"
                      name="contactMethod"
                      value="email"
                      className="h-4 w-4 bg-transparent text-[#0489BF] border-[#0489BF]"
                      required
                    />
                    <label htmlFor="emailContact" className="ml-2 text-sm">General Query</label>
                  </div>
                  <div className="flex items-center">
                    <input
                      type="radio"
                      id="phoneContact"
                      name="contactMethod"
                      value="phone"
                      className="h-4 w-4 bg-transparent text-[#0489BF] border-[#0489BF]"
                    />
                    <label htmlFor="phoneContact" className="ml-2 text-sm">Job Query</label>
                  </div>
                  <div className="flex items-center">
                    <input
                      type="radio"
                      id="phoneContact"
                      name="contactMethod"
                      value="phone"
                      className="h-4 w-4 bg-transparent text-[#0489BF] border-[#0489BF]"
                    />
                    <label htmlFor="phoneContact" className="ml-2 text-sm">Partner Query</label>
                  </div>
                </div>
              </div>

              {/* Message Textarea */}
              <div className="mb-4">
                <label htmlFor="message" className="block text-sm font-medium text-[#21343d]">Message</label>
                <textarea
                  id="message"
                  name="message"
                  rows="5"
                  className="w-full bg-transparent px-4 py-2 border border-[#0489BF] rounded-md focus:outline-none focus:ring-2 focus:ring-[#0489BF]"
                  placeholder="Enter your message"
                  required
                ></textarea>
              </div>

              {/* Submit Button */}
              <div className='flex'>
                  <button
                    type="submit"
                    className="w-full py-2 bg-[#6D310E] text-white rounded-md hover:bg-[#965834] focus:outline-none focus:ring-2 focus:ring-[#036a91]"
                  >

                   

                    <span className='flex pt-1 mx-2 items-center justify-center'><FaTelegramPlane /><p className='ml-2'>Send Message</p></span>
                  </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>


    </>
    

  );
};

