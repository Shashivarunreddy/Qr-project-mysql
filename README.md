# Health Data QR Code Generator

This project is a Flask application that allows users to input health data and generates a static QR code containing that data. The information is stored in a MySQL database,
and the QR code can be downloaded for sharing.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Setup MySQL Database](#setup-mysql-database)
4. [Running the Application](#running-the-application)
5. [Usage](#usage)
6. [License](#license)

## Prerequisites

- Python 3.x
- MySQL Server
- pip (Python package installer)
---------------------------------------------------------------------------------------------------------
## Installation

1. **Clone the Repository**

   Open your terminal and run the following command to clone the repository:

   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>

-------------------------------------------------------------------------------------------------------
2. Create a Virtual Environment (optional but recommended)

You can create a virtual environment to manage your project dependencies:

python -m venv venv
Activate the virtual environment:

Windows:

.\venv\Scripts\activate
macOS/Linux:

source venv/bin/activate

------------------------------------------------------------------------------------------------------
3. Install Required Packages

Install the necessary packages by running:

pip install Flask Flask-MySQLdb qrcode[pil]

-----------------------------------------------------------------------------------------------------
4.Setup MySQL Database
 1.Install MySQL Server

Follow the instructions on the MySQL installation guide to install MySQL on your system.

2.Create a Database

After installing MySQL, open your terminal or command prompt and log into the MySQL shell:
mysql -u root -p
(Replace root with your MySQL username if different, and enter your password when prompted.)

3.Run the Following Commands in the MySQL Shell

CREATE DATABASE health_db;
USE health_db;
CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    medical_info TEXT NOT NULL
);


This will create a database named health_db and a table named patients to store health data.

------------------------------------------------------------------------------------------------------
Running the Application

1.Run the Flask Application

In your terminal, ensure you are in the project directory and run:

python app.py


2.Access the Application
Open your web browser and go to http://127.0.0.1:5000/ to access the application.
--------------------------------------------------------------------------------------------------------
Usage
Fill out the form with the following health data:

Name
Age
Medical Info
Click on Generate QR Code. The application will generate a QR code containing the entered data, which you can download.



### Saving the README

- Save this content in a file named `README.md` in the root directory of your project.

Let me know if you need any further modifications or additional sections!
