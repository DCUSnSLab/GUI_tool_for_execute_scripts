#!/bin/bash
echo "@ TEST2 SHELL SCRIPT IS RUNNING TOO !"
echo "@ AND I WANNA GO HOME :("
echo "@ WAIT . . . . ."
sleep 5s
echo "Bye World!" > "$(date '+%Y%m%d_%H시-%M분-%S초_2').txt"
echo "@ File Saved !"
echo "@---@---@---@"

