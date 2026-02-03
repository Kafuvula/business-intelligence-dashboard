🏢 Business Intelligence Dashboard
<div align="center">
https://img.shields.io/badge/python-3.9+-blue.svg
https://img.shields.io/badge/flask-2.3.x-green.svg
https://img.shields.io/badge/MySQL-8.0-orange
https://img.shields.io/badge/license-MIT-blue.svg
https://img.shields.io/badge/MUBAS-3rd_Year_MIS-purple
https://img.shields.io/badge/status-in_development-yellow

From Manual Records to Smart Insights — Built for Malawi's Businesses

</div>
📖 What's This About?
Hello! I'm Gomezgani Chirwa, a 3rd-year Management Information Systems (MIS) student at MUBAS. This dashboard is my main project for the Programming III module (CIS-PRO-313), but it's really about something bigger.

While talking to small shop owners in my community, I kept hearing the same frustration: "I know the money is moving, but I can't see where it's going." They were drowning in paper receipts, struggling with mental inventory counts, and making crucial decisions based on guesswork. As someone training to bridge business and technology, that felt like a problem waiting for a solution.

So, I decided to build one. This isn't just another coding exercise for a grade. It's my attempt to apply what I'm learning in class to a real challenge faced by Malawian businesses. Can a simple, clear dashboard replace a messy spreadsheet and give an owner back control? I'm building this to find out.

🎓 The MIS Lens: Connecting My Studies to Real Problems
This project is where theory from all my modules meets practice. It's my playground for figuring out how the pieces fit together to solve a business problem.

Subject	What I'm Applying Here	The "Why" Behind It
Programming III	Building the app with Python & Flask	To create a tangible tool from code, focusing on clean, maintainable structure.
Database Admin	Designing the MySQL schema & planning backups	Because reliable, fast data storage is the backbone of any business system.
Financial Accounting	Structuring sales, expense, and profit tracking	To ensure the numbers reflect real business logic and help with financial decisions.
Computer Graphics	Designing charts and data visualizations	Turning raw database numbers into insights you can understand at a glance.
Operating Systems	Considering deployment and performance	So the app runs smoothly for a user, not just on my laptop.
Research Methods	Documenting the process and planning user tests	To build methodically and create something others can learn from or improve.
✨ What Can This Dashboard Do?
For a Business Owner:
See your sales as they happen – No more waiting until month-end to know where you stand.

Never run out of stock unexpectedly – Get a clear warning when popular items are getting low.

Understand who your customers are – See buying patterns to know what's working.

Track cash flow in one place – Connect daily sales to expenses and see actual profit.

