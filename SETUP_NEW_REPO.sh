#!/bin/bash
# Setup script for pushing to new GitHub repository

echo "=========================================="
echo "Setting up new GitHub repository"
echo "=========================================="
echo ""

# Check if remote already exists
if git remote | grep -q origin; then
    echo "⚠️  Remote 'origin' already exists. Removing it..."
    git remote remove origin
fi

# Prompt for new repository URL
echo "Please provide your new GitHub repository URL:"
echo "Example: https://github.com/yourusername/your-repo-name.git"
echo ""
read -p "Repository URL: " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ No repository URL provided. Exiting."
    exit 1
fi

# Add new remote
echo ""
echo "Adding remote: $REPO_URL"
git remote add origin "$REPO_URL"

# Verify remote
echo ""
echo "Current remotes:"
git remote -v

echo ""
echo "=========================================="
echo "Ready to push!"
echo "=========================================="
echo ""
echo "To push to the new repository, run:"
echo "  git push -u origin main"
echo ""
echo "Or if you want to force push (overwrites remote):"
echo "  git push -u origin main --force"
echo ""
