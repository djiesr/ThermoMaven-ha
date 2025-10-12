# 📦 Release Instructions for v1.1.0

## ✅ Pre-Release Checklist

- [x] All code changes committed
- [x] Version updated to 1.1.0 in `manifest.json`
- [x] CHANGELOG.md updated
- [x] Release notes created (RELEASE_NOTES_1.1.0.md)
- [x] Documentation updated (README.md, etc.)
- [x] Icon added (icon.png)
- [x] All tests passing
- [x] Integration tested with real device

## 🚀 Release Steps

### 1. Commit All Changes

```bash
cd g:\Programmes\ThermoMaven\github
git add .
git commit -m "Release v1.1.0 - Real-Time MQTT Integration

- Add real-time MQTT updates (~10 seconds)
- Add dynamic entity creation
- Fix temperature conversion (F to C)
- Add smart device caching
- Add custom icon
- Update documentation
"
```

### 2. Create Git Tag

```bash
git tag -a v1.1.0 -m "Version 1.1.0 - Real-Time MQTT Integration

Major release with full MQTT support, automatic device discovery,
and accurate temperature monitoring.

See RELEASE_NOTES_1.1.0.md for details."
```

### 3. Push to GitHub

```bash
# Push commits
git push origin main

# Push tag
git push origin v1.1.0
```

### 4. Create GitHub Release

1. Go to: https://github.com/djiesr/thermomaven-ha/releases/new
2. Select tag: `v1.1.0`
3. Release title: `ThermoMaven v1.1.0 - Real-Time MQTT Integration 🎉`
4. Copy content from `RELEASE_NOTES_1.1.0.md`
5. Attach ZIP file:
   ```bash
   cd custom_components
   zip -r thermomaven-1.1.0.zip thermomaven/
   ```
6. Check "Set as the latest release"
7. Click "Publish release"

### 5. Update HACS (if applicable)

If your integration is in HACS:
1. HACS will automatically detect the new tag
2. Users will see an update notification
3. No manual action needed

### 6. Announce Release

Post in:
- Home Assistant Community Forum
- Reddit r/homeassistant
- GitHub Discussions
- Your social media

### 7. Monitor Issues

After release:
- Watch for bug reports
- Respond to questions
- Plan next version based on feedback

## 📝 Release Announcement Template

```markdown
# 🎉 ThermoMaven v1.1.0 Released!

I'm excited to announce the first production-ready release of the ThermoMaven Home Assistant integration!

## What's New
- ⚡ Real-time temperature updates (~10 seconds)
- 🎨 Automatic device discovery
- 🌡️ Accurate temperature conversion
- 💾 Smart device caching
- 🎨 Custom icon

## Installation
Download from: https://github.com/djiesr/thermomaven-ha/releases/tag/v1.1.0

## Documentation
Full guide: https://github.com/djiesr/thermomaven-ha

Happy grilling! 🔥🍖
```

## 🔧 Post-Release

### Version Bump for Development

After release, bump to next dev version:

```bash
# In manifest.json
"version": "1.2.0-dev"

# Commit
git commit -am "Bump version to 1.2.0-dev"
git push
```

### Start Planning v1.2.0

Create issues for:
- Historical data graphs
- Cooking presets
- Multi-language support
- Advanced automations

## 🐛 Hotfix Process (if needed)

If critical bug found:

1. Create hotfix branch:
   ```bash
   git checkout -b hotfix/1.1.1
   ```

2. Fix bug and test

3. Update version to 1.1.1

4. Commit and tag:
   ```bash
   git commit -am "Hotfix v1.1.1 - Fix critical bug"
   git tag -a v1.1.1 -m "Hotfix v1.1.1"
   ```

5. Merge to main:
   ```bash
   git checkout main
   git merge hotfix/1.1.1
   git push origin main
   git push origin v1.1.1
   ```

6. Create GitHub release

## 📞 Support

After release, monitor:
- GitHub Issues
- GitHub Discussions
- Home Assistant Community Forum

Respond within 24-48 hours to:
- Bug reports
- Feature requests
- Questions

---

**Ready to release? Let's go! 🚀**

