#!/bin/zsh
# Script to timestamp, hash, and commit all defensive publications for legal archiving

date_str=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "Timestamp: $date_str" > TIMESTAMP.txt
sha256sum DEFENSE_PUBLICATION_MASTER.md > DEFENSE_PUBLICATION_MASTER.sha256

git add DEFENSE_PUBLICATION_MASTER.md DEFENSE_PUBLICATION_MASTER.sha256 TIMESTAMP.txt README.md

git commit -m "Defensive publication: $date_str (Dealvoy AI System)"

git push

echo "Defensive publication committed and pushed with timestamp $date_str."
