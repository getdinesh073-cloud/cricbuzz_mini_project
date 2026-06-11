# Deployment Guide

## Deployment Options

### 1. Streamlit Community Cloud
- Push code to GitHub
- Connect repository to Streamlit Cloud
- Set environment secrets in app settings

### 2. Docker Containerization
- Create Dockerfile for containerized deployment
- Build and push to container registry
- Deploy to container orchestration platform

### 3. Platform-as-a-Service
- Deploy to Heroku, Railway, Fly.io, or Azure Web Apps
- Use Procfile for custom startup commands
- Manage environment variables via platform dashboard

## Pre-deployment Checklist

- [ ] All dependencies listed in requirements.txt
- [ ] Environment variables configured
- [ ] Database credentials secured (not in code)
- [ ] API keys stored in environment/secrets
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] README.md with clear instructions
- [ ] .gitignore properly configured
- [ ] No sensitive data in Git history

## Running in Production

```bash
# Set environment variables
export DB_HOST=production_host
export DB_USER=prod_user
export DB_PASSWORD=prod_password
export CRICBUZZ_API_KEY=your_api_key

# Start the app
streamlit run main.py --server.port=8501
```
