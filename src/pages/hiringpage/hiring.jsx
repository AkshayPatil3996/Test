import React from 'react';
import Carousel1 from '../../components/carousel/Carousel1';
import { VscDebugStart } from "react-icons/vsc";
import { GiBanknote } from "react-icons/gi";
import { TfiBag } from "react-icons/tfi";
import { MdOutlineWatchLater } from "react-icons/md";

export default function HiringPage() {

  const images = [
    { id: 1, src: "images/carousel/crsl7.webp" },
    { id: 2, src: "images/carousel/crsl5.webp" },
    { id: 3, src: "images/carousel/crsl6.webp" },
    { id: 4, src: "images/carousel/crsl1.webp" },
  ];

  const jobRoles = [
    { id: 1, role: 'Engineering' },
    { id: 2, role: 'Marketing' },
    { id: 3, role: 'Sales' },
    { id: 4, role: 'HR' },
    { id: 5, role: 'Product' }
  ];

  const jobDetails = {
    title: "Software Engineer",
    hiringStatus: "Hiring",
    posted: "Posted on: 1st Jan 2024",
    startDate: "1st Feb 2024",
    ctc: "10 LPA",
    experience: "2-5 years",
    lastDate: "15th Jan 2024",
    description: "We are looking for a highly skilled 'Associate Full Stack Developer' to join our dynamic team at Rentickle. If you have a passion for coding and are proficient in Node.js, CI/CD, JavaScript, ReactJS, HTML, CSS, MongoDB, Python, and AngularJS, then we want to hear from you!",
    responsibilities: [
      " Develop and maintain web applications using the latest technologies and best practices.",
      " Collaborate with the development team to design and implement new features.",
      " Optimize applications for maximum speed and scalability.",
      " Write clean, efficient, and well-documented code.",
      " Ensure the security and integrity of the applications.",
      " Participate in code reviews and provide constructive feedback to team members.",
      " Stay up to date with the latest trends and technologies in web development.",
      "If you are a problem-solver with a strong attention to detail and a desire to learn and grow, then we want you on our team. Apply now to be part of an exciting and innovative company that values creativity and excellence in everything we do."
    ],
    skills: ["JavaScript", "React", "Node.js", "MongoDB"]
  };

  return (
    <>
      {/* Carousel */}
      <Carousel1 data={images} />

      <div className='text-center mt-5 text-4xl font-bold text-[#093F68]'>
        <h4>Job Openings</h4>
      </div>

      <div className="flex flex-col lg:flex-row h-auto lg:h-screen mt-5 bg-gray-100 overflow-hidden">
        {/* Sidebar */}
        <div className="lg:w-1/4 bg-white shadow-md p-4 overflow-y-auto">
          <h2 className="text-lg font-bold p-4 border-b text-[#093F68] text-center">Job Openings</h2>
          <ul className="space-y-2 p-4">
            {jobRoles.map((category) => (
              <li key={category.id}>
                <button className="w-full p-3 bg-[#6D310E] cursor-pointer text-white rounded-md hover:bg-brown-700 hover:bg-[#a56a48] font-semibold text-center">
                  {category.role}
                </button>
              </li>
            ))}
          </ul>
        </div>

        {/* Job Details */}
        <div className="lg:w-3/4 bg-white p-6 overflow-y-auto">
          <div className='flex w-full items-center justify-between flex-wrap'>
            {/* Left section - Image */}
            <div className='flex m-2 min-w-36 max-w-36'>
              <img src="images/img7.webp" className='min-w-36 max-w-36' alt="hiring" />
            </div>

            {/* Middle Section - Posted Date */}
            <div className='flex-grow text-center m-2'>
              <p className="text-sm text-gray-500">{jobDetails.posted}</p>
            </div>

            {/* Right Section - Hiring Status */}
            <div className='flex justify-end m-2'>
              <p className="text-sm text-gray-500 pr-48">{jobDetails.hiringStatus}</p>
            </div>
          </div>

          <div className="flex justify-between mt-7 items-center flex-wrap">
            <div>
              <h1 className="text-2xl text-[#093F68] font-bold m-2">{jobDetails.title}</h1>
            </div>
            <button className="bg-[#093F68] text-white px-4 lg:px-6 mr-24 py-2 text-nowrap rounded-lg">
              Apply Now
            </button>
          </div>

          {/* Job Summary */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 my-4 text-sm text-gray-700">
            <div className="flex items-center">
              <VscDebugStart className="mr-2" /> <strong>Start Date:</strong>
              <span className="font-bold">{jobDetails.startDate}</span>
            </div>
            <div className="flex items-center">
              <GiBanknote className="mr-2" /> <strong>CTC (Annual):</strong>
              <span className="font-bold">{jobDetails.ctc}</span>
            </div>
            <div className="flex items-center">
              <TfiBag className="mr-2" /> <strong>Experience:</strong>
              <span className="font-bold">{jobDetails.experience}</span>
            </div>
            <div className="flex items-center">
              <MdOutlineWatchLater className="mr-2" /> <strong>Last Date:</strong>
              <span className="font-bold">{jobDetails.lastDate}</span>
            </div>
          </div>

          {/* About Job */}
          <h2 className="text-xl text-[#093F68] font-semibold my-2">About the Job</h2>
          <p className="text-gray-700">{jobDetails.description}</p>

          {/* Responsibilities */}
          <h2 className="text-xl font-semibold text-[#093F68] my-4">Key Responsibilities:</h2>
          <ul className="list-disc ml-6 text-gray-700 space-y-2">
            {jobDetails.responsibilities.map((res, index) => (
              <li key={index}>{res}</li>
            ))}
          </ul>

          {/* Skills */}
          <h2 className="text-xl text-[#093F68] font-semibold my-4">Skill(s) required</h2>
          <div className="flex flex-wrap space-x-2">
            {jobDetails.skills.map((skill, index) => (
              <span key={index} className="bg-gray-200 text-gray-700 px-3 py-1 rounded-md m-2">
                {skill}
              </span>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
