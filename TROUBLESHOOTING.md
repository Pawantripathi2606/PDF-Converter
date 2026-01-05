# Render Deployment - Troubleshooting Guide

## Issue: Pillow Build Error (FIXED ✅)

### Error Message
```
KeyError: '__version__'
Getting requirements to build wheel did not run successfully.
```

### Root Cause
- **Pillow 10.1.0** is incompatible with **Python 3.13.4**
- Render was using Python 3.13.4 by default

### Solution Applied ✅

1. **Updated Pillow version**
   - Changed from `Pillow==10.1.0` to `Pillow==10.4.0`
   - Version 10.4.0 supports Python 3.13

2. **Specified Python version**
   - Created `runtime.txt` with `python-3.11.0`
   - This ensures consistent Python version across deployments

### Files Changed
- ✅ `requirements.txt` - Updated Pillow to 10.4.0
- ✅ `runtime.txt` - Added Python 3.11.0 specification

---

## Next Steps for Deployment

The fix has been pushed to GitHub. Render will automatically redeploy with the updated configuration.

### What Render Will Do:
1. ✅ Use Python 3.11.0 (from `runtime.txt`)
2. ✅ Install Pillow 10.4.0 (compatible version)
3. ✅ Build successfully
4. ✅ Start the app with Gunicorn

### Monitor Deployment:
- Go to your Render dashboard
- Check the **Logs** tab
- Look for: `==> Build successful 🎉`

---

## Expected Build Output (Success)

```
==> Installing Python version 3.11.0...
==> Using Python version 3.11.0
==> Running build command 'pip install -r requirements.txt'...
Collecting Flask==3.0.0
Collecting Werkzeug==3.0.1
Collecting PyPDF2==3.0.1
Collecting Pillow==10.4.0
Collecting img2pdf==0.5.1
Collecting gunicorn==21.2.0
Successfully installed Flask-3.0.0 Werkzeug-3.0.1 PyPDF2-3.0.1 Pillow-10.4.0 img2pdf-0.5.1 gunicorn-21.2.0
==> Build successful 🎉
```

---

## Common Render Issues & Solutions

### Issue 1: Build Timeout
**Solution**: Increase build timeout in Render settings (usually not needed for this app)

### Issue 2: Port Binding Error
**Solution**: Already handled in `gunicorn_config.py` - uses `PORT` environment variable

### Issue 3: File Upload Fails
**Possible Causes**:
- File too large (max 50MB configured)
- Disk space limit on free tier
**Solution**: Consider upgrading to paid tier or using cloud storage

### Issue 4: App Crashes on Startup
**Check**:
- Render logs for error messages
- Ensure all dependencies are in `requirements.txt`
- Verify Gunicorn configuration

---

## Deployment Checklist

- [x] Updated Pillow to compatible version
- [x] Created runtime.txt for Python version
- [x] Added Gunicorn to requirements
- [x] Created gunicorn_config.py
- [x] Pushed to GitHub
- [ ] Monitor Render deployment logs
- [ ] Test all features after deployment
- [ ] Verify file uploads work

---

## Testing After Deployment

Once deployed, test these features:

1. **Image to PDF Conversion**
   - Upload a JPG/PNG
   - Verify PDF downloads

2. **PDF Splitting**
   - Upload multi-page PDF
   - Verify ZIP with all pages downloads

3. **PDF Merging**
   - Upload two PDFs
   - Verify merged PDF downloads

---

## Support Resources

- **Render Docs**: https://render.com/docs
- **Render Status**: https://status.render.com
- **Community Forum**: https://community.render.com

---

## Version History

- **v1.0** - Initial Tkinter desktop app
- **v2.0** - Flask web app migration
- **v2.1** - Render deployment fixes (Pillow compatibility)
