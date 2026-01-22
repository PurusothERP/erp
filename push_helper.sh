#!/bin/bash
echo "--------------------------------------------------------"
echo "GitHub Push Helper"
echo "--------------------------------------------------------"
echo "This script will help you push your code to GitHub."
echo "Note: GitHub does NOT accept your account password."
echo "You must use a Personal Access Token (PAT)."
echo ""

# Get Username
read -p "Enter your GitHub Username (e.g., NilanRitvik): " USERNAME

# Get Token
echo "Enter your GitHub Personal Access Token (starts with ghp_...):"
read -s TOKEN
echo "Token captured."
echo ""

if [ -z "$TOKEN" ]; then
    echo "Error: Token cannot be empty."
    exit 1
fi

# Construct URL
REPO="eprnext.git"
REMOTE_URL="https://$USERNAME:$TOKEN@github.com/$USERNAME/$REPO"

echo "Pushing to $USERNAME/$REPO..."

# Push
git push --repo "$REMOTE_URL" user_origin HEAD:main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Success! Code pushed to GitHub."
else
    echo ""
    echo "❌ Failed to push. Please check your Token and permissions."
    echo "Make sure your Token has 'repo' permissions."
fi
