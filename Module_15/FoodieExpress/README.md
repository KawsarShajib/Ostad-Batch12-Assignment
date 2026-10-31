# 🍔 FoodieExpress — Modern & Responsive Food Delivery Landing Page

[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![RemixIcon](https://img.shields.io/badge/RemixIcon-4.1.0-orange?style=for-the-badge)](https://remixicon.com/)

A modern, clean, and fully responsive food delivery landing page built for **FoodieExpress**. Developed strictly using semantic **HTML5** and **Tailwind CSS utilities**, maintaining simplicity, clean architecture, and responsive design across all devices.

---

## 📋 Table of Contents
1. [Project Overview](#-project-overview)
2. [Key Features & Bonus Challenges](#-key-features--bonus-challenges)
3. [Design System & Color Palette](#-design-system--color-palette)
4. [File & Directory Structure](#-file--directory-structure)
5. [Sections Breakdown](#-sections-breakdown)
   - [1. Responsive Navbar](#1-responsive-navbar)
   - [2. Hero Section](#2-hero-section)
   - [3. Food Categories (Bonus)](#3-food-categories-bonus)
   - [4. Popular Dishes Grid with Discount Badges](#4-popular-dishes-grid-with-discount-badges)
   - [5. Why Choose Us?](#5-why-choose-us)
   - [6. Special Offer Section](#6-special-offer-section)
   - [7. Master Chef & About](#7-master-chef--about)
   - [8. Customer Reviews Grid (Bonus)](#8-customer-reviews-grid-bonus)
   - [9. Multi-Column Footer](#9-multi-column-footer)
6. [Tailwind CSS Layout Matrix](#-tailwind-css-layout-matrix)
7. [Running the Project Locally](#-running-the-project-locally)

---

## 🌟 Project Overview

**FoodieExpress** is an intuitive, appetizing landing page crafted for modern food lovers. It empowers visitors to browse gourmet dishes, discover food categories, claim promotional vouchers, read customer testimonials, and effortlessly place food orders.

### Core Goals:
- **HTML & Tailwind CSS Only**: Clean, simple code without any JavaScript bloat or intrusive looping animations.
- **Tailwind CSS Practice**: Rigorous application of Tailwind CSS utility classes for sizing, typography, spacing, flexbox, CSS grid, and responsive breakpoints (`sm:`, `md:`, `lg:`, `xl:`).
- **Aesthetic Consistency**: Strict adherence to the signature warm orange and deep charcoal palette.
- **Responsiveness**: Smooth visual flow across mobile smartphones, tablets, laptops, and desktop monitors.

---

## 🎯 Key Features & Bonus Challenges

| Feature Category | Implementation Details |
| :--- | :--- |
| **Sticky Navbar** | Fixed top navigation with brand logo, all 9 required links, and "Order Now" CTA button. |
| **Mobile Navigation Menu (Bonus)** | Accessible, zero-JS mobile dropdown menu using native HTML `<details>` and `<summary>` styled with Tailwind CSS. |
| **Hero Section** | Dual CTA buttons ("Explore Menu" linked to `#popular` & "Order Now"), floating badges, customer rating badge, and hero dish graphic. |
| **Popular Dishes** | Food cards featuring dish imagery, star ratings, descriptions, strike-through original prices, active prices, and "Order Now" buttons. |
| **Why Choose Us?** | 3 core benefits (*Fast Delivery*, *Fresh Ingredients*, *Affordable Prices*) with color-coded icon boxes (`#62b15c`, `#ff3e67`, `#185adb`). |
| **Special Offer Section** | Eye-catching promo banner with headline *"Get 20% Off Your First Order!"*, copyable coupon code (`FOODIE20`), and a "Claim Offer" button. |
| **Master Chef / About** | Chef spotlight with culinary description, years of experience badge, and quality checklist. |
| **Food Categories (Bonus)** | 4 responsive category cards (**Pizza**, **Burger**, **Drinks**, **Desserts**) with real food photography and item count tags. |
| **Discount Badges (Bonus)** | Floating discount tags on cards (`20% OFF`, `HOT DEAL`, `CHEF'S PICK`, `15% OFF`). |
| **Customer Reviews (Bonus)** | Responsive 3-card customer testimonials grid showcasing verified patrons with ratings, quotes, avatars, and roles. |
| **Footer** | 5-column layout with brand mission, legal/product links, and **5 social media links** (Facebook, Instagram, Twitter/X, LinkedIn, YouTube). |

---

## 🎨 Design System & Color Palette

The project employs a tailored color system embedded directly into the Tailwind configuration:

| Token Name | Hex Code | Tailwind Utility | Semantic Purpose |
| :--- | :--- | :--- | :--- |
| **Primary** | `#fc7f09` | `bg-primary`, `text-primary` | Main brand color, primary CTA buttons, badges |
| **Primary Dark** | `#db6e09` | `hover:bg-primary-dark` | Button hover states |
| **Primary Light** | `#fffcfa` | `bg-primary-light` | Section alternating background, warm card accents |
| **Text Dark** | `#18181b` | `text-textDark` | Primary headings, brand text, card titles |
| **Text Light** | `#6b7280` | `text-textLight` | Subheadings, body copy, descriptions, footer links |
| **Success Green** | `#62b15c` | `bg-[#62b15c]` | Fast delivery badge |
| **Accent Red** | `#ff3e67` | `bg-[#ff3e67]` | Fresh ingredients icon badge, 20% discount tag |
| **Accent Blue** | `#185adb` | `bg-[#185adb]` | Affordable prices icon badge |
| **Font Family** | `'Poppins'` | `font-poppins` | Modern, clean geometric sans-serif typography |

---

## 📁 File & Directory Structure

```text
FoodieExpress/
├── assets/                     # Media & photography assets
│   ├── category-burger.jpg     # Gourmet burger category image
│   ├── category-dessert.jpg    # Molten lava cake category image
│   ├── category-drinks.jpg     # Fruit cooler & mocktail category image
│   ├── category-pizza.jpg      # Artisan pepperoni pizza category image
│   ├── chef.png                # Master executive chef portrait
│   ├── client-1.jpg            # Customer avatar 1
│   ├── client-2.jpg            # Customer avatar 2
│   ├── client-3.jpg            # Customer avatar 3
│   ├── explore.png             # Special offer food graphic
│   ├── header.png              # Hero header dish graphic
│   ├── special-1.png           # Chicken Veg Curry dish
│   ├── special-2.png           # Chicken Veg Stir-Fry dish
│   ├── special-3.png           # Chicken Veg Pasta dish
│   └── topping.png             # Background decorative topping
├── index.html                  # Main application markup (Pure HTML & Tailwind CSS)
├── styles.css                  # Typography, theme variables, and custom scrollbar
└── README.md                   # Comprehensive project documentation
```

---

## 🧱 Sections Breakdown

### 1. Responsive Navbar
- Sticky glassmorphism header (`sticky top-0 z-50 bg-white/95 backdrop-blur-md`).
- Brand logo with restaurant icon.
- Full 9 navigation links: **Home**, **Menu**, **Category**, **Popular**, **Special Offer**, **Clients**, **About**, **Contact Us**.
- **Order Now** primary call-to-action button.
- Mobile drawer navigation implemented purely with HTML `<details>` and `<summary>`.

### 2. Hero Section
- High-converting headline: *"Delicious Food Delivered to Your Door."*
- Highlighted badge: *"🚀 Free Delivery On Your First 3 Orders!"*
- *"Explore Menu"* smoothly linked to `#popular`.
- *"Order Now"*.
- Social proof with customer avatars and a 4.9/5.0 star rating.
- Hero dish image 

### 3. Food Categories (Bonus)
- Responsive 2-to-4 column grid (`grid-cols-2 lg:grid-cols-4`).
- Categories: **Artisan Pizza**, **Gourmet Burgers**, **Coolers & Drinks**, **Molten Desserts**.
- Custom category images, quantity counts, and quick-link triggers.

### 4. Popular Dishes Grid with Discount Badges
- 4 rich dish cards (`grid-cols-1 sm:grid-cols-2 lg:grid-cols-4`).
- Each card features: dish photography, star rating, dish title, short description, struck-through original price, active selling price, and an *"Order Now"* button.
- Floating discount badges on each card 

### 5. Why Choose Us?
- 3 distinct value propositions:
  - **Fast Delivery** 
  - **Fresh Ingredients** 
  - **Affordable Prices** 

### 6. Special Offer Section
- Vibrant promotional card with warm gradient.
- Promotional headline: *"Get 20% Off Your First Order!"*
- Coupon display with code `FOODIE20`.
- *"Claim Offer"* button linking directly to the menu.

### 7. Master Chef & About
- Master chef portrait with *"25+ Years Culinary Mastery"* badge.
- Headline *"Cooked By The Best Chefs In The World"*.
- Value checklist with colorful checkmark icons.

### 8. Customer Reviews Grid (Bonus)
- A clean, fast-loading 3-column responsive grid 
- Verified reviews from customers with 5-star ratings and customer avatars.

### 9. Multi-Column Footer
- 5-column layout with brand mission and information links.
- **5 Social media links**: Facebook, Instagram, Twitter/X, LinkedIn, and YouTube.
- Dhaka, Bangladesh business address, contact email, and phone number.
- Copyright statement.

---

## 📐 Tailwind CSS Layout Matrix

| Breakpoint Prefix | Screen Width | Typical Device | Usage in FoodieExpress |
| :--- | :--- | :--- | :--- |
| **Default** | `< 640px` | Mobile smartphones | 1-column layout, compact cards, hamburger menu |
| **`sm:`** | `≥ 640px` | Large phones, phablets | 2-column food grids, expanded headings |
| **`md:`** | `≥ 768px` | Tablets | 3-column benefits & reviews, 2-column footer |
| **`lg:`** | `≥ 1024px` | Laptops & small desktops | 4-column dish cards & categories, 12-col hero |
| **`xl:`** | `≥ 1280px` | Desktops & large monitors | Full desktop navigation bar with auth buttons |

---

## 🚀 Running the Project Locally

No Node.js, npm, or build step is required!

1. Clone or open the project folder in your editor:
   ```bash
   cd FoodieExpress
   ```
2. Double-click `index.html` or open it with any web browser.
3. Alternatively, launch a simple HTTP server:
   ```bash
   python -m http.server 3000
   ```

---
