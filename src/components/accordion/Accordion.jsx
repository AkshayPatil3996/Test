import React, { useState } from "react";

export default function Accordion({ data }) {
  const [activeIndex, setActiveIndex] = useState(data[0]?.id);

  

  // isPath = (data) => {
  //   return { [data?.path]: '' }; 
  // };
  

  const toggleAccordion = (index) => {
    if (activeIndex !== index) {
      setActiveIndex(index);
    }
  };

  return (
    <div id="accordion-open">
      {data.map(({ id, path, title, content }) => (
        <div key={id} className="my-14">
          {/* Accordion Item */}
          <h2 id={`accordion-open-heading-${id}`}>
            <button
              type="button"
              className="flex transition-all rounded-full items-center py-3 justify-between w-full px-5 py-2 font-medium rtl:text-right bg-[#8C6046] text-black border border-b-0 border-gray-200  focus:ring-4 focus:ring-gray-200 dark:focus:ring-bg-[#6D310E] dark:border-bg-[#6D310E] dark:text-white hover:bg-[#996141] dark:hover:bg-bg-[#6D310E] gap-3 text-white"
              onClick={() => toggleAccordion(id)}
              aria-expanded={activeIndex === id ? "true" : "false"}
              aria-controls={`accordion-open-body-${id}`}
            >
              <span className="flex items-center gap-3">
                {/* Circle with image */}
                <div className={path ? ` bg-white rounded-full overflow-hidden flex items-center justify-center` : `hidden`}>
                  <img
                    src={path}
                    alt={title}
                    className="object-cover w-12 h-12 p-3"
                  />
                </div>


                {/* Accordion Title */}
                <div className="flex  md:w-48 text-sm">{title}</div>
              </span>
              <svg
                className={`w-3 h-3 shrink-0 transform ${
                  activeIndex === id ? "rotate-180" : ""
                }`}
                aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 10 6"
              >
                <path
                  stroke="currentColor"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M9 5 5 1 1 5"
                />
              </svg>
            </button>
          </h2>
          <div
            id={`accordion-open-body-${id}`}
            className={activeIndex === id ? "" : "hidden"}
            aria-labelledby={`accordion-open-heading-${id}`}
          >
            <div className="p-5 rounded-md  dark:border-gray-700 dark:bg-[#bddce9] transition-all">
              <p className="mb-2   md:text-base text-[#333333] leading-relaxed">{content}</p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
