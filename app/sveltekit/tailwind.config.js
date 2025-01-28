/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        nivaltaBlue: '#3237a7',
		lavenderIndigo: '#8657e1',
		daisyBush: '#4714a5',
		goldenFizz: '#feff40',
		whisper: '#f9f4f9',
		pastelPurple: '#b2a1bb',
		purple: '#7209b7',
		robinEggBlue: '#00e9c0',
		blueGem: '#3813a0',
		caribbeanBlue: '#1CC6A0',
		scarlet: '#f72f45',
		monsoon: '#777878',
		silver: '#c0c0c0',
		gallery: '#efeaf2',
		caribbeanGreen: '#00ca9e',
		fog: '#decaec'
			},
    },
  },
  plugins: [
	require('@tailwindcss/forms'),
  ],
}

