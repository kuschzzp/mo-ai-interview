import forms from '@tailwindcss/forms';

/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            borderRadius: {
                'button': '0.5rem',
            }
        },
    },
    plugins: [
        forms,
    ],
}
