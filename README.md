# 🏢 Business Intelligence Dashboard

<div align="center">

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.3.x-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![MUBAS Student](https://img.shields.io/badge/MUBAS-3rd_Year_MIS-purple)
![Status](https://img.shields.io/badge/status-in_development-yellow)

**Turning Business Data into Smart Decisions - A Student Project**

</div>

## 📖 What's This About?

Hello! I'm Gomezgani Chirwa, a 3rd year BIT student at MUBAS. This is my main project for the Programming III module (CIS-PRO-313).

I built this dashboard because I noticed many small businesses in Malawi still use manual spreadsheets and paper records. This makes it hard for them to see how their business is really doing. So I thought: what if I could build a simple but powerful system that shows everything in one place?

This isn't just another school project for me. I'm trying to build something that could actually help real businesses while showing what I've learned in all my courses this semester.

## 🎓 How This Connects to My Studies

This year at MUBAS, I'm taking 6 modules. This project uses something from each one:

| Subject | What I Used Here |
|---------|------------------|
| **Programming III** | Python, Flask, making everything work together |
| **Database Admin** | MySQL database design, making it fast and secure |
| **Financial Accounting** | Profit/loss reports, balance sheet views |
| **Computer Graphics** | Charts and data visualizations |
| **Operating Systems** | Making it run smoothly on servers |
| **Research Methods** | Testing with users, documenting everything |

## ✨ What Can This Dashboard Do?

### For Business Owners:
- **See sales right now** - No waiting for end-of-month reports
- **Know what's in stock** - Get warnings before you run out
- **Understand customers** - See who buys most and when
- **Track money** - Income, expenses, and profits all in one place

### Technical Stuff I Implemented:
- **Live updates** - Data refreshes every few minutes
- **Secure login** - Different views for managers and staff
- **PDF reports** - One-click download for meetings
- **Mobile friendly** - Check your business from your phone
- **Backup system** - Automatic daily database backups

## 📸 See It in Action

*(I'll add screenshots here once I build the interface)*

**Dashboard View:**
[ Sales Chart Image ]
[ Inventory Status Image ]
[ Recent Activity Image ]

**Mobile View:**
[ Phone Screenshot ]


## 🛠️ How to Set It Up (For Developers)

If you're a student or developer who wants to run this locally:

### What You Need First:
- Python 3.9 or higher
- MySQL installed on your computer
- Git (to download the project)

### Step-by-Step Installation:

```bash
# 1. Get the code
git clone https://github.com/kafuvula/business-intelligence-dashboard.git
cd business-intelligence-dashboard

# 2. Install Python packages
pip install -r requirements.txt

# 3. Set up your database
mysql -u root -p < database/setup.sql

# 4. Run the application
python run.py

# 5. Open in browser
# Go to: http://localhost:5000

```

Default Login (for testing):
Manager: admin@test.com / password123

Staff: staff@test.com / password123

(Change these immediately if deploying for real use!)



📁 How the Project is Organized

 ```bash

business-dashboard/
├── app/                    # Main application folder
│   ├── __init__.py        # Makes this a Python package
│   ├── routes.py          # All website pages
│   ├── models.py          # Database tables structure
│   ├── auth.py            # Login and security
│   └── utils.py           # Helper functions
├── templates/             # HTML pages
│   ├── dashboard.html     # Main dashboard
│   ├── login.html         # Login page
│   └── reports.html       # Reports page
├── static/               # CSS, JavaScript, images
│   ├── css/
│   ├── js/
│   └── images/
├── database/             # Database files
│   ├── setup.sql         # Creates tables
│   └── sampledata.sql    # Example data
├── tests/               # Testing files
│   ├── test_auth.py     # Login tests
│   └── test_dashboard.py # Dashboard tests
├── requirements.txt     # Python packages needed
├── config.py           # Settings (don't share publicly!)
├── run.py              # Starts the application
└── README.md           # This file!
```

```bash
🔧 What I'm Working On Now
This Week's Goals:
Set up basic Flask application
Create database tables
Design main dashboard layout
Add sales chart
Create login system
Write tests for core features

Coming Soon:
Email alerts for low stock
Customer loyalty tracking
Expense categorization
Multi-business support (for franchises)

🤝 Want to Help or Learn?
I'm still learning, so if you see something I could do better:
Found a bug? Open an Issue
Have an idea? Start a Discussion
Want to add code? Make a Pull Request

For fellow MUBAS students:
If you're working on something similar or need help with your projects, feel free to reach out. We can learn together!

🚀 What I've Learned So Far
Building this has taught me:
Planning matters - I spent 2 days just designing the database before writing any code
Small steps win - Instead of building everything at once, I add one feature at a time
Testing saves time - Writing tests feels slow but catches bugs early
Documentation is key - If I don't write it down, I forget why I did something

📚 Challenges I Faced (And How I Solved Them)
Problem 1: Making Data Update Live
Challenge: How to show new sales without refreshing the page
Solution: Used JavaScript to fetch data every 5 minutes

Problem 2: Slow Database Queries
Challenge: Loading all sales history took 10+ seconds
Solution: Added database indexes and cached frequent queries

Problem 3: Different User Views
Challenge: Managers need full access, staff need limited view
Solution: Created role-based permissions system

🎯 My Goals for This Project
Academic: Get 85%+ in Programming III practical assessment
Portfolio: Have a complete project to show employers
Learning: Truly understand how full applications are built
Helpful: Maybe someone can actually use this for their business

👨‍💻 About Me
Name: Gomezgani Chirwa
Program: Bachelor of Management Information Systems (Year 3)
University: Malawi University of Business and Applied Sciences (MUBAS)
Focus Area: Management Information Systems
Career Goal: Building technology solutions for African businesses

📞 Contact Me:
Email: chirwagomez@gmail.com (personal)

Phone/WhatsApp: +256 880 725 061

LinkedIn: linkedin.com/in/gomezgani-chirwa-4b6286270

School: 3rd Year MIS Student at MUBAS

💬 Let's Connect!
I'm always happy to:
Chat about tech projects
Help fellow students
Learn from experienced developers
Discuss business technology in Malawi

📄 Important Notes
For Academic Purposes:
This is my original work for educational purposes at MUBAS. All code is written by me unless I specifically credit someone else in the comments.

For Business Use:
This is a learning project and might have bugs. If you want to use it for a real business, please test thoroughly first and consider getting help from an experienced developer.

License:
This project is under the MIT License - meaning you can use, modify and share it, but I'm not responsible if something goes wrong.

<div align="center">
🎓 Student by Day, Coder by Night
"The best way to learn is to build something you care about."

Last Updated: February 2026
Project Status: Actively Developing
Commitment: Daily progress updates

</div> 
```

