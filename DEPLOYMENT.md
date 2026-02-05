# Hisaab Finance Tracker - Google Cloud Run Deployment Guide

## Prerequisites

1. **Google Cloud Account** with billing enabled
2. **gcloud CLI** installed and configured
3. **Docker** installed locally (for testing)
4. **Project ID** from Google Cloud Console

## Initial Setup

### 1. Set up Google Cloud Project

```bash
# Set your project ID
export PROJECT_ID="your-project-id"
export REGION="us-central1"
export SERVICE_NAME="hisaab-finance"

# Set the project
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    sqladmin.googleapis.com \
    secretmanager.googleapis.com \
    artifactregistry.googleapis.com
```

### 2. Create Artifact Registry Repository

```bash
# Create repository for Docker images
gcloud artifacts repositories create hisaab-repo \
    --repository-format=docker \
    --location=$REGION \
    --description="Hisaab Finance Tracker Docker images"

# Configure Docker authentication
gcloud auth configure-docker ${REGION}-docker.pkg.dev
```

### 3. Set up Cloud SQL PostgreSQL Database

```bash
# Create Cloud SQL instance
gcloud sql instances create hisaab-db \
    --database-version=POSTGRES_15 \
    --tier=db-f1-micro \
    --region=$REGION \
    --root-password=CHANGE_THIS_PASSWORD \
    --storage-type=SSD \
    --storage-size=10GB \
    --backup \
    --backup-start-time=03:00

# Create database
gcloud sql databases create finance_tracker \
    --instance=hisaab-db

# Create database user
gcloud sql users create finance_user \
    --instance=hisaab-db \
    --password=CHANGE_THIS_PASSWORD

# Get connection name
gcloud sql instances describe hisaab-db --format="value(connectionName)"
# Save this as: PROJECT_ID:REGION:hisaab-db
```

### 4. Create Secret Manager Secrets

```bash
# Django Secret Key (generate a new one)
echo -n "your-super-secret-django-key-here" | \
    gcloud secrets create django-secret-key --data-file=-

# Database credentials
echo -n "finance_tracker" | \
    gcloud secrets create postgres-db --data-file=-

echo -n "finance_user" | \
    gcloud secrets create postgres-user --data-file=-

echo -n "YOUR_DB_PASSWORD" | \
    gcloud secrets create postgres-password --data-file=-

echo -n "/cloudsql/PROJECT_ID:REGION:hisaab-db" | \
    gcloud secrets create postgres-host --data-file=-

echo -n "5432" | \
    gcloud secrets create postgres-port --data-file=-

# Grant Cloud Run access to secrets
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")

gcloud secrets add-iam-policy-binding django-secret-key \
    --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding postgres-db \
    --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding postgres-user \
    --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding postgres-password \
    --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding postgres-host \
    --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding postgres-port \
    --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"
```

## Deployment

### Option 1: Deploy using Cloud Build (Recommended)

```bash
# Submit build to Cloud Build
gcloud builds submit \
    --config=cloudbuild.yaml \
    --substitutions=_REGION=$REGION,_SERVICE_NAME=$SERVICE_NAME
```

### Option 2: Manual Deployment

```bash
# Build Docker image locally
docker build -t ${REGION}-docker.pkg.dev/${PROJECT_ID}/hisaab-repo/${SERVICE_NAME}:latest .

# Push to Artifact Registry
docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/hisaab-repo/${SERVICE_NAME}:latest

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
    --image=${REGION}-docker.pkg.dev/${PROJECT_ID}/hisaab-repo/${SERVICE_NAME}:latest \
    --region=$REGION \
    --platform=managed \
    --allow-unauthenticated \
    --set-env-vars=USE_DOCKER=True,DEBUG=False \
    --set-secrets=SECRET_KEY=django-secret-key:latest,POSTGRES_DB=postgres-db:latest,POSTGRES_USER=postgres-user:latest,POSTGRES_PASSWORD=postgres-password:latest,POSTGRES_HOST=postgres-host:latest,POSTGRES_PORT=postgres-port:latest \
    --add-cloudsql-instances=${PROJECT_ID}:${REGION}:hisaab-db \
    --max-instances=10 \
    --min-instances=0 \
    --memory=512Mi \
    --cpu=1 \
    --timeout=300
```

## Post-Deployment

### 1. Run Database Migrations