Under the Hood (What I'm Building):
A secure starting point – Different logins for managers and staff to protect data.

Always-current information – The dashboard updates quietly in the background.

Reports you can use – Export PDF summaries for bank meetings or planning.

Built for local context – Designed to work reliably with typical internet and devices.

📸 See It in Action
(Working on getting the first version live! Screenshots will go here as soon as the main dashboard is presentable.)

Planned Dashboard View:
[ Final Sales Chart ] | [ Live Inventory Status ] | [ Recent Customer Activity ]

Mobile-Friendly View:
[ Phone Preview ]

🛠️ How to Set It Up (For Developers & The Curious)
Want to run this locally to test it or see how it works? Here's how:

What You'll Need:
Python 3.9 or newer

A MySQL server (like XAMPP or a standalone install)

Git (to download the project)

Step-by-Step Installation:
bash
# 1. Clone the repository to your machine
git clone https://github.com/kafuvula/business-intelligence-dashboard.git
cd business-intelligence-dashboard

# 2. Install the required Python libraries
pip install -r requirements.txt

# 3. Set up the database (you'll be prompted for your MySQL password)
mysql -u root -p < database/setup.sql

# 4. Start the Flask application
python run.py

# 5. Open your browser and go to:
# http://localhost:5000
Default Login (for testing only – change these in a real deployment!):

Manager: admin@test.com / password123

Staff: staff@test.com / password123

📁 Project Structure
text
business-intelligence-dashboard/
├── app/                    # The heart of the Flask application
│   ├── __init__.py        # Initializes the app and brings everything together
│   ├── routes.py          # Defines all the website pages (URLs)
│   ├── models.py          # Blueprint for all the database tables
│   ├── auth.py            # Handles user login, registration, and security
│   └── utils.py           # Helper functions for calculations and data processing
├── templates/             # HTML files that define what each page looks like
│   ├── dashboard.html     # The main business overview page
│   ├── login.html         # The login screen
│   └── reports.html       # The reporting interface
├── static/                # Files that make the site look and feel good
│   ├── css/               # Stylesheets (colors, layout)
│   ├── js/                # JavaScript for interactive charts and updates
│   └── images/            # Logos, icons, etc.
├── database/              # Everything related to the database
│   ├── setup.sql          # Script to create all the tables from scratch
│   └── sampledata.sql     # Example data to populate the database for testing
├── tests/                 # Scripts to automatically test parts of the app
│   ├── test_auth.py
│   └── test_dashboard.py
├── requirements.txt       # List of all Python packages the project needs
├── config.py             # Settings (database connections, secret keys)
├── run.py                # The script to launch the application
└── README.md             # This file you're reading!
🔧 Current Focus & What's Next
This Week's Goal: Get the core engine running.

✅ Initialize the Flask application structure.

✅ Design and create the core database tables.

🔲 Build the main dashboard layout (HTML/CSS).

🔲 Integrate the first live chart (Sales Trend).

🔲 Complete the user login and authentication system.

🔲 Write basic tests for the login and dashboard features.

On the Horizon (If Time Allows):

Automated email alerts for low stock levels.

Basic customer loyalty tracking.

Better expense categorization.

Support for tracking multiple business locations.

🤝 Want to Help or Learn?
I'm building this in public as a learning journey. If you're a fellow student, developer, or just curious:

Found a bug? Open a GitHub Issue.

Have an idea for a feature? Start a Discussion!

Want to contribute code? Pull Requests are very welcome.

Especially for my MUBAS peers: If you're working on a similar project or stuck on a Flask/MySQL concept, feel free to reach out. Maybe we can figure it out together.

🚀 Lessons from the Trenches
This process has already taught me more than any single lecture:

Planning is not optional. I spent two full days just sketching database tables and user flows before writing a single line of code. It saved me countless hours later.

Small, steady wins beat grand plans. The goal of "build a full dashboard" was paralyzing. The goal of "make the login page work today" was achievable and motivating.

Your future self will thank you for notes. Why did I structure that query a certain way? Without comments and documentation, I'd have to re-solve the same puzzle.

📚 Real Challenges I'm Tackling
Problem: How to show live data without requiring a page refresh (which feels clunky).
My Approach: Using JavaScript to quietly fetch new data from the server every few minutes and update only the parts of the screen that need to change.

Problem: The database got slow when I tried to load a full year of sales for a chart.
My Approach: I learned about database indexing (like a book's index) and caching (temporarily storing frequent results) to speed things up dramatically.

Problem: A manager needs to see everything, but a staff member should only see sales data.
My Approach: Building a role-based permissions system from the start that checks who is logged in and tailors what they can see and do.

🎯 My Goals for This Project
Academic: Demonstrate a deep, practical understanding of full-stack development for my Programming III (CIS-PRO-313) assessment.

Portfolio: Create a substantial, working project that I can show to potential employers or clients as proof of my skills.

Learning: Move from understanding concepts in isolation to knowing how to architect and deploy a complete, integrated system.

Impact: Create a tool that is genuinely useful. If even one small business owner finds it helpful, I'll consider that a huge success.

👨‍💻 About Me
Name: Gomezgani Chirwa
Program: Bachelor of Management Information Systems (Year 3)
University: Malawi University of Business and Applied Sciences (MUBAS)
Focus: I'm passionate about the space where business strategy meets practical technology—figuring out what tools a business actually needs and then building them.
Career Goal: To design and implement information systems that solve real, everyday challenges for businesses and organizations across Africa.

📬 Get in Touch:

Email: chirwagomez@gmail.com

Phone/WhatsApp: +256 880 725 061

LinkedIn: linkedin.com/in/gomezgani-chirwa-4b6286270

💬 Let's Talk! I'm always up for:

Chatting about tech projects, big or small.

Helping fellow students puzzle through a problem.

Learning from developers who've walked this path before.

Discussing the future of business technology in Malawi and beyond.

📄 Important Notes
For Academic Purposes:
This is my original work created for my studies at MUBAS. All code has been written by me, with learning resources and tutorials credited where applicable.

For Business Use:
Please remember this is a student learning project. It might have bugs or unfinished parts. If you're considering using it for a real business, please test it thoroughly and consult with an experienced developer first.

License:
This project is licensed under the MIT License. This means you are free to use, copy, modify, and distribute the software, but I am not liable for any outcomes from its use.

<div align="center">
🎓 Student by Day, Builder by Night
"The best way to learn is to build something that matters to you."

Last Updated: February 2026
Project Status: Actively in Development
Commitment: Making steady, daily progress

</div>