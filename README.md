# DevQuery: AI-Powered Q&A Platform for Developers

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![AI Integration](https://img.shields.io/badge/AI-Integrated-4285F4?style=for-the-badge&logo=artificial-intelligence&logoColor=white)

## Overview

DevQuery is a Stack Overflow-like platform designed for the developer community, enhanced with AI capabilities. It allows users to ask questions, receive AI-generated answers, and interact with a community of developers. The platform features automatic tagging, question analysis, and summarization powered by AI.

## Features

- User registration and authentication
- Ask and answer questions
- AI-generated answers and tag suggestions
- Question analysis and summarization
- User profiles and reputation system
- Admin dashboard and moderator panel
- Modern, responsive design

## Technology Stack

- **Backend**: Python, Flask
- **Database**: SQLAlchemy ORM
- **Frontend**: HTML, CSS, JavaScript
- **AI Integration**: Custom AI helper (details in `utils/ai_helper.py`)

## Key Components

### Models
- `User`: User information and authentication
- `Question`: Represents questions asked by users
- `Answer`: Stores answers to questions
- `Tag`: Manages tags for questions
- `Vote`: Handles voting on questions and answers

### Routes
- User authentication (register, login, logout)
- Question and answer management
- Admin and moderator functionalities
- Main page and search results

### Utils
- `ai_helper.py`: AI integration for answer generation, tagging, and analysis
- `decorators.py`: Custom decorators for route protection

## Usage

1. Register for an account or log in
2. Ask questions or browse existing ones
3. Answer questions or view AI-generated answers
4. Use the search functionality to find specific topics
5. Gain reputation by receiving upvotes on your questions and answers
6. Admins and moderators can access additional features through their respective panels

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.