```bash
# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")

# Connect to Cloud SQL and run migrations
gcloud run jobs create migrate-db \
    --image=${REGION}-docker.pkg.dev/${PROJECT_ID}/hisaab-repo/${SERVICE_NAME}:latest \
    --region=$REGION \
    --set-secrets=SECRET_KEY=django-secret-key:latest,POSTGRES_DB=postgres-db:latest,POSTGRES_USER=postgres-user:latest,POSTGRES_PASSWORD=postgres-password:latest,POSTGRES_HOST=postgres-host:latest,POSTGRES_PORT=postgres-port:latest \
    --add-cloudsql-instances=${PROJECT_ID}:${REGION}:hisaab-db \
    --command=python \
    --args="manage.py,migrate"

# Execute the migration job
gcloud run jobs execute migrate-db --region=$REGION
```

### 2. Create Superuser

```bash
# Create a one-time job to create superuser
gcloud run jobs create create-superuser \
    --image=${REGION}-docker.pkg.dev/${PROJECT_ID}/hisaab-repo/${SERVICE_NAME}:latest \
    --region=$REGION \
    --set-secrets=SECRET_KEY=django-secret-key:latest,POSTGRES_DB=postgres-db:latest,POSTGRES_USER=postgres-user:latest,POSTGRES_PASSWORD=postgres-password:latest,POSTGRES_HOST=postgres-host:latest,POSTGRES_PORT=postgres-port:latest \
    --add-cloudsql-instances=${PROJECT_ID}:${REGION}:hisaab-db \
    --command=python \
    --args="manage.py,createsuperuser,--noinput,--username=admin,--email=admin@example.com"

# Execute
gcloud run jobs execute create-superuser --region=$REGION
```

### 3. Access Your Application

```bash
# Get the service URL
gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)"
```

## Continuous Deployment with GitHub

### Set up Cloud Build Trigger

```bash
# Connect your GitHub repository
gcloud builds triggers create github \
    --name="hisaab-deploy" \
    --repo-name="your-repo-name" \
    --repo-owner="your-github-username" \
    --branch-pattern="^main$" \
    --build-config="cloudbuild.yaml" \
    --substitutions=_REGION=$REGION,_SERVICE_NAME=$SERVICE_NAME
```

Now every push to the `main` branch will automatically deploy to Cloud Run!

## Monitoring and Logs

```bash
# View logs
gcloud run services logs read $SERVICE_NAME --region=$REGION --limit=50

# Follow logs in real-time
gcloud run services logs tail $SERVICE_NAME --region=$REGION

# View metrics in Cloud Console
echo "https://console.cloud.google.com/run/detail/${REGION}/${SERVICE_NAME}/metrics?project=${PROJECT_ID}"
```

## Cost Optimization

1. **Set min-instances to 0** - Only pay when app is used
2. **Use db-f1-micro** - Smallest Cloud SQL instance
3. **Enable request-based scaling** - Automatically scale down
4. **Set up budget alerts** - Monitor spending

## Troubleshooting

### Check service status
```bash
gcloud run services describe $SERVICE_NAME --region=$REGION
```

### Test database connection
```bash
gcloud sql connect hisaab-db --user=finance_user
```

### View build history
```bash
gcloud builds list --limit=10
```

### Update environment variables
```bash
gcloud run services update $SERVICE_NAME \
    --region=$REGION \
    --set-env-vars=NEW_VAR=value
```

## Security Best Practices

1. ✅ Use Secret Manager for sensitive data
2. ✅ Enable HTTPS only (Cloud Run default)
3. ✅ Use IAM for access control
4. ✅ Enable Cloud Armor for DDoS protection
5. ✅ Regular security updates
6. ✅ Monitor with Cloud Logging

## Backup Strategy

```bash
# Automated backups are enabled by default
# Manual backup
gcloud sql backups create --instance=hisaab-db

# List backups
gcloud sql backups list --instance=hisaab-db

# Restore from backup
gcloud sql backups restore BACKUP_ID --backup-instance=hisaab-db
```

## Scaling Configuration

```bash
# Update scaling settings
gcloud run services update $SERVICE_NAME \
    --region=$REGION \
    --min-instances=1 \
    --max-instances=100 \
    --concurrency=80 \
    --cpu=2 \
    --memory=1Gi
```

## Custom Domain Setup

```bash
# Map custom domain
gcloud run domain-mappings create \
    --service=$SERVICE_NAME \
    --domain=yourdomain.com \
    --region=$REGION
```

## Support

For issues or questions:
- Check Cloud Run logs
- Review Cloud Build history
- Consult Google Cloud documentation
- Check Django logs in Cloud Logging
