# Admin Orders Management System

A Flask-based admin panel for managing e-commerce orders with full CRUD operations, status tracking, and detailed order views.

## Features

### Admin Dashboard

* **Admin-only access** with authentication
* **Order listing** with search and filter capabilities
* **Status management** (Pending, Processing, Shipped, Delivered, Cancelled)
* **Detailed order views** with complete customer and product information
* **Order deletion** functionality
* **Print orders** for offline record keeping

### Order Management

* View all orders in a sortable table
* Filter orders by status with badge counters
* Search orders by:

  * Order number
  * Customer name
  * Email address
  * Phone number
* Update order status with one click
* View complete order details including:

  * Customer information (name, email, phone)
  * Complete shipping address (district, upazila, full address)
  * Order items with quantities and pricing
  * Order total
  * Timestamps (created and updated)

## Technology Stack

* **Backend**: Python 3.x with Flask
* **Database**: SQLite (can be upgraded to PostgreSQL/MySQL)
* **ORM**: SQLAlchemy
* **Frontend**: Bootstrap 5, Font Awesome icons
* **Templating**: Jinja2

## Installation

### Prerequisites

* Python 3.8 or higher
* pip (Python package manager)

### Step 1: Clone or Create Project Directory

```bash
mkdir admin-orders-system
cd admin-orders-system

