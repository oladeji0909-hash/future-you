# Deployment & Update Guide

## 🚀 Continuous Deployment Setup

### How It Works
Every time you push code to the `main` branch, the app automatically:
1. Runs tests
2. Builds new Docker images
3. Deploys backend to AWS ECS
4. Deploys frontend to S3/CloudFront
5. Goes live in ~5 minutes

### Making Updates After Launch

#### Option 1: Automatic (Recommended)
```bash
# Make your changes
git add .
git commit -m "Add new feature"
git push origin main

# GitHub Actions automatically deploys
# Check progress at: github.com/your-repo/actions
```

#### Option 2: Manual Deploy
```bash
# Run deployment script
./scripts/deploy.sh

# Or deploy individually:
# Backend only
cd backend
docker build -t futureyou-backend .
docker push your-registry/futureyou-backend

# Frontend only
cd frontend
npm run build
aws s3 sync build/ s3://futureyou-frontend --delete
```

#### Option 3: Rollback
```bash
# Rollback to previous version
aws ecs update-service --cluster futureyou-cluster \
  --service futureyou-backend \
  --task-definition futureyou-backend:PREVIOUS_VERSION

# Or use GitHub Actions to redeploy specific commit
```

## 🔧 Infrastructure Management

### Initial Setup
```bash
# 1. Install Terraform
# 2. Configure AWS credentials
aws configure

# 3. Initialize Terraform
cd terraform
terraform init

# 4. Deploy infrastructure
terraform apply

# 5. Note outputs (CloudFront domain, etc.)
```

### Update Infrastructure
```bash
cd terraform
terraform plan    # Preview changes
terraform apply   # Apply changes
```

### Database Migrations
```bash
# Run migrations on deployed database
cd backend
alembic upgrade head

# Or via ECS task
aws ecs run-task --cluster futureyou-cluster \
  --task-definition migration-task \
  --launch-type FARGATE
```

## 📊 Monitoring Updates

### Check Deployment Status
```bash
# Backend health
curl https://api.futureyou.app/health

# Frontend status
curl https://futureyou.app

# ECS service status
aws ecs describe-services --cluster futureyou-cluster \
  --services futureyou-backend
```

### View Logs
```bash
# Backend logs
aws logs tail /ecs/futureyou-backend --follow

# Or use CloudWatch console
```

## 🔄 Update Workflow

### Feature Updates
1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes and test locally
3. Push and create Pull Request
4. Merge to main → Auto-deploys

### Hotfix Updates
1. Create hotfix branch: `git checkout -b hotfix/critical-fix`
2. Make fix
3. Push directly to main (emergency) or PR
4. Auto-deploys in minutes

### Database Schema Changes
1. Create migration: `alembic revision -m "add new column"`
2. Test locally
3. Push to main
4. Migration runs automatically on deploy

## 🛡️ Zero-Downtime Deployment

The setup ensures:
- **Rolling updates**: New version deploys while old runs
- **Health checks**: Only switches when new version is healthy
- **Automatic rollback**: Reverts if health checks fail
- **Blue-green deployment**: Can enable for critical updates

## 🔐 Environment Variables

### Update Production Secrets
```bash
# Via AWS Systems Manager Parameter Store
aws ssm put-parameter --name /futureyou/prod/SECRET_KEY \
  --value "new-secret" --type SecureString --overwrite

# Or update in ECS task definition
# Then redeploy service
```

## 📱 Mobile App Updates

### iOS
```bash
cd mobile/ios
fastlane release
# Uploads to App Store Connect
# Submit for review
```

### Android
```bash
cd mobile/android
fastlane release
# Uploads to Google Play Console
# Rolls out gradually
```

## 🧪 Testing Before Deploy

### Local Testing
```bash
docker-compose up
# Test at localhost:3000
```

### Staging Environment
```bash
# Deploy to staging first
git push origin staging
# Test at staging.futureyou.app
# Then merge to main
```

## 📈 Scaling Updates

### Increase Capacity
```bash
# Scale backend
aws ecs update-service --cluster futureyou-cluster \
  --service futureyou-backend --desired-count 5

# Or update in Terraform
# desired_count = 5
terraform apply
```

### Database Scaling
```bash
# Upgrade RDS instance
aws rds modify-db-instance --db-instance-identifier futureyou-db \
  --db-instance-class db.t3.medium --apply-immediately
```

## 🚨 Emergency Procedures

### Rollback Deployment
```bash
# Quick rollback
aws ecs update-service --cluster futureyou-cluster \
  --service futureyou-backend --force-new-deployment \
  --task-definition futureyou-backend:PREVIOUS_REVISION
```

### Disable Feature Flag
```bash
# Update feature flag in database
# Or environment variable
aws ssm put-parameter --name /futureyou/prod/FEATURE_X_ENABLED \
  --value "false" --overwrite
```

### Take Site Offline (Maintenance)
```bash
# Upload maintenance page to S3
aws s3 cp maintenance.html s3://futureyou-frontend/index.html
aws cloudfront create-invalidation --distribution-id XXX --paths "/*"
```

## 📝 Update Checklist

Before each deployment:
- [ ] Tests pass locally
- [ ] Database migrations tested
- [ ] Environment variables updated
- [ ] Changelog updated
- [ ] Monitoring alerts configured
- [ ] Rollback plan ready

## 🎯 Best Practices

1. **Small, frequent updates** - Deploy multiple times per day
2. **Feature flags** - Toggle features without redeploying
3. **Canary releases** - Test with 5% of users first
4. **Monitor metrics** - Watch error rates after deploy
5. **Communicate** - Notify users of major updates

## 🔗 Useful Commands

```bash
# Check what's deployed
git log origin/main -1

# Compare local vs deployed
git diff origin/main

# View deployment history
aws ecs describe-task-definition --task-definition futureyou-backend

# Force immediate deployment
git commit --allow-empty -m "Trigger deploy"
git push origin main
```

---

**You can update the live app anytime by simply pushing to GitHub!** 🚀
