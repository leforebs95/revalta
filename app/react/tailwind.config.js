/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        nivaltaBlue: '#5F57FF' // keeping your custom color
      }
    },
  },
  plugins: [],
}