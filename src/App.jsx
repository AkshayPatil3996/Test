import Home from './pages/homepage/Home'
import PricingPage  from './pages/pricingpage/Pricing';
import Product from './pages/productpage/Product';
import BlogPage from './pages/blogpage/Blog';
import TermsAndCondition from './pages/Termsandconditionpage/termsandcondition';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"; 
import Contactpage from './pages/contactpage/Contact';
import HiringPage from './pages/hiringpage/hiring';
import RegistrationPage from './pages/registrationpage/SignUp';
// import RegistrationPageTest from './pages/registrationpage/SignUp1';
import LoginPage from './pages/loginpage/Login';
import Layout from './components/layout/layout';
import PrivacyPolicy from './pages/privacypolicy/Privacy';
import ChooseCategory from './pages/category/Chosecategory';


function App(){
    return (
      <Router>
      <Routes>

        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="/product" element={<Product />} />
          <Route path="/pricing" element={<PricingPage />} />
          <Route path="/blog" element={<BlogPage />} />
          <Route path="/terms" element={<TermsAndCondition />} />
          <Route path="/privacy/policy" element={<PrivacyPolicy />} />
          <Route path="/contact" element={<Contactpage />} />
          <Route path="/hiring" element={<HiringPage />} />
        </Route>
        
        {/* <Route path="/registertest" element={<RegistrationPageTest />} /> */}

 
        <Route path="/register" element={<RegistrationPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/category" element={<ChooseCategory />} />
        
      </Routes>
    </Router>
    );
}


export default App;

