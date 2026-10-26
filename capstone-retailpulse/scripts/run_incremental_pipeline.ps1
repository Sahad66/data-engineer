
$ErrorActionPreference = "Stop"

# Project paths
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$PythonExe = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$PipelineScript = Join-Path $ProjectRoot "src\retailpulse\run_incremental_pipeline.py"

# Log path
$LogDir = Join-Path $ProjectRoot "logs"
$LogFile = Join-Path $LogDir "scheduled_pipeline.log"

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

# Check required files
if (-not (Test-Path $PythonExe)) {
    throw "Python virtual environment not found: $PythonExe"
}

if (-not (Test-Path $PipelineScript)) {
    throw "Pipeline script not found: $PipelineScript"
}

# Run pipeline and save output
"[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Pipeline started" |
    Tee-Object -FilePath $LogFile -Append

& $PythonExe $PipelineScript 2>&1 |
    Tee-Object -FilePath $LogFile -Append

$PipelineExitCode = $LASTEXITCODE

"[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Pipeline exit code: $PipelineExitCode" |
    Tee-Object -FilePath $LogFile -Append

if ($PipelineExitCode -ne 0) {
    exit $PipelineExitCode
}

exit 0
