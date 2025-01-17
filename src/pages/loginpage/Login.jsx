import React, { useState } from "react";
import { Link } from "react-router-dom";

export default function LoginPage() {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Form Data Submitted:", formData);
  };

  return (
    <div className="w-full min-h-screen grid grid-cols-12 gap-0">

      <div className="col-span-12 md:col-span-8 p-5 bg-[#437AA4] relative">
        <img
          src="images/login.png" 
          alt="Registration page background"
          className="w-auto h-[550px] object-cover m-[100px]"
        />
      </div>


      <div className="col-span-12 md:col-span-4 bg-[#081D30] p-6 flex items-center justify-center">
        <div className="w-full max-w-md">
        <Link to='/'><h2 className="text-white text-2xl font-bold mb-4 text-center">OPULA - ARS</h2></Link>
          <h2 className="text-white text-2xl font-bold mb-4 text-center">Login</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
           
            <div>
              <label className="block text-white mb-2" htmlFor="email">
                Email <span className="text-red-500">*</span>
              </label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="w-full px-4 py-2 bg-transparent border-2 border-white text-white rounded-md focus:outline-none focus:border-blue-500"
                placeholder="Enter your email"
                required
              />
            </div>
            <div>
              <label className="block text-white mb-2" htmlFor="password">
                Password <span className="text-red-500">*</span>
              </label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className="w-full px-4 py-2 bg-transparent border-2 border-white text-white rounded-md focus:outline-none focus:border-blue-500"
                placeholder="Enter your password"
                required
              />
            </div>
            <button
              type="submit"
              className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              Login
            </button>
          </form>
            {/* Divider with 'or' */}
          <div className="flex flex-col items-center space-y-4 mt-6">
            <div className="flex items-center w-full">
              <div className="flex-grow border-t border-gray-300"></div>
              <span className="mx-4 text-gray-500">or</span>
              <div className="flex-grow border-t border-gray-300"></div>
            </div>

            {/* Google Sign-Up Button */}
            <button className="w-full text-white flex items-center justify-center space-x-2 bg-transparent  font-semibold py-2 px-4 rounded-full border border-gray-300 hover:bg-[#0489BF]">
              <img
                src="images/google.png"
                alt="Google Icon"
                className="w-5 h-5"
              />
              <span>Sign in with Google</span>
            </button>
              <Link to='/register'><p className="text-white">Don't have an account ?
                <span className="text-blue-500 underline ml-3">Create an Account</span>
                </p>
              </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
