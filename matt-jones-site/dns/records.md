# DNS for matt-jones.org

DNS is managed at Squarespace: **Settings → Domains → matt-jones.org → DNS**.
The website is served by GitHub Pages. Email is Google Workspace.

## Website (GitHub Pages)

Delete the Squarespace website records (the "Squarespace Defaults" preset: the four `198.x` A
records, the `www` → `ext-cust.squarespace.com` CNAME, and the `verify.squarespace.com` CNAME).
Then add:

| Host  | Type  | Value                     |
|-------|-------|---------------------------|
| `@`   | A     | `185.199.108.153`         |
| `@`   | A     | `185.199.109.153`         |
| `@`   | A     | `185.199.110.153`         |
| `@`   | A     | `185.199.111.153`         |
| `@`   | AAAA  | `2606:50c0:8000::153`     |
| `@`   | AAAA  | `2606:50c0:8001::153`     |
| `@`   | AAAA  | `2606:50c0:8002::153`     |
| `@`   | AAAA  | `2606:50c0:8003::153`     |
| `www` | CNAME | `matt-jones-org.github.io`|

Optional but recommended, to stop anyone else's GitHub repo from claiming the domain: in
GitHub (your profile **Settings → Pages → Add a domain**), add `matt-jones.org`. GitHub shows a
TXT record (`_github-pages-challenge-matt-jones-org`) to add here.

## Email (Google Workspace): leave alone

Keep whatever Google Workspace records exist. They're usually shown as the "Google Workspace"
preset. Don't touch MX, the `v=spf1` TXT, `google._domainkey`, `_dmarc`, or any
`google-site-verification` TXT. If any are missing, the target values are:

| Host                | Type | Value                                               |
|---------------------|------|-----------------------------------------------------|
| `@`                 | MX   | `1 smtp.google.com`                                 |
| `@`                 | TXT  | `v=spf1 include:_spf.google.com ~all`               |
| `google._domainkey` | TXT  | DKIM key from admin.google.com → Gmail → Authenticate email |
| `_dmarc`            | TXT  | `v=DMARC1; p=none; rua=mailto:matt@matt-jones.org`  |
