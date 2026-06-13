/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./public/index.html",
    "./src/**/*.{js,jsx}",
  ],

  theme: {
    extend: {
      colors: {
        navy: "#0A1A2F",
        gold: "#C9A03D",
        whiteColor: "#FFFFFF",
        lightGray: "#F5F5F5",
        darkGray: "#333333",
        success: "#10B981",
        error: "#EF4444",
      },

      fontFamily: {
        heading: ["Playfair Display", "serif"],
        body: ["Inter", "sans-serif"],
      },

      spacing: {
        xs: "4px",
        sm: "8px",
        md: "16px",
        lg: "24px",
        xl: "32px",
        "2xl": "48px",
        "3xl": "64px",
      },
    },
  },

  plugins: [],
};