# Lista de pastas numeradas
$folders = Get-ChildItem -Directory -Filter 'ex*' | Sort-Object Name

foreach ($folder in $folders) {
    # Entra na pasta
    Set-Location $folder.FullName

    # Executa o comando jff
    # jff

    # Obtém o nome do arquivo .md na pasta
    $mdFile = Get-ChildItem -Filter '*.md' | Select-Object -First 1

    if ($mdFile) {
        # Gera o nome do arquivo .html
        $referenceFile = $mdFile.BaseName + '.html'
        $newFile = $mdFile.BaseName + '_new.html'

        $diff = Compare-Object -ReferenceObject (Get-Content $referenceFile) -DifferenceObject (Get-Content $newFile -ErrorAction SilentlyContinue)

        if ($null -eq $diff) {
            Write-Host "✅ OK - Conteúdos são idênticos para $($folder.Name)"
        } else {
            Write-Host "❌ ERRO - Conteúdos são diferentes para $($folder.Name)"
            # Mostra as diferenças se necessário
            $diff
        }
    } else {
        Write-Host "ERRO - Nenhum arquivo .md encontrado para $($folder.Name)"
    }

    # Volta para a pasta original
    Set-Location ..

}

