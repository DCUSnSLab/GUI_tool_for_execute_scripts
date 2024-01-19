#!/bin/bash
echo "* TEST1 SHELL SCRIPT IS RUNNING !"
echo "* WAIT . . ."
sleep 3s
echo "Hello World!" > "$(date '+%Y%m%d_%H시-%M분-%S초_1').txt"
echo "* File Saved !"
echo "*---*---*---*"