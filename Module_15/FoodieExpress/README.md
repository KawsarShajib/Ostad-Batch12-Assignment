# 🍔 FoodieExpress — Modern & Responsive Food Delivery Landing Page

A modern, clean, and fully responsive food delivery landing page built for **FoodieExpress**. Developed strictly using semantic **HTML5** and **Tailwind CSS utilities**, maintaining simplicity, clean architecture, and responsive design across all devices.

---

## 📋 Table of Contents

1. [Project Overviews](#-project-overview)
2. [Key Features & Bonus Challenges](#-key-features--bonus-challenges)
3. [File & Directory Structure](#-file--directory-structure)
4. [Sections Breakdown](#-sections-breakdown)
   - [1. Responsive Navbar](#1-responsive-navbar)
   - [2. Hero Section](#2-hero-section)
   - [3. Food Categories (Bonus)](#3-food-categories-bonus)
   - [4. Popular Dishes Grid with Discount Badges](#4-popular-dishes-grid-with-discount-badges)
   - [5. Why Choose Us?](#5-why-choose-us)
   - [6. Special Offer Section](#6-special-offer-section)
   - [7. Master Chef & About](#7-master-chef--about)
   - [8. Customer Reviews Grid (Bonus)](#8-customer-reviews-grid-bonus)
   - [9. Multi-Column Footer](#9-multi-column-footer)
5. [Tailwind CSS Layout Matrix](#-tailwind-css-layout-matrix)
6. [Running the Project Locally](#-running-the-project-locally)

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

| Feature Category                   | Implementation Details                                                                                                                     |
| :--------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------- |
| **Sticky Navbar**                  | Fixed top navigation with brand logo, all 9 required links, and "Order Now" CTA button.                                                    |
| **Mobile Navigation Menu (Bonus)** | Accessible, zero-JS mobile dropdown menu using native HTML `<details>` and `<summary>` styled with Tailwind CSS.                           |
| **Hero Section**                   | Dual CTA buttons ("Explore Menu" linked to `#popular` & "Order Now"), floating badges, customer rating badge, and hero dish graphic.       |
| **Popular Dishes**                 | Food cards featuring dish imagery, star ratings, descriptions, strike-through original prices, active prices, and "Order Now" buttons.     |
| **Why Choose Us?**                 | 3 core benefits (_Fast Delivery_, _Fresh Ingredients_, _Affordable Prices_) with color-coded icon boxes (`#62b15c`, `#ff3e67`, `#185adb`). |
| **Special Offer Section**          | Eye-catching promo banner with headline _"Get 20% Off Your First Order!"_, copyable coupon code (`FOODIE20`), and a "Claim Offer" button.  |
| **Master Chef / About**            | Chef spotlight with culinary description, years of experience badge, and quality checklist.                                                |
| **Food Categories (Bonus)**        | 4 responsive category cards (**Pizza**, **Burger**, **Drinks**, **Desserts**) with real food photography and item count tags.              |
| **Discount Badges (Bonus)**        | Floating discount tags on cards (`20% OFF`, `HOT DEAL`, `CHEF'S PICK`, `15% OFF`).                                                         |
| **Customer Reviews (Bonus)**       | Responsive 3-card customer testimonials grid showcasing verified patrons with ratings, quotes, avatars, and roles.                         |
| **Footer**                         | 5-column layout with brand mission, legal/product links, and **5 social media links** (Facebook, Instagram, Twitter/X, LinkedIn, YouTube). |

---

## 📁 File & Directory Structure

```text
FoodieExpress/
├── assets/                     # Media & photography assets
│   ├── category-burger.jpg
│   ├── category-dessert.jpg
│   ├── category-drinks.jpg
│   ├── category-pizza.jpg
│   ├── chef.png
│   ├── client-1.jpg
│   ├── client-2.jpg
│   ├── client-3.jpg
│   ├── explore.png
│   ├── header.png
│   ├── special-1.png
│   ├── special-2.png
│   ├── special-3.png
│   └── topping.png
├── index.html                  # Main application
├── styles.css                  # Typography, theme variables, and custom scrollbar
└── README.md                   # Project documentation
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

- High-converting headline: _"Delicious Food Delivered to Your Door."_
- Highlighted badge: _"🚀 Free Delivery On Your First 3 Orders!"_
- _"Explore Menu"_ smoothly linked to `#popular`.
- _"Order Now"_.
- Social proof with customer avatars and a 4.9/5.0 star rating.
- Hero dish image

### 3. Food Categories (Bonus)

- Responsive 2-to-4 column grid (`grid-cols-2 lg:grid-cols-4`).
- Categories: **Artisan Pizza**, **Gourmet Burgers**, **Coolers & Drinks**, **Molten Desserts**.
- Custom category images, quantity counts, and quick-link triggers.

### 4. Popular Dishes Grid with Discount Badges

- 4 rich dish cards (`grid-cols-1 sm:grid-cols-2 lg:grid-cols-4`).
- Each card features: dish photography, star rating, dish title, short description, struck-through original price, active selling price, and an _"Order Now"_ button.
- Floating discount badges on each card

### 5. Why Choose Us?

- 3 distinct value propositions:
  - **Fast Delivery**
  - **Fresh Ingredients**
  - **Affordable Prices**

### 6. Special Offer Section

- Vibrant promotional card with warm gradient.
- Promotional headline: _"Get 20% Off Your First Order!"_
- Coupon display with code `FOODIE20`.
- _"Claim Offer"_ button linking directly to the menu.

### 7. Master Chef & About

- Master chef portrait with _"25+ Years Culinary Mastery"_ badge.
- Headline _"Cooked By The Best Chefs In The World"_.
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

| Breakpoint Prefix | Screen Width | Typical Device            | Usage in FoodieExpress                         |
| :---------------- | :----------- | :------------------------ | :--------------------------------------------- |
| **Default**       | `< 640px`    | Mobile smartphones        | 1-column layout, compact cards, hamburger menu |
| **`sm:`**         | `≥ 640px`    | Large phones, phablets    | 2-column food grids, expanded headings         |
| **`md:`**         | `≥ 768px`    | Tablets                   | 3-column benefits & reviews, 2-column footer   |
| **`lg:`**         | `≥ 1024px`   | Laptops & small desktops  | 4-column dish cards & categories, 12-col hero  |
| **`xl:`**         | `≥ 1280px`   | Desktops & large monitors | Full desktop navigation bar with auth buttons  |

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
