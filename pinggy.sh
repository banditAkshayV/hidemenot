#!/bin/bash

WEBHOOK_URL="https://defaulte700286ed8144d0a98f7bb2984d70a.25.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/c84f248ed7fc43d8b0b75c24415ff90f/triggers/manual/paths/invoke?api-version=1&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=TvZ0e1i362xUDKGw9s6_pZEbPaHro3rGpFic1W4ZdM8"
PINGGY_USER="MwN3OoUZtqf"
PINGGY_HOST="ap.free.pinggy.io"

while true; do
  echo "[*] Starting Pinggy tunnel..."
  
  ssh -p 443 -R0:localhost:5000 \
    -o StrictHostKeyChecking=no \
    -o ServerAliveInterval=30 \
    "${PINGGY_USER}@${PINGGY_HOST}" 2>&1 | while read -r line; do
      echo "[pinggy] $line"
      
      if [[ "$line" =~ (http[s]?://[a-zA-Z0-9.-]+\.pinggy\.link) ]]; then
        URL="${BASH_REMATCH[1]}"
        echo "[+] Detected URL: $URL"
        
        # Send webhook
        curl -X POST -H "Content-Type: application/json" \
             -d "{\"url\": \"$URL\"}" "$WEBHOOK_URL"
      fi
    done

  echo "[!] Tunnel ended. Restarting in 10 seconds..."
  sleep 10
done
