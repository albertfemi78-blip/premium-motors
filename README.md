# 🚗 Premium Motors – Car Dealership Website

Premium Motors is a Django-powered car dealership website designed to showcase new and used vehicles. It provides customers with an easy way to explore available cars, view vehicle details, and submit enquiries about vehicles they are interested in purchasing.

## 🌐 Live Website

[Visit Premium Motors](https://premium-motors-a496.onrender.com/)

## 📌 Project Overview

Premium Motors was developed to provide a simple and user-friendly online platform for a car dealership.

The website allows visitors to browse available vehicles, explore their specifications, view car images, and contact the dealership through an enquiry form.

The application also includes an administrative dashboard where dealership staff can manage vehicle listings and customer enquiries.

## ✨ Features

* **Homepage:** Introduces the dealership and displays featured vehicles.
* **Car Listings:** Displays available new and used vehicles.
* **Car Details:** Shows vehicle information, specifications, pricing, and images.
* **Car Image Gallery:** Supports multiple images for vehicle listings.
* **Customer Enquiries:** Allows customers to submit enquiries about specific vehicles.
* **Admin Dashboard:** Provides management of cars, car images, and customer enquiries.
* **Responsive Design:** Provides a user-friendly browsing experience across different screen sizes.
* **Cloud Image Storage:** Uses Cloudinary to store vehicle images.
* **Database Integration:** Stores vehicle information and customer enquiries.

## 🛠️ Technologies Used

| Technology   | Purpose                   |
| ------------ | ------------------------- |
| Python       | Backend programming       |
| Django       | Web application framework |
| HTML5        | Website structure         |
| CSS3         | Website styling           |
| JavaScript   | Frontend interactions     |
| PostgreSQL   | Production database       |
| Cloudinary   | Vehicle image storage     |
| Git & GitHub | Version control           |
| Render       | Website deployment        |

## 🚘 Vehicle Information

Each vehicle listing can include:

* Vehicle name and manufacturer
* Model year
* Price
* Vehicle condition (New or Used)
* Transmission type
* Fuel type
* Mileage
* Colour
* Vehicle images
* Availability status

## 📂 Project Structure

```text
premium-motors/
│
├── car_dealership/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── cars/
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── admin.py
│   └── urls.py
│
├── static/
├── media/
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/albertfemi78-blip/premium-motors.git
```

### 2. Navigate to the Project Folder

```bash
cd premium-motors
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables

Create a `.env` file in the project root and configure the environment variables required by your Django settings.

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

For production, configure your database and Cloudinary credentials securely.

Never upload your `.env` file or secret credentials to GitHub.

### 7. Apply Database Migrations

```bash
python manage.py migrate
```

### 8. Create an Administrator Account

```bash
python manage.py createsuperuser
```

### 9. Start the Development Server

```bash
python manage.py runserver
```

Open your browser and visit:

```text
http://127.0.0.1:8000/
```

## 🔐 Admin Dashboard

The Django administration interface allows authorised administrators to:

* Add and update vehicle listings.
* Manage vehicle images.
* Update vehicle availability.
* View customer enquiries.

Access the admin dashboard at:

```text
http://127.0.0.1:8000/admin/
```

## ☁️ Deployment

Premium Motors is deployed using **Render**.

The production setup uses:

* Render for application hosting.
* PostgreSQL for production database management.
* Cloudinary for vehicle image storage.
* Environment variables for sensitive configuration.

## 👨‍💻 Developer

**Albert**

Full-Stack Web Development Learner

### GitHub

[View the Premium Motors Repository](https://github.com/albertfemi78-blip/premium-motors)


