import { useState } from "react";
import { Link } from "react-router-dom";

export default function RegistrationPageTest() {
  const [formData, setFormData] = useState({
    firstname: "",
    lastname: "",
    email: "",
    password: "",
    confirmPassword: "",
    phoneNumber: "",
    domain: "",
    terms: false,
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();


    if (formData.password !== formData.confirmPassword) {
      alert("Passwords do not match");
      return;
    }

    console.log("Form Data Submitted:", formData);
  };

  return (
    <div className="w-full min-h-screen grid grid-cols-12 gap-0">
      {/* Image Section */}
      <div className="col-span-12 md:col-span-8 bg-[#437AA4]">
        <img
          src="images/signup.png"
          alt="Registration page background"
          className="w-fit h-fit object-cover"
        />
      </div>

      {/* Form Section */}
      <div className="col-span-12 md:col-span-4 bg-[#081D30] min-h-screen  p-6 flex items-center justify-center">
        <div className="w-full max-w-md">
          <Link to="/">
            <h2 className="text-white text-2xl font-bold mb-4 text-center">OPULA-ARS</h2>
          </Link>
          <h2 className="text-white text-2xl font-bold mb-4 text-center">Register</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* First Name */}
            <div className="mb-4">
              <label htmlFor="firstname" className="block text-white font-medium">
                First Name <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                id="firstname"
                name="firstname"
                value={formData.firstname}
                onChange={handleChange}
                className="w-full px-4 py-2 bg-transparent border-2 border-white text-white rounded-md focus:outline-none focus:border-blue-500"
                placeholder="Enter your First name"
                required
              />
            </div>

            {/* Last Name */}
            <div className="mb-4">
              <label htmlFor="lastname" className="block text-white font-medium">
                Last Name
              </label>
              <input
                type="text"
                id="lastname"
                name="lastname"
                value={formData.lastname}
                onChange={handleChange}
                className="w-full px-4 py-2 bg-transparent border-2 border-white text-white rounded-md focus:outline-none focus:border-blue-500"
                placeholder="Enter your Last name"
              />
            </div>

            {/* Email */}
            <div className="mb-4">
              <label htmlFor="email" className="block text-white font-medium">
                Email <span className="text-red-500">*</span>
              </label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="w-full px-4 py-2 bg-transparent border-2 border-white text-white rounded-md focus:outline-none focus:border-blue-500"
                placeholder="Enter your Email"
                required
              />
            </div>

            {/* Phone Number */}
            <div className="mb-4">
              <label htmlFor="phoneNumber" className="block text-white font-medium">
                Mobile Number <span className="text-red-500">*</span>
              </label>
              <div className="flex items-center">
                <div className="flex items-center px-3 py-2 border-2 border-white rounded-l-md bg-transparent">
                  <img
                    src="https://upload.wikimedia.org/wikipedia/commons/4/41/Flag_of_India.svg"
                    alt="India Flag"
                    className="h-5 w-7"
                  />
                  <span className="ml-2 text-white">+91</span>
                </div>
                <input
                  type="text"
                  id="phoneNumber"
                  name="phoneNumber"
                  value={formData.phoneNumber}
                  onChange={handleChange}
                  className="w-full px-4 py-2 bg-transparent border-2 border-white text-white rounded-r-md focus:outline-none focus:border-blue-500"
                  placeholder="Enter your Phone Number"
                  required
                />
              </div>
            </div>

            {/* Password */}
            <div className="mb-4">
              <label htmlFor="password" className="block text-white font-medium">
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

            {/* Confirm Password */}
            <div className="mb-4">
              <label htmlFor="confirmPassword" className="block text-white font-medium">
                Confirm Password<span className="text-red-500">*</span>
              </label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                className="w-full px-4 py-2 bg-transparent border-2 border-white text-white rounded-md focus:outline-none focus:border-blue-500"
                placeholder="Confirm your password"
                required
              />
            </div>

            {/* Domain */}
            <div className="mb-4">
              <label htmlFor="domain" className="block text-white font-medium">
                Domain <span className="text-red-500">*</span>
              </label>
              <div className="relative">
                <input
                  type="text"
                  id="domain"
                  name="domain"
                  value={formData.domain}
                  onChange={handleChange}
                  className="w-full px-4 py-2 bg-transparent border-2 border-white text-white rounded-md focus:outline-none focus:border-blue-500 pr-32"
                  placeholder="Enter your domain"
                  required
                />
                <span className="absolute right-0 top-1/2 transform bg-white text-dark font-bold p-3 rounded text-sm px-1 -translate-y-1/2">
                  .opulaars.com
                </span>
              </div>
            </div>

            {/* Terms and Conditions */}
            <div className="mb-4 flex items-center">
              <input
                type="checkbox"
                id="terms"
                name="terms"
                checked={formData.terms}
                onChange={handleChange}
                className="w-4 h-4 text-blue-500 border-gray-300 rounded focus:ring focus:ring-blue-500"
                required
              />
              <label htmlFor="terms" className="ml-2 text-white">
                I agree to the{" "}
                <a
                  href="/terms-of-service"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-500 underline"
                >
                  Terms of Service
                </a>{" "}
                and{" "}
                <a
                  href="/privacy-policy"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-500 underline"
                >
                  Privacy Policy
                </a>.
              </label>
            </div>

            {/* Submit Button */}
            <Link to='/category'>
              <button
                type="submit"
                className="w-full bg-[#6D310E] text-white py-2 mt-2 rounded-md hover:bg-[#724328] focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                Register
              </button>
            </Link>
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
              <span>Sign up with Google</span>
            </button>
              <Link to='/login'><p className="text-white">Already Have an Account ?
                <span className="text-blue-500 underline ml-3">Login</span>
                </p>
              </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
