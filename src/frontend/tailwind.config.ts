import type { Config } from "tailwindcss";

export default {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      backgroundImage: {
        bannerImg: "url('../../public/bg.png')",
        blackOverlay: "linear-gradient(to bottom, rgba(0,0,0,0) 0%, rgba(0,0,0,0.8) 100%)",
      },
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        lavender: {
          900: '#3c2a4d',
          800: '#523d66',
          700: '#6d4f84',
          600: '#8763a2',
          500: '#a27dc1',
        },
      },
    },
  },
  plugins: [],
} satisfies Config;
