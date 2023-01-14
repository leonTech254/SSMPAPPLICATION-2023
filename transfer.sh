cp -R * /home/leon/workspace/TOOLS/BUILDOZER/BUILD/
cd /home/leon/workspace/TOOLS/BUILDOZER/  
buildozer -v android debug deploy run
cd -

git add .
git commit -m "--update-auto"
git push -u origin main