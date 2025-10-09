#!/bin/bash

set -euo pipefail

urls=(
  "https://flashpaper-dev3.chime.com"
  "https://docs-dev3.chime.com"
  "https://flashpaper.chime.com"
  "https://flashpaper-dev1.chime.com"
  "https://chime-com-dev1.chime.com"
  "https://flashpaper-qa.chime.com"
  "https://flashpaper-dev4.chime.com"
  "https://vpn.chime.com"
  "https://wp-dev2.chime.com"
)

for url in "${urls[@]}"; do
  # strip scheme and path -> hostname
  host="${url#*://}"
  host="${host%%/*}"

  # run dig
  ips=$(dig +short "$host" | tr '\n' ' ' | sed 's/ *$//')

  if [ -z "$ips" ]; then
    ips="(no A/AAAA records returned)"
  fi

  printf "%-40s %s\n" "$url" "$ips"
done

