import React from 'react';

const PricingPage = () => {
  return (
    <div className='p-5'>
      <h2 className="font-bold mt-20 text-4xl relative text-center text-cyan-950 before:block before:absolute before:w-28 before:h-2 before:rounded-full before:bg-cyan-700 before:text-center before:inset-x-2/4 before:top-14">Pricing and Plan</h2>

      <div className='container pt-7 mx-auto my-10'>
        <h5 className='text-3xl text-cyan-950 mt-12 font-bold'>Lets find the solutions that fit for you</h5>
        <p className='py-5 text-2xl font-light text-cyan-950'>Fill the form below & our expert will get in touch!</p>


        <div className="cst_content flex md:flex-row flex-col mx-auto w-full py-18 justify-center my-2.5">
          <div className='md:w-2/5 w-full'>
            <div className='w-full text-center'>
              <form className='bg-gradient-to-r from-cyan-900 to-sky-400 text-white py-18 rounded-md'>
                <div className='lg:mx-8 mx-2 py-16 text-center'>
                  <div className='col-span-full mx-auto my-5'>
                    <input type='text' className='lg:w-9/12  w-full min-h-12 border rounded-md mx-auto px-4 text-cyan-900' placeholder='First Name' />
                  </div>
                  <div className='col-span-full mx-auto my-5'>
                    <input type='text' className='lg:w-9/12  w-full min-h-12 border rounded-md mx-auto px-4 text-cyan-900' placeholder='Last Name' />
                  </div>
                  <div className='col-span-full mx-auto my-5'>
                    <input type='email' className='lg:w-9/12  w-full min-h-12 border rounded-md mx-auto px-4 text-cyan-900' placeholder='Email Address' />
                  </div>
                  <div className='col-span-full mx-auto my-5'>
                    <input type='email' className='lg:w-9/12  w-full min-h-12 border rounded-md mx-auto px-4 text-cyan-900' placeholder='Enter Company Name' />
                  </div>
                  <div className='col-span-full mx-auto my-5'>
                    <input type='tel' className='lg:w-9/12  w-full min-h-12 border rounded-md mx-auto px-4 text-cyan-900' placeholder='Enter Mobile No' />
                  </div>
                  <div className='col-span-full mx-auto my-5'>
                    <input type='tel' className='lg:w-9/12  w-full min-h-12 border rounded-md mx-auto px-4 text-cyan-900' placeholder='Enter country' />
                  </div>
                  <div className='col-span-full  my-5'>
                    <select className='lg:w-9/12  w-full min-h-12 rounded-md text-cyan-900 px-4'>
                      <option value={'Choose Business type'} selected>Choose Business type</option>
                      <option value={'B2B'} selected>B2B</option>
                      <option value={'B2C'} selected>B2C</option>
                      <option value={'Both'} selected>Both</option>
                    </select>
                  </div>
                  <div className='col-span-full  my-5'>
                    <select className='lg:w-9/12  w-full min-h-12 rounded-md text-cyan-900 px-4'>
                      <option value={'Industary'} selected>Industry</option>
                      <option value={'Ecommerce'}>Ecommerce</option>
                      <option value={'video Streaming'} >video Streaming</option>
                      <option value={'Telecome'} >Telecome</option>
                    </select>
                  </div>
                  <div className='col-span-full  my-5 text-start'>
                    <button className='px-6 py-2 rounded-md mx-16' style={{ backgroundColor:'#6D310E'}}>
                      Submit
                    </button>
                  </div>
                </div>
              </form>
            </div>
          </div>
          <div className='md:w-3/5 w-full'>
            <div className="content py-5 mx-8 py-16 ">
              <h5 className='text-3xl text-cyan-900 text font-bold'>Learn :</h5>
              <div className='cst_context_img flex p-5 my-2 items-center'>
                <img src="images/Arroew_blue.png" className='w-5 h-5'/>
                <p className='mx-2 px-3 w-72 text-cyan-900 font-semibold'>
                  How OpulaARS can make yours online store
                  Stand Out
                </p>
              </div>
              <div className='cst_context_img flex p-5 my-2 items-center'>
                <img src="images/Arroew_blue.png" className='w-5 h-5' />
                <p className='mx-2 px-3 w-72 text-cyan-900 font-semibold'>
                  How to integrate omnichannel seamlessly with your website
                </p>
              </div>
              <div className='cst_context_img flex p-5 my-2 items-center'>
                <img src="images/Arroew_blue.png" className='w-5 h-5' />
                <p className='mx-2 px-3 w-72 text-cyan-900 font-semibold'>
                  How to select the algorithm that gives the best AOV
                </p>
              </div>
              <div className='cst_context_img flex p-5 my-2 items-center'>
                <img src="images/Arroew_blue.png" className='w-5 h-5' />
                <p className='mx-2 px-3 w-72 text-cyan-900 font-semibold'>
                  How to create product & customer segments for targeted content
                </p>
              </div>
             </div>
          </div>
        </div>

      </div>

    </div>
  );
};

export default PricingPage;