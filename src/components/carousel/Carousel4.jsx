import { useState } from "react";
import { Carousel } from "react-responsive-carousel";
import "react-responsive-carousel/lib/styles/carousel.min.css"; // Carousel styling

export default function Carousel4({ data }) {
    const [currentIndex, setCurrentIndex] = useState(0);

    const handlePrev = () => {
        setCurrentIndex((prevIndex) => (prevIndex === 0 ? data.length - 1 : prevIndex - 1));
    };

    const handleNext = () => {
        setCurrentIndex((prevIndex) => (prevIndex === data.length - 1 ? 0 : prevIndex + 1));
    };



    const [ispopOpen, setIspopOpen] = useState(false);

    const toggleMenu = () => {
        setIspopOpen(!ispopOpen);
    };

    return (
        <div className={`fixed bottom-80 right-1 z-50  bg-sky-900 mb-4 2xl:w-64 2xl:min-h-96 2xl:rounded-lg  ${ispopOpen ? "w-64 min-h-96 rounded-lg " : " w-16 min-h-16 rounded-full flex items-center justify-center"}`} onClick={toggleMenu}>
            {/* Static content */}
            <img src="images/Quize_icon.png" className={`2xl:hidden  w-16 min-h-16 p-2 ${ispopOpen ? "hidden w-16 min-h-16 p-2" :"block"}`} />
            <div className={`w-64 text-white py-2 2xl:block  ${ispopOpen ? "block" : "hidden"}`}>
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
                                <div className="min-w-48 min-h-32  border rounded-lg mx-2">
                                    <img src={item.icon} alt="Icon" className="w-100 h-100" />
                                    {/* <div className="" style={{ backgroundImage: url(`${{ item.icon }}`)}}>
                                    </div> */}
                                </div>
                            </div>

                            {/* Static Title */}
                            <h2 className="text-2xl font-semibold mb-4">{item.title}</h2>

                            {/* Static Content */}
                            <p className="text-sm  mb-6 py-4">
                                {item.content}
                            </p>
                        </div>
                    ))}
                </Carousel>

                {/* Navigation buttons */}
                {/* <div
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
                </div> */}

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
