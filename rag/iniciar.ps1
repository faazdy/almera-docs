# Arranca el RAG-lite de SABIA. Uso:  .\iniciar.ps1
Set-Location $PSScriptRoot

if (-not (Test-Path .venv)) {
    Write-Host "Creando entorno virtual..."
    python -m venv .venv
    .venv\Scripts\python.exe -m pip install -q -r requirements.txt
}

if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host "Se creo rag\.env a partir de .env.example. Pon tu OPENROUTER_API_KEY y vuelve a ejecutar."
    exit 1
}

.venv\Scripts\python.exe -m app.main
