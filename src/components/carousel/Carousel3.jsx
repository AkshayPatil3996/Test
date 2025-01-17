import { useState } from "react";
import { Carousel } from "react-responsive-carousel";
import "react-responsive-carousel/lib/styles/carousel.min.css"; // Carousel styling

export default function Carousel3({ data }) {
  const [currentIndex, setCurrentIndex] = useState(0);

  const handlePrev = () => {
    setCurrentIndex((prevIndex) => (prevIndex === 0 ? data.length - 1 : prevIndex - 1));
  };

  const handleNext = () => {
    setCurrentIndex((prevIndex) => (prevIndex === data.length - 1 ? 0 : prevIndex + 1));
  };

  return (
    <div className="flex justify-center items-center mb-40 my-4 py-5">
      {/* Static content */}
      <div className="relative bg-[#004d80] text-white p-8 rounded-lg shadow-lg  lg:w-96 md:w-96 w-80  mx-4 text-center">
        {/* Carousel3 component */}
        <Carousel
          selectedItem={currentIndex}
          onChange={(index) => setCurrentIndex(index)}
          showThumbs={false}
          showStatus={false}
          infiniteLoop
          autoPlay
          interval={5000}
          className="rounded-xl"
        >
          {data.map((item) => (
            <div key={item.id}>
              <div className="flex justify-center mb-4">
                <div className="w-10 h-10 flex justify-center items-center">
                  <img src={item.icon} alt="Icon" className="w-10 h-10" />
                </div>
              </div>

              {/* Static Title */}
              <h2 className="text-2xl font-semibold mb-4">{item.title}</h2>

              {/* Static Content */}
              <p className="text-sm leading-relaxed mb-6">
                {item.content}
              </p>
            </div>
          ))}
        </Carousel>

        {/* Navigation buttons */}
        <div
          className="absolute top-1/2 -translate-y-1/2 left-4 cursor-pointer"
          onClick={handlePrev}
        >
          <span className="text-white text-xl">&#8249;</span>
        </div>
        <div
          className="absolute top-1/2 -translate-y-1/2 right-4 cursor-pointer"
          onClick={handleNext}
        >
          <span className="text-white text-xl">&#8250;</span>
        </div>

        {/* Indicator dots */}
        {/* <div className="flex justify-center mt-4 space-x-2">
          {data.map((_, index) => (
            <span
              key={index}
              className={`w-2 h-2 rounded-full ${index === currentIndex ? "bg-white" : "bg-gray-400"}`}
            ></span>
          ))}
        </div> */}
      </div>
    </div>
  );
}
