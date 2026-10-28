#!/usr/bin/env bash
# Shows what public DNS returns for the records the site and email depend on.
for q in "NS matt-jones.org" "A matt-jones.org" "AAAA matt-jones.org" "CNAME www.matt-jones.org" \
         "MX matt-jones.org" "TXT matt-jones.org" "TXT google._domainkey.matt-jones.org" "TXT _dmarc.matt-jones.org"; do
  set -- $q; printf '%-6s %-36s ' "$1" "$2"; dig +short "$1" "$2" @8.8.8.8 | tr '\n' ' '; echo
done
for u in https://matt-jones.org https://www.matt-jones.org/about/; do curl -sSo /dev/null -w "$u -> %{http_code} %{redirect_url}\n" "$u"; done
