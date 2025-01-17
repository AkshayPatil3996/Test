import React from "react";

// Data for the footer sections
const footerLinks = {

  products: [
    { name: "Services", url: "#" },
    { name: "Pricing", url: "/pricing" },
    { name: "Testimonials", url: "#" },
    { name: "Blog", url: "/blog" },
  ],
  support: [
    { name: "Terms of Service", url: "/terms" },
    { name: "Privacy Policy", url: "/privacy/policy" },
    { name: "Cookie Policy", url: "#" },
    { name: "Contact Us", url: "/contact" },
  ],
  
};

export default function Footer() {
  return (
    <>
      <footer className="bg-[#051114] text-white py-6 backdrop-blur-md">
        <div className="max-w-[1200px] mx-auto grid grid-cols-1 md:grid-cols-4 gap-8 px-6">
          <div>
            <h1 className="font-semibold text-lg">OpulaArs</h1>
            <div>
                {/* <h5>Contact us</h5> */}
                <p className="text-sm mb-4">
                Embrace the power of personalisation with OpulaARS. Improve your AOV from the first day.
For more information or to schedule a demo, contact us. We look forward to helping you create a more personalized and engaging experience for your customers.

                </p>
            </div>
          </div>

          <div>
            <h3 className="font-semibold text-lg">Resources</h3>
            <ul>
              {footerLinks.products.map((link, index) => (
                <li key={index}>
                  <a href={link.url} className="hover:underline">
                    {link.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-lg">Useful Links</h3>
            <ul>
              {footerLinks.support.map((link, index) => (
                <li key={index}>
                  <a href={link.url} className="hover:underline">
                    {link.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-lg text-center">Newsletter</h3>
            <div className="mt-8 px-6 text-center">
               
                <p className="text-sm mb-4 text-start">Sign Up and receive the latest news via email</p>
               <div className="flex justify-center flex-col ">
                    <input
                    type="email"
                    placeholder="Enter your email"
                    className="px-4 py-2  rounded text-black"
                    />
                    <button className="bg-[#023d50] text-white px-6 py-2 rounded hover:bg-[#021f28] transition duration-300 my-2 m-0">
                    Send
                    </button>
                </div>
            </div>
          </div>
        </div>

        <div className="border-t border-gray-600 mt-6 pt-4 text-center text-sm">
          <p>&copy; 2024 The OpulaArs. All Rights Reserved.</p>
        </div>
      </footer>
    </>
  );
}
