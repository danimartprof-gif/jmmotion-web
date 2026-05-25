# JM-MOTION · Web

Web landing para JM-MOTION (Fisioterapia & Readaptación, El Campello).

## Stack
- HTML5 + TailwindCSS (CDN)
- Imágenes WebP (responsive `srcset`)
- Dockerizado con nginx:alpine

## Local preview
```bash
python3 -m http.server 8910
# http://127.0.0.1:8910/
```

## Build & run con Docker
```bash
docker build -t jmmotion-web .
docker run --rm -p 8080:80 jmmotion-web
```

## Deploy
Coolify auto-deploy desde `main`.

---
Desarrollado por [Stratoma AI](https://stratomai.com)
