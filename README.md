# Mechanical Temp HVAC Website

## 📌 Project Overview
This repository contains the complete source code for the **Mechanical Temp** website — a multi-page static site designed for a local HVAC (Heating, Ventilation, and Air Conditioning) service company based in **Southfield, MI**.  

The site is:
- Fast and responsive  
- Optimized for lead generation  
- Built entirely with **modern front-end technologies**  
- Backend-free (deployable to GitHub Pages, Netlify, or standard hosting)

---

## 📂 Website Structure
The website is organized into several core HTML files:

- **`index.html`** — Homepage with services overview, testimonials, offers, and lead captures.  
- **`ac-services.html`** — Air conditioning repair, installation, and maintenance.  
- **`furnace-services.html`** — Heating and furnace services.  
- **`commercial-hvac.html`** — Commercial HVAC and national accounts.  
- **`service-plan.html`** — Monthly maintenance plan details.  
- **`blog.html`** — Blog index listing articles.  
- **`blog-post-1.html`** — Example blog article (new posts follow this template).  

---

## ⭐ Key Features

### 1. Interactive Appointment Scheduler
- **Multi-Step Form:** 4-step modal for selecting date, time, and contact details.  
- **EmailJS Integration:** Sends appointments to company emails and SMS gateways.  
- **Spam Prevention:** Simple math captcha included.  

### 2. Direct-to-Text Chat Widget
- **Floating Icon:** Persistent bottom-right chat bubble.  
- **Clean Interface:** Opens lightweight chat form.  
- **Backend-Free Messaging:** Uses EmailJS to send messages as text/email.  

### 3. SEO & Local Business Optimization
- **Schema.org Markup:** JSON-LD schema for `HVACBusiness`.  
- **Unique Metadata:** Custom `<title>` and `<meta>` descriptions for every page.  
- **Google-Friendly:** Optimized mobile layout + review links.  

### 4. Blog System
- Lightweight blog powered by static HTML.  
- **`blog.html`** as the index.  
- Each article is its own **`blog-post-x.html`** file.  

---

## 🛠️ Technologies Used
- **HTML5** — Core structure.  
- **Tailwind CSS** — Utility-first styling via CDN.  
- **Vanilla JavaScript** — Interactive features (menu, modal, chat).  
- **EmailJS** — Client-side email + SMS integration.  

---

## ⚙️ Customization & Setup

To adapt this website for your own business:

1. **Update EmailJS Credentials**  
   - Replace `emailjs.init("YOUR_USER_ID")` with your EmailJS User ID.  
   - Update `service_id` and `template_id` in `emailjs.send()` calls.  

2. **Edit Recipient Information**  
   - Inside `sendAppointmentEmail()` and `sendChatMessage()`, replace the default recipient emails/SMS gateway addresses with your own.  

---

## 🚀 Deployment
The site can be deployed directly to:  
- **GitHub Pages**  
- **Netlify**  
- **Standard web hosting providers**  

No backend setup required.  
