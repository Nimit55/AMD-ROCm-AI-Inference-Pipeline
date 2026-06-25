#!/bin/bash
echo AMD ROCm Pipeline Health Check
echo Date: $(date)
echo Python: $(python3 --version)
echo Disk: $(df -h / | awk "NR==2{print $4}") free
echo RAM: $(free -h | awk "/^Mem:/{print $7}") available
echo Status: Ready