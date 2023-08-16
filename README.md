# Property Rental Marketplace Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
3. [Project Overview](#project-overview)
    - [Architecture](#architecture)
    - [Folder Structure](#folder-structure)
4. [Configuration](#configuration)
    - [Environment Variables](#environment-variables)
    - [Database Setup](#database-setup)
    - [Third-Party Integrations](#third-party-integrations)
5. [Development](#development)
    - [Running the Development Server](#running-the-development-server)
    - [Code Guidelines](#code-guidelines)
6. [Deployment](#deployment)
    - [Deployment Platforms](#deployment-platforms)
    - [Deploying the Application](#deploying-the-application)
7. [Testing](#testing)
    - [Unit Tests](#unit-tests)
    - [Integration Tests](#integration-tests)
8. [Troubleshooting](#troubleshooting)
    - [Common Issues](#common-issues)
    - [Debugging](#debugging)
9. [Contributing](#contributing)
    - [Version Control](#version-control)
    - [Pull Requests](#pull-requests)
10. [Contact](#contact)
11. [License](#license)

## Introduction <a name="introduction"></a>

<img src="https://github.com/AlexDimov-04/Property-Rental-Marketplace---RentWise/assets/106152399/009a2fc3-56b9-47f9-840e-23e09e058e0b">

Welcome to the Property Rental Marketplace - RentWise project documentation. This document provides comprehensive information about the project's architecture, setup, development guidelines, deployment process, testing, and more.

## Getting Started <a name="getting-started"></a>

### Prerequisites <a name="prerequisites"></a>

This project enhance some of the following dependencies, you can aquire to your environment.

- Python 3.10 or newer
- PostgreSQL database
- Stripe API keys
- AWS s3 bucket keys (for storing media files)
- SMTP email server configuration

### Installation <a name="installation"></a>

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/property-rental-marketplace.git
   cd property-rental-marketplace
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project Overview <a name="project-overview"></a>

### Architecture and Project Overview <a name="architecture"></a>

#### Description:

The Property Rental Marketplace is a robust web application built using the Django framework. It empowers users to seamlessly list, explore, and transact properties, creating a dynamic platform for property rental and sales. The application adheres to the Model-View-Template (MVT) architectural pattern, ensuring organized and efficient development.

#### Key Features:

- User-Friendly Interface: The platform offers a user-friendly interface where users can effortlessly create accounts, enabling them to efficiently list their properties.

- Property Listing Variety: The application caters to a diverse array of property types, including Villas, Offices, and Apartments, available for Rent, Sale, or as Featured listings.

- Advanced Property States: Properties can be categorized with specific states, such as For Rent, For Sale, and Featured, allowing users to easily filter and discover relevant listings.

- Customizable Offer Creation: Users have the flexibility to create offers for their properties, providing detailed information and images to attract potential clients.

- Estimate Calculator: The built-in estimate calculator employs a sophisticated formula that analyzes property specifics, offering users an accurate estimate of potential earnings or costs.

- Newsletter Subscription: Users can stay informed about the latest property listings and updates by subscribing to the newsletter.

- Automated Notifications: The application leverages Django signals to send timely notifications to users whenever new properties are listed or other important actions occur.

- Customized Admin Dashboard: The admin interface features a tailored dashboard, empowering staff members to manage user integrations based on their assigned roles and responsibilities.

- Secure Payment Processing: Seamless payment processing is integrated using the Stripe API, allowing users to make secure transactions. A cancel/success message promptly informs users about their transaction status.

#### Technical Highlights:

The application is developed on the Django framework, providing a solid foundation for rapid development and maintainability.
Customized Django signals enhance user engagement by delivering real-time notifications.
Utilization of the Stripe API ensures secure and seamless payment processing for property transactions.
The calculator employs a proven formula to accurately estimate property-related costs and earnings.

#### Conclusion:

The Property Rental Marketplace is a comprehensive web application that facilitates property listing, browsing, and transactions. Its intuitive interface, diverse property categories, and advanced features make it a versatile platform for both property owners and potential renters/buyers. The integration of modern technologies ensures secure payment processing and efficient property estimation. With its user-friendly design and innovative functionalities, the Property Rental Marketplace is poised to transform the property rental and sales landscape.

### Front end <a name="Front end"></a>
Used Front End tools + UI interface
- Bootstrap
- Jquery
- Vanilla JS
- Django Template Language

### Folder Structure <a name="folder-structure"></a>

- `property_rental_marketplace/`: Core Django project directory.
- `property_market/`: App for property listing and management.
- `user_authentication/`: App for user registration and authentication.
- `profile_management/`: App for user profile management.
- `static/`: Static assets (CSS, JS, images). -> uploaded to aws s3 bucket service
- `media/`: User-uploaded media files (property images). -> uploaded to aws s3 bucket service
- `templates/`: HTML templates.

## Configuration <a name="configuration"></a>

### Environment Variables <a name="environment-variables"></a>

The project uses environment variables for security enhancement it stores the aws, stripe and smtp configurations in .env file
in the root directorty. It is also in the .gitignore.

### Database Setup <a name="database-setup"></a>

Create a PostgreSQL database and update the `DATABASES` configuration in `settings.py`.

### Third-Party Integrations <a name="third-party-integrations"></a>

Integrate AWS S3 for media storage and Stripe for payment processing. Configure email settings for sending notifications.

## Development <a name="development"></a>

### Running the Development Server <a name="running-the-development-server"></a>

To run the development server:
```bash
python manage.py runserver
```

### Code Guidelines <a name="code-guidelines"></a>

Follow PEP 8 style guidelines. Use Django's Model-View-Template (MVT) architecture and create modular, reusable components.

## Deployment <a name="deployment"></a>

### Deployment Platforms <a name="deployment-platforms"></a>

The project will be deployed later on platforms like Heroku, AWS, or similar cloud services.

### Deploying the Application <a name="deploying-the-application"></a>

Follow the deployment documentation specific to the chosen platform.

## Testing <a name="testing"></a>

### Unit Tests <a name="unit-tests"></a>

Run unit tests using:
```bash
python manage.py test
```

### Integration Tests <a name="integration-tests"></a>

Integrate third-party testing tools (e.g., pytest-django) for integration tests.

## Troubleshooting <a name="troubleshooting"></a>

### Common Issues <a name="common-issues"></a>

- The project is open source, if you have any suggestions of improvement, fork the repo and make pull request.
