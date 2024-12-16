# Namecheap-DynDNS

A simple containerised dynamic DNS updater for Namecheap

[Namecheap-DynDNS](https://github.com/enayet123/Namecheap-DynDNS) utilises Namecheaps DynDNS REST API

## Installation/Setup

### Docker

The docker image is available and can be pulled from Docker Hub: [enayet123/namecheap-dyndns](https://hub.docker.com/r/enayet123/namecheap-dyndns)

> **Note:** DOMAIN, DYNAMIC_DNS_PASSWORD and SUBDOMAINS are required environment variables

docker compose:

```
services:
  namecheap:
    image: enayet123/namecheap-dyndns:latest
    container_name: namecheap
    restart: unless-stopped
    environment:
      - DOMAIN=your.domain.com
      - DYNAMIC_DNS_PASSWORD=password
      - SUBDOMAINS=@,subdomain,portal,admin # '@' updates the root domain
      - CHECK_INTERVAL_SECONDS=3600
```

Docker CLI:

```
docker run -d \
  --name=namecheap \
  -e DOMAIN=your.domain.com \
  -e DYNAMIC_DNS_PASSWORD=password \
  -e SUBDOMAINS=@,subdomain,portal,admin \ # '@' updates the root domain
  -e CHECK_INTERVAL_SECONDS=3600 \
  --restart unless-stopped \
  enayet123/namecheap-dyndns:latest
```

### Python

> **Note:** The following steps assume you already have python installed in your environment.

Clone the repository to a location of your choice
```
git clone git@github.com:enayet123/Namecheap-DynDNS.git
cd Namecheap-DynDNS
```

Provide the required environment variables and run the application
```
DOMAIN=your.domain.com DYNAMIC_DNS_PASSWORD=password SUBDOMAINS=subdomain,portal,admin CHECK_INTERVAL_SECONDS=3600 python main.py
```

## Environment Variables

All variables are optional however providing none will result in the application quitting

| Variable                    | Description                                                                                          |
|-----------------------------|------------------------------------------------------------------------------------------------------|
| `DOMAIN`                    | The domain you want to dynamically update the IP address for                                         |
| `DYNAMIC_DNS_PASSWORD`      | Your namecheap DynDNS password found under Advanced DNS                                              |
| `SUBDOMAINS`                | A list of subdomains to update                                                                       |
| `CHECK_INTERVAL_SECONDS`    | The time interval between IP address checks (optional)                                               |

## Disclaimer 

This application is provided "as is" without any warranties or guarantees of any kind, either express or implied. The use of this application is at your own risk. The developers assume no liability for any damages, losses, or issues, including but not limited to data loss, system malfunctions, or financial impacts, that may arise from the use or misuse of this application.

By using this application, you agree to take full responsibility for any outcomes and understand that the developers are not liable for any consequences resulting from its use. Always test the application in a controlled environment before deploying it in production.
