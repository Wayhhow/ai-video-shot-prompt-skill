# install.ps1 - 把本 skill 一键安装到 Trae IDE 的 skills 目录
#
# 用法：
#   .\install.ps1                                    # 安装到默认路径
#   .\install.ps1 -DestDir "C:\my\skills\foo"      # 安装到自定义路径
#   .\install.ps1 -Force                             # 目标目录非空时跳过确认，直接覆盖安装
#
# 兼容：Windows PowerShell 5.1+ / PowerShell Core 7+
[CmdletBinding()]
param(
    [string]$DestDir,
    [switch]$Force
)

# 解析脚本所在目录
$src = Split-Path -Parent $MyInvocation.MyCommand.Path

# 目标目录
if (-not $DestDir) {
    $DestDir = Join-Path $env:USERPROFILE ".trae\skills\crafting-ai-video-shot-prompts"
}

# 防止装到根目录
if ([string]::IsNullOrEmpty($DestDir) -or $DestDir -eq "\" -or $DestDir -eq "/") {
    Write-Error "ERROR: 目标目录无效: $DestDir"
    exit 2
}

# 防止把脚本装到自己头上
# 用 GetFullPath 而非 Resolve-Path：目标目录尚不存在时 Resolve-Path 会报错
$srcFull = [IO.Path]::GetFullPath($src).TrimEnd('\', '/')
$dstFull = [IO.Path]::GetFullPath($DestDir).TrimEnd('\', '/')
if ($srcFull -ieq $dstFull) {
    Write-Error "ERROR: 源目录与目标目录相同: $src"
    exit 2
}

# 目标目录已存在且非空：默认要求确认，防止误选重要目录导致同名文件被覆盖
if ((Test-Path $DestDir) -and (Get-ChildItem -Path $DestDir -Force -ErrorAction SilentlyContinue | Select-Object -First 1)) {
    if (-not $Force) {
        Write-Host "WARN: 目标目录已存在且非空: $DestDir" -ForegroundColor Yellow
        Write-Host "      同名文件将被覆盖。如确认无误请输入 yes；或用 -Force 跳过本确认。"
        $ans = Read-Host "继续安装? [yes/N]"
        if ($ans -ne "yes") {
            Write-Error "已取消安装。"
            exit 3
        }
    }
}

# 确保目标存在
New-Item -ItemType Directory -Force -Path $DestDir | Out-Null

# 复制内容（含隐藏文件，但跳过 .git）
Get-ChildItem -Path $src -Force | Where-Object { $_.Name -ne ".git" } | ForEach-Object {
    $target = Join-Path $DestDir $_.Name
    if ($_.PSIsContainer) {
        Copy-Item -Path $_.FullName -Destination $target -Recurse -Force
    } else {
        Copy-Item -Path $_.FullName -Destination $target -Force
    }
}

Write-Host "Installed to $DestDir"
Write-Host ""
Write-Host "下一步："
Write-Host "  1. 重启 Trae IDE 或重载窗口"
Write-Host "  2. 在对话中提到「写一个 AI 视频提示词」即可触发本 skill"
