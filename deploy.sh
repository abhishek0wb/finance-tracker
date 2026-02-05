#!/bin/bash

# Hisaab Finance Tracker - Quick Deployment Script
# This script deploys your app to Google Cloud Run

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Hisaab Finance Tracker - Cloud Run Deployment${NC}"
echo "=================================================="

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ gcloud CLI is not installed. Please install it first.${NC}"
    exit 1
fi

# Get project configuration
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    echo -e "${RED}❌ No GCP project set. Run: gcloud config set project YOUR_PROJECT_ID${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Project ID: ${PROJECT_ID}${NC}"

# Configuration
REGION=${REGION:-"us-central1"}
SERVICE_NAME=${SERVICE_NAME:-"hisaab-finance"}
REPOSITORY=${REPOSITORY:-"hisaab-repo"}

echo -e "${YELLOW}Configuration:${NC}"
echo "  Region: $REGION"
echo "  Service: $SERVICE_NAME"
echo "  Repository: $REPOSITORY"
echo ""

# Confirm deployment
read -p "Deploy to Cloud Run? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Deployment cancelled.${NC}"
    exit 0
fi

echo -e "${GREEN}📦 Starting deployment...${NC}"

# Submit to Cloud Build
echo -e "${YELLOW}Building and deploying with Cloud Build...${NC}"
gcloud builds submit \
    --config=cloudbuild.yaml \
    --substitutions=_REGION=$REGION,_SERVICE_NAME=$SERVICE_NAME,_REPOSITORY=$REPOSITORY

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Deployment successful!${NC}"
    
    # Get service URL
    SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)" 2>/dev/null)
    
    if [ ! -z "$SERVICE_URL" ]; then
        echo -e "${GREEN}🌐 Your app is live at: ${SERVICE_URL}${NC}"
        echo ""
        echo -e "${YELLOW}Next steps:${NC}"
        echo "  1. Run migrations: See DEPLOYMENT.md for instructions"
        echo "  2. Create superuser: See DEPLOYMENT.md for instructions"
        echo "  3. Visit your app: $SERVICE_URL"
    fi
else
    echo -e "${RED}❌ Deployment failed. Check the logs above.${NC}"
    exit 1
fi
