Status monitor
==============

A web app that monitors HTTP and TCP endpoints and creates PagerDuty alerts and Slack notifications when something goes wrong.

Tech stack:

🐍 Python async **aiohttp** backend (a long running process; sorry, no serverless 🙂) \
🌈 **Next.js** frontend (statically exported HTML + JS files served by Python backend) \
🗄 **SQLite** database (or possibly other SQL database supported by Python backend SQLAlchemy layer) \
📜 simple YAML configuration file (devops/automatization friendly); the web interface is only for stats and alerts \
👤 Google OAuth
