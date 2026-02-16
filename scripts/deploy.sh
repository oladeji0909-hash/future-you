#!/bin/bash

echo "🚀 Deploying Future You..."

# Backend deployment
echo "📦 Building backend..."
cd backend
docker build -t futureyou-backend:latest .

echo "🔄 Pushing to registry..."
docker tag futureyou-backend:latest your-registry/futureyou-backend:latest
docker push your-registry/futureyou-backend:latest

echo "✅ Backend deployed!"

# Frontend deployment
echo "📦 Building frontend..."
cd ../frontend
npm run build

echo "☁️ Deploying to S3..."
aws s3 sync build/ s3://futureyou-frontend --delete

echo "🔄 Invalidating CloudFront cache..."
aws cloudfront create-invalidation --distribution-id YOUR_DISTRIBUTION_ID --paths "/*"

echo "✅ Frontend deployed!"
echo "🎉 Deployment complete!"
