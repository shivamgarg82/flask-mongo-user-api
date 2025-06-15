# User Management API with Flask & MongoDB

![Python](https://img.shields.io/badge/python-3.9+-blue?style=flat-square)
![Flask](https://img.shields.io/badge/flask-2.0.*-lightgrey?style=flat-square)
![MongoDB](https://img.shields.io/badge/mongodb-5.0+-green?style=flat-square) 

A simple API for managing users that I built while learning Flask and MongoDB. It's not perfect, but it works!
 
## Why I Built This

I wanted to understand:
- How to use MongoDB with Flask (it's different from SQL!)
- Proper REST API design
- Docker containerization 

## Features (That Actually Work)

✔️ Basic CRUD operations for users  
✔️ Password hashing (thanks to some StackOverflow help)  
✔️ Docker setup (after 3 tries)  
✔️ Error handling for most cases  

## Known Issues (Be Warned)

⚠️ **Email validation is weak** - just checks for "@"  
⚠️ **No tests yet** - I'm still learning pytest  
⚠️ **First request is slow** - MongoDB takes a sec to wake up  

## Installation

### Prerequisites
- Docker (I used version 20.10)
- Docker-compose

### Quick Start
1. Clone this repo (if you haven't)
   ```bash
   git clone https://github.com/yourusername/flask-mongo-crud.git
Run it:

bash
cd flask-mongo-crud
docker-compose up --build
(This might take a while the first time)

API Endpoints
Endpoint	Method	What It Does
/users	POST	Create new user
/users	GET	List all users
/users/<id>	GET	Get one user
/users/<id>	PUT	Update user
/users/<id>	DELETE	Remove user
Example request:

bash
curl -X POST http://localhost:5000/users -H "Content-Type: application/json" -d '{"name":"Bob","email":"bob@test.com","password":"123"}'
Lessons Learned
MongoDB is different:

No schema is cool but weird

ObjectId confused me at first

Docker networking:

Spent hours figuring out why Flask couldn't talk to MongoDB

Solution: Needed depends_on AND wait-for-it.sh

Password security:

First version stored plain text passwords (yikes!)

Fixed with bcrypt after reading about hashing

What's Next?
If I had more time:

Add proper email validation

Write actual tests

Implement JWT auth

Maybe add user profiles?

Screenshots
https://postman-screenshot.png (I can add real screenshots later)

License
MIT - Do whatever you want with this, but maybe don't use it in production yet!
