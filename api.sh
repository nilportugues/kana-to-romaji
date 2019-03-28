echo fs.file-max=524288 | sudo tee -a /etc/sysctl.conf
echo fs.inotify.max_user_instances=524288 | sudo tee -a /etc/sysctl.conf
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
echo fs.inotify.max_queued_events=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

echo 'session required pam_limits.so' | sudo tee -a /etc/pam.d/common-session
ulimit -n

sudo python3 api/app.py
