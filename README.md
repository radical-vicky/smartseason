# SmartSeason - Field Monitoring System

A comprehensive field monitoring system for tracking crop progress across multiple fields during growing seasons. Built with Django, this system supports role-based access for Coordinators (Admins) and Field Agents.

## Live Demo

[Deploy your project on Render and add the link here]

## Demo Credentials

| Role | Username | Password |
|------|----------|----------|
| Coordinator (Admin) | admin | admin123 |
| Field Agent | agent1 | agent123 |
| Field Agent | agent2 | agent123 |
| Field Agent | agent3 | agent123 |

## Features

### Role-Based Access
- **Coordinator (Admin)**: Full access to all fields, agent management, and system oversight
- **Field Agent**: Access only to assigned fields with update capabilities

### Field Management
- Create, edit, and delete fields
- Assign fields to specific field agents
- Upload field images (Cloudinary storage)
- Track crop types, planting dates, and current stages

### Field Stages
- Planted → Growing → Ready → Harvested

### Smart Status Logic
- **Active**: Progressing normally within expected timelines
- **At Risk**: Exceeds expected duration for current stage
  - Planted > 30 days (should have germinated)
  - Growing > 90 days (should be maturing)
  - Ready > 120 days (should have been harvested)
- **Completed**: Field has reached harvested stage

### Field Updates
- Agents can update stages and add observations
- Complete history of all updates
- Image upload support

### Dashboards
- **Coordinator Dashboard**: Overview of all fields, agent performance, crop distribution, recent activity
- **Agent Dashboard**: Assigned fields, pending updates, needs attention alerts

### Additional Features
- Image upload with Cloudinary CDN storage
- Mobile-responsive design
- Password reset functionality
- User profiles

## Tech Stack

- **Backend**: Django 5.1
- **Database**: SQLite (development) / PostgreSQL (production)
- **Authentication**: django-allauth
- **Image Storage**: Cloudinary
- **Frontend**: Tailwind CSS
- **Server**: Gunicorn

## Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Virtual environment (recommended)
- Cloudinary account (for image storage)

### Step-by-Step Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/smartseason.git
cd smartseason



# Django Core Settings
SECRET_KEY=django-insecure-5ozkg(1)uc64l627epzz2t+6o_&r52juf($)8$4gxf*$@8f3lz
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3

# MPESA Configuration (keep as is)
MPESA_CONSUMER_KEY=LQost6BhC09UpLKaYjbRunq3IZN1ylfzHzI8tz47jxlaVHvI
MPESA_CONSUMER_SECRET=Kn2l7P0mCnFAJAi7KdOMsIRkpAsH698PBLbhG5EqVRc7CY27pv6d0U96hEhmByo6
MPESA_SHORTCODE=174379
MPESA_SHORTCODE_TYPE=paybill
MPESA_PASSKEY=bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919
MPESA_CALLBACK_URL=https://galaxystore1.onrender.com/mpesa/callback/
MPESA_ENVIRONMENT=sandbox
MPESA_INITIATOR_NAME=testapi
MPESA_INITIATOR_PASSWORD=Safaricom2018

# Cloudinary
CLOUDINARY_CLOUD_NAME=dvuooxbqi
CLOUDINARY_API_KEY=875143959481713
CLOUDINARY_API_SECRET=BsLyRtEvfVCEZOdQ6JWnY6mTEqI

OPENAI_API_KEY=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
GROQ_API_KEY=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





EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000


AFRICASTALKING_USERNAME = 'sandbox'  
AFRICASTALKING_API_KEY = ''