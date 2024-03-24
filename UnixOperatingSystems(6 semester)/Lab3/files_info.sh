find / -type f -exec ls -l {} + 2>/dev/null | awk '{print $5}' > file_sizes.txt


