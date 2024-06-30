#!/bin/bash
# Change to the home directory
cd ~
# Change to the project directory
cd /home/neguete/Documents/Cocktail-Machine/
# Add a delay to ensure network is up (optional)
sleep 10
# Log the date and time the script is run
echo "Running startup script at $(date)" >> /home/neguete/Documents/Cocktail-Machine/startup.log
# Attempt to pull the latest changes from the repository
git pull >> /home/neguete/Documents/Cocktail-Machine/startup.log 2>&1
# Check the status of the git pull command
if [ $? -ne 0 ]; then
  echo "Git pull failed at $(date)" >> /home/neguete/Documents/Cocktail-Machine/startup.log
else
  echo "Git pull succeeded at $(date)" >> /home/neguete/Documents/Cocktail-Machine/startup.log
fi
# Start backend.py
echo "Starting backend.py at $(date)" >> /home/neguete/Documents/Cocktail-Machine/startup.log
python3 backend.py >> /home/neguete/Documents/Cocktail-Machine/startup.log 2>&1 &
if [ $? -ne 0 ]; then
  echo "backend.py failed to start at $(date)" >> /home/neguete/Documents/Cocktail-Machine/startup.log
else
  echo "backend.py started successfully at $(date)" >> /home/neguete/Documents/Cocktail-Machine/startup.log
fi
# Start the application in the background
echo "Starting npm application at $(date)" >> /home/neguete/Documents/Cocktail-Machine/startup.log
npm start >> /home/neguete/Documents/Cocktail-Machine/startup.log 2>&1 
if [ $? -ne 0 ]; then
  echo "npm start failed at $(date)" >> /home/neguete/Documents/Cocktail-Machine/startup.log
else
  echo "npm start succeeded at $(date)" >> /home/neguete/Documents/Cocktail-Machine/startup.log
fi