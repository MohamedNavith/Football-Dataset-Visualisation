/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        dark: '#0f172a',  // Deep blue-black background
        card: '#1e293b',  // Lighter blue-black for cards
        accent: '#3b82f6', // Bright Blue for highlights
      }
    },
  },
  plugins: [],
}