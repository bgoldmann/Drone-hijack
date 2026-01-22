#!/bin/bash
# Script to push fresh repository to GitHub

echo "=========================================="
echo "Push Fresh Repository to GitHub"
echo "=========================================="
echo ""

# Check if repository URL is provided as argument
if [ -z "$1" ]; then
    echo "Usage: ./PUSH_TO_GITHUB.sh <repository-url>"
    echo ""
    echo "Example:"
    echo "  ./PUSH_TO_GITHUB.sh https://github.com/bgoldmann/Drone-hijack.git"
    echo ""
    echo "Or create a new repository on GitHub first, then run:"
    echo "  1. Create new repository on GitHub (empty, no README)"
    echo "  2. Copy the repository URL"
    echo "  3. Run: ./PUSH_TO_GITHUB.sh <your-repo-url>"
    exit 1
fi

REPO_URL="$1"

# Remove existing remote if it exists
if git remote | grep -q origin; then
    echo "Removing existing remote..."
    git remote remove origin
fi

# Add new remote
echo "Adding remote: $REPO_URL"
git remote add origin "$REPO_URL"

# Verify remote
echo ""
echo "Current remotes:"
git remote -v

echo ""
echo "=========================================="
echo "Pushing to GitHub..."
echo "=========================================="
echo ""

# Push to GitHub (force push to overwrite if needed)
echo "Pushing main branch..."
git push -u origin main --force

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "Repository URL: $REPO_URL"
    echo "Branch: main"
    echo ""
else
    echo ""
    echo "❌ Push failed. Please check:"
    echo "  1. Repository URL is correct"
    echo "  2. You have push access to the repository"
    echo "  3. Repository exists on GitHub"
    echo ""
    exit 1
fi
