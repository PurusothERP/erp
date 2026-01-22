#!/bin/bash
echo "--------------------------------------------------------"
echo "Easy GitHub Login"
echo "--------------------------------------------------------"
echo "1. I will launch the GitHub login process."
echo "2. You will see a CODE (e.g., 0000-0000)."
echo "3. Copy that code."
echo "4. Press ENTER to open your browser."
echo "5. Paste the code and click 'Authorize'."
echo "--------------------------------------------------------"
echo ""
gh auth login --hostname github.com --git-protocol https --web
