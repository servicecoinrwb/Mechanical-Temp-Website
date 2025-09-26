Mechanical Temp HVAC Website
📌 Project Overview

This repository contains the complete source code for the Mechanical Temp website — a multi-page static site designed for a local HVAC (Heating, Ventilation, and Air Conditioning) service company based in Southfield, MI.

The site is built to be a high-performance lead generation asset. It is fast, fully responsive, and optimized for local SEO. Because it’s a static site (backend-free), it can be deployed easily and at no cost to modern platforms like GitHub Pages or Netlify.

📂 Website Structure

The website is organized into several core HTML files for both customer-facing pages and internal tools:

index.html — The main homepage with a comprehensive overview of services, testimonials, offers, and multiple lead-capture points.

ac-services.html — A dedicated landing page for air conditioning repair, installation, and maintenance.

furnace-services.html — A dedicated landing page for heating and furnace services.

commercial-hvac.html — A dedicated landing page for commercial clients and national accounts.

service-plan.html — A sales page detailing the monthly maintenance plan.

system-selector.html — An interactive, multi-step tool for customers to get a personalized new system estimate.

lead-funnel.html — An internal training and reference tool for office staff to handle incoming website leads.

⭐ Key Features
Advanced Lead Generation Tools

Interactive Appointment Scheduler: A 4-step modal that allows customers to select an exact date and time for service, describe their issue, and provide their contact details.

Interactive System Selector: An e-commerce-style tool that guides customers through choosing a new HVAC system based on their home size and desired efficiency, generating a highly qualified sales lead.

Direct-to-Text Chat Widget: A floating chat bubble opens a lightweight form for customers to enter their name, phone number, and question, enabling immediate follow-up via text message.

SEO & Local Business Optimization

Schema.org Markup: Rich JSON-LD schema is included on all relevant pages to define the business as an HVACBusiness, improving local search visibility.

Unique Metadata: Every page has a custom <title> and <meta name="description"> tag, optimized with relevant keywords.

Google-Friendly: The site includes a sitemap.xml for fast indexing, a placeholder for the Google Search Console verification tag, and links to a Google Business Profile for reviews.

Modern, Responsive Design

Mobile-first build to ensure a seamless experience on all devices.

Sticky, responsive header with a mobile “hamburger” menu for easy navigation.

🛠️ Technologies Used

HTML5 — Core structure and content.

Tailwind CSS — Utility-first styling framework, loaded via CDN for simplicity.

Vanilla JavaScript — Powers interactive features (responsive menu, pop-up modals, form logic).

EmailJS — Client-side service powering all lead-generation forms without a backend (emails and SMS via gateways).

⚙️ Customization & Setup
1) Update Business Information

In each .html file, update the address, phone number, and service areas in:

Visible content (e.g., footer)

Hidden JSON-LD schema in the <head>

2) Configure EmailJS

Create an account at EmailJS.com.

Create three Email Templates to handle the different forms:

Scheduler Template — Main appointment booking

System Selector Template — New system quote requests

Chat Widget Template — Simple chat messages

In each .html file, find the <script> tag at the bottom and replace the placeholder Service ID and Template IDs with your own.

3) Verify with Google Search Console

Add your site to Google Search Console.

Choose the HTML tag verification method and copy your unique verification code.

Paste this code into the placeholder

<meta name="google-site-verification" content="YOUR_CODE_HERE">


in the <head> of index.html.

🚀 Deployment

This is a static website, so no backend setup is required. It can be deployed directly to any provider that serves static HTML files, including:

GitHub Pages

Netlify

Vercel

Standard web hosting
