# Deployment Guide - Render

## Quick Deploy to Render

### Option 1: Using Render Dashboard (Recommended)

1. **Sign up/Login** to [Render](https://render.com)

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `https://github.com/Pawantripathi2606/PDF-Converter`

3. **Configure Service**
   - **Name**: `pdf-converter-pro` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --config gunicorn_config.py app:app`
   - **Instance Type**: Free (or paid for better performance)

4. **Deploy**
   - Click "Create Web Service"
   - Render will automatically deploy your app
   - You'll get a URL like: `https://pdf-converter-pro.onrender.com`

---

### Option 2: Using render.yaml Blueprint

1. Push the `render.yaml` file to your repository
2. In Render Dashboard, click "New +" → "Blueprint"
3. Select your repository
4. Render will auto-configure based on `render.yaml`

---

## Environment Variables (Optional)

If you need to configure any environment variables:

| Variable | Value | Description |
|----------|-------|-------------|
| `PYTHON_VERSION` | `3.11.0` | Python version to use |
| `PORT` | Auto-set by Render | Port for the application |

---

## Important Notes

### File Upload Limits
- Render's free tier has limited disk space
- Consider using cloud storage (AWS S3, Cloudinary) for production
- Current max file size: 50MB (configured in `app.py`)

### Temporary Files
- The app auto-cleans files older than 1 hour
- Render's ephemeral filesystem means files don't persist between deploys
- This is fine for temporary PDF processing

### Performance
- **Free Tier**: Spins down after 15 minutes of inactivity (cold starts)
- **Paid Tier**: Always running, faster response times

---

## Post-Deployment

After deployment, test all features:
1. ✅ Image to PDF conversion
2. ✅ PDF splitting
3. ✅ PDF merging

---

## Troubleshooting

### Build Fails
- Check that `requirements.txt` is in the root directory
- Verify Python version compatibility

### App Crashes
- Check Render logs in the dashboard
- Ensure all dependencies are installed
- Verify Gunicorn is starting correctly

### File Upload Issues
- Check file size limits
- Verify upload folder permissions
- Review Render's disk space limits

---

## Monitoring

Access logs in Render Dashboard:
- **Logs** tab shows real-time application logs
- **Metrics** tab shows performance data
- **Events** tab shows deployment history

---

## Updating Your App

To deploy updates:
1. Push changes to GitHub
2. Render auto-deploys from the `main` branch
3. Or manually trigger deploy in Render Dashboard

---

## Cost

- **Free Tier**: $0/month (with limitations)
- **Starter**: $7/month (always running, better performance)
- **Standard**: $25/month (more resources)

For this PDF converter, the **Free tier** is sufficient for testing and light usage.
