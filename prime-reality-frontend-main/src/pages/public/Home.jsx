import Navbar from "../../components/common/Navbar";
import HeroSection from "../../components/home/HeroSection";
import LandTypesSection from "../../components/home/LandTypesSection";
import StatsCTASection from "../../components/home/StatsCTASection";
import TestimonialsCarousel from "../../components/home/TestimonialsCarousel";
import Footer from "../../components/common/Footer";

// home page
// final design ke sections yahan combine ho rahe hain

function Home() {
  return (
    <>
      {/* navbar */}
      <Navbar />

      {/* hero section */}
      <HeroSection />

      {/* land type section */}
      <LandTypesSection />

      {/* stats and CTA section */}
      <StatsCTASection />

      {/* testimonials section - teammate work */}
      <TestimonialsCarousel />

      {/* footer - teammate work */}
      <Footer />
    </>
  );
}

export default Home;