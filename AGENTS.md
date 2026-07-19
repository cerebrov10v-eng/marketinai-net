# AGENTS.md — MarketinAI (Kimi Code Context)
> Proyecto: marketinai.net | Actualizado: 2026-07-18

## 🎯 IDENTIDAD DEL PROYECTO
- **Producto**: Kit Automatización IA para CEOs — €397 fundador / €597 normal
- **Dominio**: marketinai.net
- **Stack**: React/Vite frontend + FastAPI backend (cuando exista)
- **Deploy**: Easypanel → `v10v-core_marketinai` | imagen `localhost:5000/cerebro-v10-marketinai:latest`
- **Puerto interno**: 32773

## 🔧 RUTAS CLAVE
```
E:\proyectos  pc2\marketinai\          → Raíz del proyecto
E:\proyectos  pc2\marketinai\src\      → Componentes React
E:\proyectos  pc2\marketinai\src\App.jsx → Router principal
E:\proyectos  pc2\marketinai\package.json
E:\proyectos  pc2\marketinai\vite.config.js
E:\proyectos  pc2\marketinai\nginx.conf
```

## ⚠️ ESTADO ACTUAL (2026-07-18)
- ✅ Landing desplegada en Easypanel
- ❌ Traefik routing 404 (www + apex) — pendiente fix
- Ver playbook: `/memories/traefik_deploy_playbook.md`

## 🛠️ COMANDOS FRECUENTES
```powershell
# Desarrollo local
cd "E:\proyectos  pc2\marketinai"; npm run dev

# Build y deploy
cd "E:\proyectos  pc2\marketinai"; npm run build
# Luego push a repo y redeploy en Easypanel

# Ver logs en VPS
ssh -i "C:\Users\rober\.ssh\id_vps_cerebro" root@72.61.193.34 "docker logs v10v-core_marketinai.1... --tail 50"
```

## 📋 REGLAS
- Python venv global: `E:\proyectos  pc2\.venv\Scripts\python.exe`
- NUNCA commitear `.env` ni API keys
- Git repo: ver `E:\Cerebro V10\AGENTS.md` para credenciales
