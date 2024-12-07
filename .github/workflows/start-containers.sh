# .github/workflows/deploy-start-containers.sh

#!/bin/bash
set -e

# Connect to EC2 and deploy the start-containers script
ssh -o "StrictHostKeyChecking=no" "$EC2_USER@$EC2_HOST" << 'EOF'
# Define the content of start-containers.sh
cat <<SCRIPT > /home/ubuntu/start-containers.sh
#!/bin/bash
stopped_containers=$(sudo docker ps -a -q)

if [ -n "$stopped_containers" ]; then
  echo "Starting containers..."
  for container in $stopped_containers; do
    sudo docker start -a $container
  done
else
  echo "No containers to start."
fi
SCRIPT

# Make the script executable. Verify the path
chmod +x /home/ubuntu/start-containers.sh 

# Add the script to run on reboot via cron
(sudo crontab -l 2>/dev/null; echo "@reboot /home/ubuntu/start-containers.sh") | sudo crontab -
EOF
