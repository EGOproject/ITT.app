@echo off
echo checking connectivity
ping www.github.com
pause
cls
echo checking repository status
git status
pause
cls
echo Adding changes and new files for tracking
git add .
git add .
pause
cls
echo Commiting to local repo
git commit -m "Backup by: EGO on %date% %time%"
pause
cls
echo updating local repo with remote changes
git pull
pause
cls
echo updating remote repo with local changes
git push
pause
cls
echo checking current status
git status
pause
cls
echo Backup and Update Complete!!!
pause
