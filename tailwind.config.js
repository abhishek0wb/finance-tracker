/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './templates/**/*.html',
    './expenses/templates/**/*.html',
    './users/templates/**/*.html',
    './static/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        // Professional Business Color Palette
        primary: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',  // Deep Navy - Primary
        },
        success: {
          50: '#ecfdf5',
          100: '#d1fae5',
          200: '#a7f3d0',
          300: '#6ee7b7',
          400: '#34d399',
          500: '#10b981',
          600: '#059669',  // Refined Emerald - Income
          700: '#047857',
          800: '#065f46',
          900: '#064e3b',
        },
        danger: {
          50: '#fef2f2',
          100: '#fee2e2',
          200: '#fecaca',
          300: '#fca5a5',
          400: '#f87171',
          500: '#ef4444',
          600: '#e11d48',  // Subtle Rose/Crimson - Expense
          700: '#be123c',
          800: '#9f1239',
          900: '#881337',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        serif: ['Georgia', 'Cambria', 'Times New Roman', 'serif'],
      },
      backdropBlur: {
        xs: '2px',
      },
      borderRadius: {
        'professional': '8px',  // Subtle, structured rounding
      },
    },
  },
  plugins: [
    require('daisyui'),
  ],
  daisyui: {
    themes: [
      {
        business: {
          "primary": "#0f172a",      // Deep Navy
          "secondary": "#475569",    // Slate Gray
          "accent": "#059669",       // Refined Emerald
          "neutral": "#1e293b",      // Dark Slate
          "base-100": "#ffffff",     // Pure White
          "base-200": "#f8fafc",     // Very Light Slate
          "base-300": "#e2e8f0",     // Light Slate (borders)
          "info": "#0ea5e9",
          "success": "#059669",      // Refined Emerald
          "warning": "#f59e0b",
          "error": "#e11d48",        // Subtle Rose/Crimson
        },
      },
    ],
  },
}
