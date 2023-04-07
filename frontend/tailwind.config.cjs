module.exports = {
  content: [
    './index.html',"./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        adelia: ["ADELIA", "cursive"],
      },
    },
  },
  plugins: [require("daisyui")],
};
