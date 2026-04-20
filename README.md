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