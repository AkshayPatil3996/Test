import React from "react";
import { FaHandshake } from "react-icons/fa";
import { MdRocketLaunch } from "react-icons/md";
import { RiShareForwardFill } from "react-icons/ri";
import { GiReceiveMoney } from "react-icons/gi";
import { BsGraphUpArrow } from "react-icons/bs";
import { Link } from "react-router-dom";
import Accordion from "../../components/accordion/Accordion";
import CarouselHeroScetion from "../../components/carousel/CarouselHeroSection"
import Carousel3 from "../../components/carousel/Carousel3"
import Carousel4 from "../../components/carousel/Carousel4"



export default function Home() {


    const impactData = [
        {
            icon: <MdRocketLaunch className="text-[#FF5370] text-3xl" />,
            bgColor: "bg-[#FFF3F4]",
            title: "Boosted User Retention",
            path: "images/salient/salient3.png",
            description:
                "Video-streaming platforms using machine learning algorithms to recommend videos, keep users on the platform longer and boost ad revenue. YouTube's recommendation engine reportedly drives over 70% of total viewing time.",
        },
        {
            icon: <BsGraphUpArrow className="text-[#9B6717] text-3xl" />,
            bgColor: "bg-[#FFF4E5]",
            title: "Increased Average Order Value (AOV)",
            path: "images/salient/salient3.png",
            description:
                "Retailers using recommendation engines have observed significant increases in cross-sell and up-sell conversions by recommending relevant and complementary products. According to McKinsey, personalized cross-selling can increase sales by up to 20%.",
        },
        {
            icon: <GiReceiveMoney className="text-[#FFC078] text-3xl" />,
            bgColor: "bg-[#FFF7ED]",
            title: "Higher Lifetime Customer Value",
            path: "images/salient/salient3.png",
            description:
                "With personalized offerings and tailored suggestions based on past activities and preferences, improved overall customer satisfaction and were driven to repeat usage.",
        },
    ];



    const canUse = [
        {
            title: 'Online Store Owners',
            description: `Personalization makes your store more attractive to existing customers
                        while also providing multiple opportunities to convert new customers. 
                        It also provides data to the business about customer activity and site usage. 
                        Using OpulaARS, business owners can get started quickly.`,
            icon: <RiShareForwardFill className="text-[#024059] text-2xl size-5" />,
        },
        {
            title: 'Website Builders',
            description: `Those who build e-commerce websites and stores can include personalization
                        as a value-added service that can contribute to their revenue stream. Website
                        builders and designers can integrate OpulaARS seamlessly into the store.`,
            icon: <RiShareForwardFill className="text-[#024059] text-2xl size-5" />,
        },
        {
            title: 'Marketers',
            description: `By creating personalized marketing campaigns and customer outreach, marketers
                        can ensure they are reaching out to the right people with the right information
                        to convert them into customers.`,
            icon: <RiShareForwardFill className="text-[#024059] text-2xl size-5" />,
        }
    ];

    const accordionData = [
        {
            id: 1,
            path: 'images/icon10.webp',
            title: "Data Collection",
            content:
                "Our system gathers extensive data from customer interactions, including browsing patterns, purchase history, and behavioral data. By analyzing this information, we establish a foundation of customer intent.",
        },
        {
            id: 2,
            path: 'images/icon11.webp',
            title: "Processing and Analysis",
            content:
                "Flowbite is first conceptualized and designed using the Figma software so everything you see in the library has a design equivalent in our Figma file.",
        },
        {
            id: 3,
            path: 'images/icon12.webp',
            title: "Personalisation and Recommendation Delivery",
            content:
                "Flowbite is first conceptualized and designed using the Figma software so everything you see in the library has a design equivalent in our Figma file.",
        },
        {
            id: 4,
            path: 'images/icon13.webp',
            title: "Continuous Improvement and Feedback Loop",
            content:
                "Opula’s recommendation engine is designed for continuous learning. It adapts with every new customer interaction to enhance recommendation precision and user satisfaction over time. The Rand D team at Opula is continuously working to improve the algorithms to minimize the errors.",
        },

    ];


    const salientFeatures = [
        {
            title: 'User-Friendly Interface',
            description: `Enjoy a clean and intuitive interface designed to make navigation a breeze.`,
            path: "images/salient/salient1.png",
        },
        {
            title: 'Intelligent Algorithms',
            description: `The team at OpulaARS is continuously innovating on the latest recommendation algorithms to bring the best solutions for you. Combining the product catalog with our intelligent algorithms, you can provide valuable cross-selling, up-selling, and customized product recommendations.`,
            path: "images/salient/salient2.png",
        },
        {
            title: 'Cross-Platform Support',
            description: `By creating personalized marketing campaigns and customer outreach, marketers can ensure they are reaching out to the right people with the right information to convert them to customers.`,
            path: "images/salient/salient3.png",
        },
        {
            title: 'Segment-specific Content and Promotions',
            description: `Create products and customer segments for targeted content and promotions.`,
            path: "images/salient/salient4.png",
        }
    ];

    const features = [
        {
            id: 1,
            path: 'images/icon1.png',
            title: 'Seamless Integration',
            description:
                'For brands built using COTS e-commerce apps, OpulaARS offers quick, plug-and-play integration that allows store owners to get started with minimal setup. This includes direct access to our recommendation engine via the app, allowing merchants to manage recommendation settings, track analytics, and view conversion impact—all from within the app interface.',
        },
        {
            id: 2,
            path: 'images/icon2.png',
            title: 'Customizable Widgets for Brand-Specific Needs',
            description:
                'OpulaARS provides customizable recommendation widgets that blend seamlessly with your website’s design and brand aesthetic. This feature helps smaller brands present a professional look that matches larger competitors, keeping customers engaged with their personalized selections.',
        },
        {
            id: 3,
            path: 'images/icon3.png',
            title: 'Targeted Cross-Selling and Up-selling Tools',
            description:
                'OpulaARS provides cross-sell and up-sell recommendations that increase the average order value, essential for maximizing revenue without increasing traffic acquisition costs.',
        },
        {
            id: 4,
            path: 'images/icon4.png',
            title: 'Easy-to-Use Dashboard for SMBs',
            description:
                'We understand that small business owners are often short on time. OpulaARS includes an intuitive dashboard that lets you set up, monitor, and adjust your recommendation settings with just a few clicks. Track which products are driving conversions, which recommendations work best, and gain insights for informed future marketing efforts.',
        },
    ];

    const keyFeatures = [
        {
            id: 1,
            path: 'images/icon8.png',
            title: 'Automatic Product Recommendations',
            content: 'From “Recommended for You” sections to “Similar Products” carousels, OpulaARS provides a variety of recommendation types that users can easily configure and display on their sites.'
        },
        {
            id: 2,
            path: 'images/icon5.png',
            title: 'Real-Time Analytics and Insights',
            content: 'Get immediate feedback on recommendation performance, with insights that help smaller brands make fast, data-driven decisions to enhance customer engagement and satisfaction.'
        },
        {
            id: 3,
            path: 'images/icon6.png',
            title: 'Intelligent re-ranking',
            content: 'Use/customize AI-ranking algorithms to optimize the product order in search results.'
        },
        {
            id: 4,
            path: 'images/icon7.png',
            title: 'Easy A/B Testing Capabilities',
            content: 'Use/customize AI-ranking algorithms to optimize the product order in search results.'
        }
    ];

    const chooseOpula = [
        {
            title: "E-commerce",
            description:
                "To suggest products based on browsing history, purchase behavior, and customer preferences.",
            image: "/path-to-your-images/ecommerce.jpg",
        },
        {
            title: "Music Streaming",
            description:
                "To recommend songs, artists, and playlists tailored to individual tastes.",
            image: "/path-to-your-images/music-streaming.jpg",
        },
        {
            title: "Video Streaming",
            description:
                "To suggest movies, TV shows, and videos based on viewing habits.",
            image: "/path-to-your-images/video-streaming.jpg",
        },
        {
            title: "News and Articles",
            description:
                "To personalize content delivery based on customer interests and reading patterns.",
            image: "/path-to-your-images/news.jpg",
        },
        {
            title: "Social Media",
            description:
                "To suggest movies, TV shows, and videos based on viewing habits.",
            image: "/path-to-your-images/social-media.jpg",
        },
        {
            title: "Education",
            description:
                "To recommend courses, tutorials, and learning resources based on customer goals and progress.",
            image: "/path-to-your-images/education.jpg",
        },
        {
            title: "Travel and Hospitality",
            description:
                "To suggest destinations, hotels, and activities based on past travel history and preferences.",
            image: "/path-to-your-images/travel.jpg",
        },
        {
            title: "Health and Fitness",
            description:
                "To suggest fitness plans based on preferences and activity history.",
            image: "/path-to-your-images/health.jpg",
        },
        {
            title: "Retail Banking and Finance",
            description:
                "To recommend financial products and services like loans, credit cards, and investment opportunities.",
            image: "/path-to-your-images/finance.jpg",
        },
    ];


    const images = [
        {
            id: 1,
            src: "images/Herobanner_1.webp",
        },
        {
            id: 2,
            src: "images/Herobanner_2.webp",
        },
        {
            id: 3,
            src: "images/Herobanner_3.webp",
        },

    ];

    const shopAsist = [
        {
          id: 1,
          icon: "images/icon9.png",
          title: "What's on offer",
          content: "An app that makes personalized recommendations, considering preferences and historical buying behavior..."
        },
        {
          id: 2,
          icon: "images/icon9.png",
          title: "What's on offer 2",
          content: "More detailed content for offer 2..."
        },
        {
          id: 3,
          icon: "images/icon9.png",
          title: "What's on offer 3",
          content: "Content for the third offer..."
        }
    ];
    

    const Quizepop = [
        {
            id: 1,
            icon: "images/img_craousal1.png",
            content: "Collaborative filtering model, based on assumption that people like things similar to other things they like, and things that are liked by other people with similar taste."
        },
        {
            id: 2,
            icon: "images/img_craousal2.svg",
            content: "In order to apply gradient descent, the function must be continuous, differentiable, and convex. The function’s gradient also needs to satisfy the requirements for Lipschitz continuity."
        },
        {
            id: 3,
            icon: "images/img_craousal3.avif",
            content: "The length of a vector is called the norm. The norm is a positive value that indicates the magnitude of the vector. The norm of a vector can be calculated using the above Euclidean formula."
        }
    ];



    


    return (
        <>

            <div className="" >
                <Carousel4 data={Quizepop} />
            </div>
            


            {/* Hero Section */}
            <section className="bg-gradient-to-r from-[#d9ebec] via-[#BED9E3] to-[#82C0D9] max-w-screen  py-12">
                <div className="mx-auto xl:pt-32  md:mt-5 mt-16   lg:px-12 md:px-6 sm:px-4 px-2  flex flex-col md:flex-row md:items-center md:justify-between">
                    <div className="md:w-1/2">
                        <h1 className="text-2xl lg:text-3xl font-bold text-slate-950 leading-tight mb-6 ">
                            Welcome to OpulaARS, the <br />
                            <span>Advanced Recommendation System</span> <br />
                            offered by Opula.
                        </h1>
                        <h6 className="my-4">Get Started with OpulaARS</h6>
                        <p className="text-gray-600 mb-6 pr-20">
                            Join the list of satisfied customers who have transformed their online presence
                            with our recommender system. Sign up today and start discovering the products,
                            and content your customers would love, curated just for them.
                        </p>
                        <div className="flex space-x-4">
                            <button className="bg-[#024059] text-white px-6 py-2 rounded">
                                Get Started
                            </button>
                            <Link to='/hiring'>
                                <button className="bg-[#8C6046] text-white px-6 py-2 rounded">
                                    We are hiring
                                </button>
                            </Link>
                        </div>
                    </div>

                    <div className="md:w-1/2 mt-8 md:mt-0">
                        {/* <img
                            src="images/img1.png"
                            alt="AI interacting with a person"
                            className="rounded-lg shadow-lg"
                        /> */}
                        <CarouselHeroScetion data={images} />

                    </div>

                </div>
            </section>


            <div className="container mx-auto py-5 mt-5 px-2 xl:px-12 items-center justify-between">

                {/* Harness The Power of Choice */}

                <div>
                    <h3 className="text-[#024059] font-semibold text-2xl  mx-6">
                        Harness the “Power of Choice”
                    </h3>

                    <p className="text-[#333333] lg:text-lg text-base leading-relaxed mt-6 mx-8">
                        At Opula, we empower your business by delivering the right choices to customers through a world-class recommendation platform. Presenting curated, relevant choices isn't just an enhancement—it’s a business imperative. The Opula ARS engine integrates seamlessly with your e-commerce ecosystem, enabling you to provide personalized experiences that delight customers and drive conversions. With OpulaARS, the power of choice translates to stronger engagement, higher retention, and increased revenue.
                        <br />
                        <br />
                        Our state-of-the-art recommendation engine brings you closer to the things your customers love, making their online experience truly personalized, be it music, news or consumables.
                    </p>
                </div>

                {/* The Impact of the Right Choices*/}

                <div className="py-10">
                    <h3 className="text-[#024059] font-semibold text-2xl mx-6">
                        The Impact of the Right Choices
                    </h3>

                    <p className="text-[#333333] text-lg sm:text-base leading-relaxed mt-6 mx-8">
                        The biggest names in digital—video-streaming, e-commerce, and social-media apps—have mastered the art
                        of making personalized recommendations, understanding that presenting relevant choices directly impacts
                        their growth. The effect is clear:
                    </p>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-0 mt-12 lg:mx-20 md:mx-2">
                        {impactData.map((impact, index) => (
                            <div
                                key={index}
                                className="bg-white shadow-2xl mx-3 my-4  rounded-lg text-center hover:shadow-xl transition duration-300 lg:w-64 md:w-52 w-11/12 min-h-64"
                            >
                                <div className="rounded-t-lg  relative">
                                    <div
                                        className={`lg:w-24 lg:h-24 md:w-20 md:h-20 sm:w-24 sm:h-24  w-16 h-16 flex items-center justify-center mx-auto rounded-full ${impact.bgColor} my-4`}
                                    >
                                        {impact.icon}
                                    </div>



                                    <div className="lg:p-6 md:p-4  p-10 bg-gradient-to-b text-white rounded-b-2xl" style={{ backgroundImage: 'url(images/bgimage/bg2.png)', minHeight: '333.55px', maxHeight: '333.55px', backgroundRepeat:'no-repeat', backgroundSize:'cover' }}>
                                        <h4 className="md:text-base lg:text-lg font-semibold px-3 py-2">{impact.title}</h4>
                                        <p className="text-sm leading-relaxed py-4 font-light">
                                            {impact.description}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>

                    <p className="text-[#333333] text-lg leading-relaxed mt-6 mx-8">
                        The impact of personalized recommendations extends well beyond entertainment and e-commerce. Across industries, brands that successfully integrate AI-powered recommendation systems, have  transformed customer engagement and experience.
                    </p>
                </div>

                {/* Who can use it */}
                <div className="relative py-5 bg-cover bg-center">

                    <div className="max-w-screen-xl mx-auto  md:px-2 lg:px-6  relative z-10">
                        <div className="grid grid-cols-1 md:grid-cols-12 ">

                            <div className="col-span-12 md:col-span-8">
                                <img src="images/grp_cloud.png" alt="OpulaARS Use Case" className="w-full rounded-lg" />
                            </div>

                            <div className="col-span-12 md:col-span-4 flex flex-col justify-center space-y-8">
                                <h4 className="lg:text-3xl text-4xl  font-semibold text-[#024059]">Who can use it?</h4>

                                {canUse.map((use, index) => (
                                    <div key={index} className="space-y-4">
                                        <div className="flex items-center space-x-4">
                                            {use.icon}
                                            <h6 className="lg:text-xl md:text-base font-medium">{use.title}</h6>
                                        </div>

                                        <p className="lg:text-base md:text-sm  text-[#051114] leading-relaxed font-normal">{use.description}</p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>

                {/* How It Works: Technology Behind OpulaARS */}
                <div className="relative py-20 bg-cover bg-center">
                    <div className="max-w-screen-xl mx-auto px-2 md:px-6 relative z-10">
                        <div className="">
                            <h4 className="lg:text-3xl text-4xl  font-semibold text-[#024059]">
                                How It Works: Technology Behind OpulaARS
                            </h4>
                            <p className="mt-5 text-[#333333] lg:text-lg md:text-base leading-relaxed">Opula Advanced Recommendation System is powered by advanced AI and machine learning technologies, ensuring that your customers always receive the most relevant recommendations. Here’s a look at the steps and the sophisticated algorithms that power our engine:
                            </p>
                        </div>
                        <div className="flex mt-7 flex-col md:flex-row">
                            <div className=" flex items-center justify-center mr-3  w-full">
                                <img src="images/img6.webp" alt="" className="w-4/6 h-4/12  md:w-full md:h-full " />
                            </div>
                            <div className="flex ml-3 w-full">
                                <Accordion data={accordionData} />
                            </div>
                        </div>
                    </div>
                </div>

                {/* Why Choose OpulaARS? */}
                {/* <div className="relative py-10 bg-cover bg-center">
                    <div className="max-w-screen-xl mx-auto px-6 md:px-12 relative z-10">
                        <div className="">
                            <h4 className="text-3xl font-semibold text-[#024059]">
                                Why Choose OpulaARS ?
                            </h4>
                            <p className="mt-5 text-[#333333] text-lg leading-relaxed">Adopt worthwhile personalisation to maximize growth in revenue and customer acquisition.
                                Our advanced algorithms analyze user preferences to provide recommendations that match customer's unique tastes.

                                <br /><br /><br />
                                Experience the magic of customized suggestions across the following domains.


                            </p>
                        </div>

                        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 py-7">
                            {chooseOpula.map((item, index) => (
                                <div
                                    key={index}
                                    className="relative group bg-gray-800 text-white rounded-md overflow-hidden shadow-md"
                                    style={{ aspectRatio: "1.4/1" }}
                                >
                                    <img
                                        src={item.image}
                                        alt={item.title}
                                        className="w-full h-full object-cover opacity-80"
                                    />
                                    <div className="absolute inset-0 bg-black bg-opacity-60 p-4 flex flex-col justify-center text-center group-hover:bg-opacity-80 transition-all">
                                        <h2 className="text-xl font-bold">{item.title}</h2>
                                        <p className="text-sm mt-2">{item.description}</p>
                                    </div>
                                </div>
                            ))}
                        </div>

                    </div>
                </div> */}

                <div className="py-2 container mx-auto px-1 2xl:px-32 ">
                    <div className="flex gap-4 sm:flex-row flex-col">
                        <div className="col  rounded-lg md:h-96 relative md:w-3/5 sm:w-1/3 w-full h-64 " style={{backgroundImage: 'url(images/why_1.png)', backgroundRepeat: 'no-repeat', backgroundSize:'cover' }}>
                            <div className="absolute  rounded-lg top-0 left-0 right-0 bottom-0" style={{ backgroundColor: '#024059', opacity: '60%' }}></div>
                            <div className="text-area  md:pt-10  lg:pt-32 px-4 text-center z-20 relative pb-10">
                                <h1 className="p-4 text-white font-semibold 2xl:text-4xl">E-commerce</h1>
                                <p className="text-white text-start">
                                    To suggest products based on browsing history, purchase behavior, and customer preferences.
                                </p>
                            </div>
                        </div>

                        <div className="col rounded-lg md:h-96 relative  border md:w-1/5 sm:w-1/3 w-full h-64" style={{ backgroundImage: 'url(images/why_2.png)', backgroundRepeat: 'no-repeat', backgroundSize: 'cover' }}>
                            <div className="absolute  rounded-lg top-0 left-0 right-0 bottom-0" style={{  backgroundColor: '#024059', opacity: '60%' }}></div>
                            <div className="text-area  md:pt-10  lg:pt-32 px-4 text-center z-20 relative pb-10">
                                <h1 className="px-0 py-2 text-white font-semibold 2xl:text-4xl text-left">Music Streaming</h1>
                                <p className="text-white text-start">
                                    To recommend songs, artists, and playlists tailored to individual tastes.
                                </p>
                            </div>
                        </div>

                        <div className="col rounded-lg md:h-96 relative  border md:w-1/5 sm:w-1/3 w-full h-64" style={{ backgroundImage: 'url(images/why_10.png)', backgroundRepeat: 'no-repeat', backgroundSize: 'cover' }}>
                            <div className="absolute  rounded-lg top-0 left-0 right-0 bottom-0" style={{  backgroundColor: '#024059', opacity: '60%' }}></div>
                            <div className="text-area  md:pt-10  lg:pt-32 px-4 text-center z-20 relative pb-10">
                                <h1 className="px-0 py-2 text-white font-semibold 2xl:text-4xl text-left">Video Streaming</h1>
                                <p className="text-white text-start">
                                    To suggest movies, TV shows, and videos based on viewing habits.
                                </p>
                            </div>
                        </div>

                    </div>
                </div>

                <div className="py-2 container mx-auto px-1 2xl:px-32">
                    <div className="flex gap-4">
                        <div className="col  rounded-lg sm:h-96 relative md:w-4/5" style={{ backgroundImage: 'url(images/why_3.png)', backgroundRepeat: 'no-repeat', backgroundSize: 'cover' }}>
                            <div className="absolute  rounded-lg top-0 left-0 right-0 bottom-0" style={{  backgroundColor: '#024059', opacity: '60%' }}></div>

                            <div className="text-area  px-0 z-20 relative md:pt-10 lg:pt-36">
                                <h1 className="p-2 text-white font-semibold 2xl:text-4xl text-start">News and Articles</h1>
                                <p className="text-white text-start sm:p-4 p-2">
                                    To personalize content delivery based on customer interests and reading patterns.
                                </p>
                            </div>
                        </div>


                        <div className="col rounded-lg pl-3 relative  border md:w-1/5" style={{ backgroundImage: 'url(images/why_4.png)', backgroundRepeat: 'no-repeat', backgroundSize: 'cover' }}>
                            <div className="absolute  rounded-lg top-0 left-0 right-0 bottom-0" style={{  backgroundColor: '#024059', opacity: '60%' }}></div>
                            <div className="text-area  md:pt-10  lg:pt-32 p-2 text-center z-20 relative pb-10">
                                <h1 className="px-0 py-2 text-white font-semibold 2xl:text-4xl text-left">Social Media  </h1>
                                <p className="text-white text-start">
                                    To suggest movies, TV shows, and videos based on viewing habits.
                                </p>
                            </div>
                        </div>

                    </div>
                </div>

                <div className="py-2 container mx-auto px-1 2xl:px-32">
                    <div className="flex gap-2 md:flex-row flex-col">

                        <div className="col rounded-lg relative  border md:w-1/4  min-h-12" style={{ backgroundImage: 'url(images/why_5.png)', backgroundRepeat: 'no-repeat', backgroundSize: 'cover' }}>
                            <div className="absolute  rounded-lg top-0 left-0 right-0 bottom-0" style={{  backgroundColor: '#024059', opacity: '60%' }}></div>
                            <div className="text-area  md:pt-10  lg:pt-32 px-4 text-center z-20 relative pb-10">
                                <h1 className="px-0 py-2 text-white font-semibold 2xl:text-4xl text-left">Education </h1>
                                <p className="text-white text-start">
                                    To recommend courses, tutorials, and learning resources based on customer goals and progress.
                                </p>
                            </div>
                        </div>
                        <div className="col rounded-lg relative  border md:w-1/4" style={{ backgroundImage: 'url(images/why_7.png)', backgroundRepeat: 'no-repeat', backgroundSize: 'cover' }}>
                            <div className="absolute  rounded-lg top-0 left-0 right-0 bottom-0" style={{  backgroundColor: '#024059', opacity: '60%' }}></div>
                            <div className="text-area  md:pt-10  lg:pt-32 px-4 text-center z-20 relative pb-10">
                                <h1 className="px-0 py-2 text-white font-semibold 2xl:text-4xl text-left">Travel and Hospitality</h1>
                                <p className="text-white text-start">
                                    To suggest destinations, hotels, and activities based on past travel history and preferences.
                                </p>
                            </div>
                        </div>
                        <div className="col rounded-lg relative  border md:w-1/4" style={{ backgroundImage: 'url(images/why_6.png)', backgroundRepeat: 'no-repeat', backgroundSize: 'cover' }}>
                            <div className="absolute  rounded-lg top-0 left-0 right-0 bottom-0" style={{  backgroundColor: '#024059', opacity: '60%' }}></div>
                            <div className="text-area  md:pt-10  lg:pt-32 px-4 text-center z-20 relative pb-10">
                                <h1 className="px-0 py-2 text-white font-semibold 2xl:text-4xl text-left">Health and Fitness  </h1>
                                <p className="text-white text-start">
                                    To suggest destinations, hotels, and activities based on past travel history and preferences.

                                </p>
                            </div>
                        </div>
                        <div className="col rounded-lg relative  border md:w-1/4" style={{ backgroundImage: 'url(images/why_8.png)', backgroundRepeat: 'no-repeat', backgroundSize: 'cover' }}>
                            <div className="absolute  rounded-lg top-0 left-0 right-0 bottom-0" style={{  backgroundColor: '#024059', opacity: '60%' }}></div>
                            <div className="text-area  md:pt-10  lg:pt-32 px-4 text-center z-20 relative pb-10">
                                <h1 className="px-0 py-2 text-white font-semibold 2xl:text-4xl text-left">Retail Banking and Finance</h1>
                                <p className="text-white text-start">
                                    To recommend financial products and services like loans, credit cards, and investment opportunities based on customer profiles..
                                </p>
                            </div>
                        </div>

                    </div>
                </div>

                <div className="py-2 container mx-auto px-1 2xl:px-32">
                    <div className="flex gap-4">
                        <div className="col rounded-lg relative  border sm:py-20 py-10  w-full" style={{ backgroundImage: 'url(images/why_9.png)', backgroundRepeat: 'no-repeat', backgroundSize: 'cover' }}>
                            <div className="absolute  rounded-lg top-0 left-0 right-0 bottom-0" style={{  backgroundColor: '#024059', opacity: '60%' }}></div>
                            <div className="text-area  md:pt-10  lg:pt-32 px-4 text-center z-20 relative pb-10">
                                <h1 className="px-0 py-2 text-white font-semibold 2xl:text-4xl text-left">Telecome </h1>
                                <p className="text-white text-start">
                                    To recommend appropriate tariff plans and value added services
                                </p>
                            </div>
                        </div>



                    </div>
                </div>


                {/* Salient Features */}

                <div className="relative  md:py-20 py-4 bg-cover bg-center">
                    <div className="max-w-screen-xl mx-auto px-2 md:px-6 relative z-10">
                        <div className="grid grid-cols-1 md:grid-cols-12 ">

                            <div className=" md:col-span-4 flex flex-col justify-center space-y-8 px-6 md:px-2">
                                <h4 className="text-3xl font-normal text-[#2477BF]">Salient Features...</h4>

                                {salientFeatures.map((sfeature, index) => (
                                    <div key={index} className="space-y-4">
                                        <div className="flex items-center space-x-4   flex-row">
                                            <img src={sfeature.path} alt={sfeature.title} className="w-12 h-12 rounded-full object-cover" />
                                            <h6 className="lg:text-xl font-medium text-[#024059] md:text-sm md:ml-0">{sfeature.title}</h6>
                                        </div>

                                        <p className="lg:text-base text-sm  text-[#051114] leading-relaxed">{sfeature.description}</p>
                                    </div>
                                ))}
                            </div>


                            <div className="col-span-12 md:col-span-8 px-6 ">
                                <img src="images/salient/salient.png" alt="OpulaARS Use Case" className="w-4/6 md:w-full rounded-lg" />
                            </div>

                        </div>
                    </div>
                </div>
            </div>

            {/* Empowering Small and Medium-Sized E-Commerce Brands with OpulaARS */}

            <div className="bg-[#8C6046] w-full p-8">
                <div className="text-center text-white text-3xl mb-6 pr-8">
                    <h3 className="lg:text-3xl md:text-2xl sm:text-xl text-base">
                        Empowering Small and Medium-Sized E-Commerce Brands with <span className="font-bold">OpulaARS</span>
                    </h3>
                </div>
                <div className="container mx-auto py-5 mt-5  px-0 sm:px-6  xl:px-12 items-center justify-between">
                    <div className="flex flex-col md:flex-row items-center md:items-start">
                        <div className="w-full md:w-1/2 flex justify-center  mb-6 md:mb-0">
                            <img
                                src="images/smallnmed.png"
                                alt="small and medium"
                                className="w-72 h-auto rounded-lg  transform rotate-12 object-cover"
                            />
                        </div>
                        <div className="w-full md:w-1/2 text-white text-lg leading-relaxed md:pl-8">
                            <p className="text-xs md:text-base">
                                For small and medium-sized e-commerce brands, a powerful recommendation engine can make a significant
                                difference in building customer loyalty, boosting sales, and maximizing limited resources. <span className="font-bold">OpulaARS</span> offers an ideal solution by bringing the power of advanced AI-based recommendations to small businesses, helping them compete with larger players by providing a highly personalized shopping experience for every customer.
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            {/*  Why OpulaARS is Perfect for Small and Medium E-Commerce Brands?  */}

            <div
                className="relative  lg:pt-30 lg:pb-60 bg-cover md:bg-top w-100 justify-items-start my-10"
                style={{ backgroundImage: 'url(images/bg2.png)', backgroundRepeat: 'no-repeat' }}
            >
                <div className="container mx-auto px-6  md:pt-36 lg:pt-56">
                    <div className="text-center mb-12 mt-10 pt-20">
                        <h2 className="lg:text-4xl md:text-3xl sm:text-2xl font-semibold text-gray-800  sm:w-96 text-left">
                            Why OpulaARS is Perfect for Small and Medium E-Commerce Brands?
                        </h2>
                        <p className="mt-4 sm:text-base text-xs text-gray-600 leading-relaxed text-left md:px-4 px-2">
                            Small and medium-sized brands often need to optimize every customer interaction for
                            conversions while staying within budget constraints. OpulaARS is designed to deliver
                            powerful recommendations without requiring a team of developers or complex integration.
                            OpulaARS provides:
                        </p>
                    </div>


                    <div className="grid gap-8 grid-cols-1 md:grid-cols-2 lg:grid-cols-2   lg:px-36  xl:px-48">
                        {features.map((feature) => (
                            <div
                                key={feature.id}
                                className="flex flex-col items-center text-center relative bg-white shadow-lg rounded-lg p-6 min-h-96 my-5"
                            >

                                <div className="flex  border border-8 border-slate-100 justify-center absolute items-center w-20 p-4  h-20 bg-[#024059] rounded-full mb-6" style={{ top:'-34px'}}>
                                    <img src={feature.path} alt={feature.title} className="w-14  w-14 " />
                                </div>


                                <div className="py-20">
                                    <h3 className="text-xl font-semibold text-gray-800">{feature.title}</h3>
                                    <p className="mt-4 text-gray-600 sm:text-base text-sm">{feature.description}</p>
                                </div>


                            </div>
                        ))}
                    </div>
                </div>


            </div>

            {/* Key Features Tailored for Small and Medium E-Commerce Sites */}

            <div className="container mx-auto py-5 mt-9 md:px-6 lg:px-12 items-center justify-between">

                <div className="max-w-screen-xl mx-auto md:px-6 lg:px-12 relative z-10">
                    <div className="grid grid-cols-1 md:grid-cols-12 md:gap-12 py-30">

                        <div className="col-span-12 md:col-span-6 min-h-96">
                            <h3 className="text-[#024059] font-semibold   text-3xl mx-6">Key Features Tailored for Small and Medium E-Commerce Sites</h3>
                            <img src="images/img4.png" alt="OpulaARS Use Case" className="md:w-full rounded-lg  mt-3" />
                        </div>

                        <div className="col-span-12 md:col-span-6 flex  flex-col  pt-5 md:pt-14 justify-center space-y-8 px-10 translate-y-2.5">

                            {keyFeatures.map((kfeature, index) => (
                                <div key={index} className="space-y-4   w-full">
                                    <img src={kfeature.path} alt={kfeature.title} className="w-28 h-28  object-contain" />
                                    <h6 className="text-xl font-medium text-[#024059]">{kfeature.title}</h6>
                                    <p className="lg:text-base text-sm text-[#051114] leading-relaxed">{kfeature.content}</p>
                                </div>
                            ))}
                        </div>




                    </div>

                </div>


            </div>

            {/*   How OpulaARS Can Make Your Store Built Using COTS E-Commerce Platforms Stand Out*/}
            <div className="bg-[#8C6046] w-full  md:p-2 p-8 mt-5 ">
                <div className="text-center text-white text-3xl md:mb-6 text-2xl md:px-32 xl:px-96">
                    <h3 className=" text-center my-3 w-4/5 mx-auto lg:text-4xl md:text-3xl sm:text-2xl text-xl">
                        How OpulaARS Can Make Your Store Built Using COTS E-Commerce Platforms Stand Out
                    </h3>
                </div>
                <div className="container mx-auto py-5 mt-10 sm:px-6 px-0 lg:px-12 items-center justify-between">
                    <div className="flex flex-col md:flex-row items-center">
                        <div className="w-full md:w-3/5 text-white text-lg leading-relaxed md:pl-8">
                            <p className="text-xs sm:text-sm md:text-base lg:text-lg">
                                For smaller businesses built using COTS e-commerce platforms, providing customers with a
                                unique and personalized shopping experience is key to standing out. OpulaARS helps you
                                leverage each customer interaction by recommending products that make sense for your brand’s
                                unique audience. We’re here to make sure every recommendation counts, helping your business
                                grow while maintaining the authentic, brand-specific touch that keeps customers coming
                                back
                            </p>
                        </div>
                        <div className="w-full md:w-2/5 flex justify-center  mb-6 md:mb-0">
                            <div
                                className="relative py-10 bg-cover bg-center justify-items-start "
                                >
                                <img
                                    src="images/img5.png"
                                    alt="small and medium"
                                    className="w-96 h-auto rounded-lg  transform rotate-12 bg-contain"
                                />
                            </div>
                        </div>

                    </div>
                </div>
            </div>

            <h3 className="text-[#024059] text-center font-semibold text-3xl mx-6">
                Shop Assist
            </h3>

            <Carousel3 data={shopAsist} />

            {/* <div
        className="container-fluid relative py-20 bg-cover bg-center text-white p-8 rounded-lg shadow-lg w-96 text-center"
        style={{
            backgroundColor: '#8C6046',
            // clipPath: 'ellipse(2000% 60% at 100% 100%)',
        }}
        > */}
            {/* <div className="flex justify-center items-center mb-40"> */}
                {/* <div className="bg-[#004d80] text-white p-8 rounded-lg shadow-lg w-96 text-center"> */}
                {/* <Carousel3 data={shopAsist} /> */}
                    {/* <div className="flex justify-center mb-4">
                        <div className="w-10 h-10 flex justify-center items-center">
                            <img src="images/icon9.png" alt="Icon" className="w-10 h-10" />
                        </div>
                    </div>

                    <h2 className="text-2xl font-semibold mb-4">What's on offer</h2>

                    <p className="text-sm leading-relaxed mb-6">
                       
                        An app that makes personalized recommendations, considering preferences
                        and historical buying behavior. Users can view alternative options from multiple sites
                        to ensure value and transparency. Payment gateway integration, Buy Now Pay Later (BNPL) options, and
                        targeted advertising. Also on offer consolidated purchase tracking, loyalty programs, and
                        one-click checkout to simplify the buying process.
                    </p> */}

                    {/* <div className="absolute top-1/2 -translate-y-1/2 left-4 cursor-pointer">
                        <span className="text-white text-xl">&#8249;</span>
                    </div>
                    <div className="absolute top-1/2 -translate-y-1/2 right-4 cursor-pointer">
                        <span className="text-white text-xl">&#8250;</span>
                    </div> */}

                    {/* <div className="flex justify-center mt-4 space-x-2">
                        <span className="w-2 h-2 bg-white rounded-full"></span>
                        <span className="w-2 h-2 bg-gray-400 rounded-full"></span>
                        <span className="w-2 h-2 bg-gray-400 rounded-full"></span>
                    </div> */}
                {/* </div> */}
            {/* </div/> */}
            {/* </div> */}



        </>
    );
}