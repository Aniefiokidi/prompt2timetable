/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cu: {
          purple: '#4B286D', // Royal purple
          gold: '#C9A84C',   // Gold
          navy: '#003366',   // Navy (optional)
        },
      },
    },
  },
  plugins: [],
}
