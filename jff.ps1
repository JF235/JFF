if ($args.Count -eq 1) {
    # Se houver um argumento, usa esse valor como nome do arquivo
    $file = $args[0]

    # Verifica se o arquivo tem a extensão .md
    if (-not ($file -like "*.md")) {
        $string = "Arquivo $file com extensão não suportada"
        Write-Output $string
        Exit
    }
}
else {
    # Obtém a lista de arquivos .md no diretório atual
    $arquivosMD = Get-ChildItem -Filter *.md

    # Verifica a quantidade de arquivos .md
    if ($arquivosMD.Count -eq 1) {
        # Se houver apenas um arquivo .md, armazena seu nome na variável $file
        $file = $arquivosMD[0].Name
    }
    elseif ($arquivosMD.Count -gt 1) {
        Write-Output "Há mais de um arquivo .md no diretório"
        Exit
    }
    else {
        Write-Output "Nenhum arquivo .md encontrado no diretório"
        Exit
    }
}

# Constrói o caminho completo para o script Python
$scriptPath = Join-Path $PSScriptRoot "src\jff.py"

# Executa o programa Python com o nome do arquivo como argumento
python $scriptPath $file