$root = "C:\PROJETOS-LAB\project-management-intelligence"
$output = "$root\estrutura.txt"
$ignore = @(".venv", "__pycache__", ".git")

function Show-Tree {
    param ($path, $indent = "")

    $items = Get-ChildItem -Path $path | Where-Object { $_.Name -notin $ignore }

    foreach ($item in $items) {
        if ($item.PSIsContainer) {
            Add-Content $output "${indent}[DIR] $($item.Name)"
            Show-Tree -path $item.FullName -indent "$indent    "
        } else {
            Add-Content $output "${indent}[FILE] $($item.Name)"
        }
    }
}

if (Test-Path $output) { Remove-Item $output }

Add-Content $output "[DIR] project-management-intelligence"
Show-Tree -path $root

Write-Host "Estrutura exportada para: $output"