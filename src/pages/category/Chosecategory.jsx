import React, { useState } from "react";
import { IoIosRemoveCircleOutline } from "react-icons/io";
import { IoAddCircleOutline } from "react-icons/io5";


export default function ChooseCategory() {

  const [selectedCategories, setSelectedCategories] = useState([]);
  

  const [availableCategories, setAvailableCategories] = useState([
    'Electronics',
    'Clothing',
    'Furniture',
    'Books',
    'Toys & Games',
    'Sports & Outdoors',
    'Beauty & Personal Care',
    'Health & Wellness',
    'Automotive',
    'Groceries',
    'Jewelry & Watches',
    'Home Appliances',
    'Gardening & Outdoor',
    'Pet Supplies',
    'Office Supplies',
    'Musical Instruments',
    'Baby Products',
    'Video Games',
    'Tools & Home Improvement',
    'Luggage & Bags',
  ]);

  const handleSelectCategory = (category) => {
    if (!selectedCategories.includes(category)) {
      setSelectedCategories((prevSelectedCategories) => [
        ...prevSelectedCategories,
        category
      ]);
      setAvailableCategories((prevAvailableCategories) =>
        prevAvailableCategories.filter((item) => item !== category)
      );
    }
  };

  const handleRemoveCategory = (category) => {
    setSelectedCategories((prevSelectedCategories) =>
      prevSelectedCategories.filter((item) => item !== category)
    );
    setAvailableCategories((prevAvailableCategories) => [
      ...prevAvailableCategories,
      category
    ]);
  };

  return (
    <>
        <div className="bg-gradient-to-r from-[#081D30] to-[#3f7db8]">
            <div className="container min-h-screen">
                {/* Header Section */}
                <div className="text-center py-12">
                <h4 className="text-3xl font-bold text-white">Opula ARS</h4>
                <span className="text-red-600">Thanks for joining us, Kindly verify your email</span>
                <h6 className="text-2xl font-bold text-white">How Many Categories do you want to work with?</h6>
                </div>

                {/* Search Bar */}
                <div className="flex items-center justify-center mb-8">
                <div className="flex">
                    <input
                    type="text"
                    id="Search categories"
                    name="Search categories"
                    className="w-full bg-transparent px-10 py-2 border border-[#45829b] rounded-full focus:outline-none focus:ring-2 focus:ring-[#0489BF]"
                    placeholder="Search categories"
                    required
                    />
                </div>
                <div className="flex mx-5">
                    <button className="rounded-full bg-[#6fc3dd] px-4 py-3 text-black w-32">Search</button>
                </div>
                </div>

                {/* Category Box */}
                <div className="flex flex-col items-center justify-center py-2 mx-auto max-w-7xl">
                {/* Selected Categories Box */}
                <div className="flex flex-col w-full mb-6">
                    <div className="flex justify-between items-center w-full mb-4">
                    <h4 className="text-lg font-semibold text-[#ffffff] mx-auto">
                        Selected Categories ({selectedCategories.length})
                    </h4>
                    <button
                        type="submit"
                        className="bg-[#b6551e] text-white py-2 px-6 rounded-md hover:bg-[#915c3e] focus:outline-none focus:ring-2 focus:ring-[#92674e]"
                    >
                        Submit
                    </button>
                    </div>
                    <div className="w-full bg-gradient-to-r from-[#c3dcdd] via-[#4991ac] to-[#65c2e7]  p-4 rounded-md">
                    {/* Display selected categories inside a box */}
                    <div className="flex flex-wrap gap-4 justify-center">
                        {selectedCategories.map((category) => (
                        <button
                            key={category}
                            className="bg-[#573725] text-white px-6 py-2 rounded-full hover:bg-[#e93d3d] transition duration-300"
                            onClick={() => handleRemoveCategory(category)}
                        >
                            <div className="flex">
                                <div className="flex">
                                    {category}
                                </div>
                                <span className="text-[#f08a8a] flex pt-1 ml-2 font-bold">
                                    <IoIosRemoveCircleOutline />
                                 </span>
                            </div>
                            
                        </button>
                        ))}
                    </div>
                    </div>
                </div>

                {/* Available Categories Buttons */}
                <h4 className="text-lg font-semibold text-[#ffffff] mb-2">Choose Categories for work</h4>
                <div className="flex flex-wrap gap-4 w-full justify-center mt-6">
                    {availableCategories.map((category) => (
                    <button
                        key={category}
                        className="bg-[#82C0D9] text-black px-6 py-2 rounded-full mx-2 my-2 hover:bg-[#beeec4] transition duration-300"
                        onClick={() => handleSelectCategory(category)}
                    >
                        <div className="flex">
                            <div className="flex">
                                {category} 
                            </div>
                            <span className="text-[#0f5a3b] flex pt-1 ml-2 font-bold"><IoAddCircleOutline /></span>
                        </div>
                    </button>
                    ))}
                </div>
                </div>
            </div>
        </div>

    </>
  );
}
