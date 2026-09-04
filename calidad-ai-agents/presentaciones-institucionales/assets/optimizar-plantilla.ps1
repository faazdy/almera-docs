# Adelgaza plantilla.pptx para empaquetar la skill (necesita PowerPoint en Windows).
#
#   powershell -File optimizar-plantilla.ps1 [-Src plantilla-original.pptx] [-Out plantilla.pptx]
#
# Qué hace, vía automatización COM de PowerPoint:
#   1. borra todas las diapositivas de ejemplo,
#   2. borra el render de personaje de cada layout que se conserva
#      (el personaje se coloca en generación desde marca/personajes/),
#   3. borra los layouts que la skill no usa (lista $KEEP).
# PowerPoint compacta los `ppt/media` huérfanos al guardar.
#
# Resultado típico: ~46 MB  ->  ~0,8 MB.  Reejecutar si se actualiza la plantilla
# institucional; luego re-verificar portadas y separadores.

param(
  [string]$Src = "$PSScriptRoot\plantilla.pptx",
  [string]$Out = "$PSScriptRoot\plantilla.pptx"
)
$Src = (Resolve-Path $Src).Path

# layouts que usa pptx_kit (portada + contenido + 4 separadores)
$KEEP = @("Portada", "Contenido Tabla 4", "Separador1", "Separador2", "1_Separador1", "2_Separador1")
$msoPicture = 13

$pp = New-Object -ComObject PowerPoint.Application
try {
  $pres = $pp.Presentations.Open($Src, $false, $false, $false)   # RW, sin ventana

  while ($pres.Slides.Count -gt 0) { $pres.Slides.Item(1).Delete() }

  # render de personaje: picture 300-520pt de ancho, >300pt de alto, pegado a la izquierda
  foreach ($cl in $pres.SlideMaster.CustomLayouts) {
    if ($KEEP -notcontains $cl.Name) { continue }
    for ($i = $cl.Shapes.Count; $i -ge 1; $i--) {
      $sh = $cl.Shapes.Item($i)
      if ($sh.Type -eq $msoPicture -and $sh.Width -gt 300 -and $sh.Width -lt 520 `
          -and $sh.Height -gt 300 -and $sh.Left -lt 200) {
        Write-Output ("{0}: quito {1}" -f $cl.Name, $sh.Name)
        $sh.Delete()
      }
    }
  }

  for ($i = $pres.SlideMaster.CustomLayouts.Count; $i -ge 1; $i--) {
    $cl = $pres.SlideMaster.CustomLayouts.Item($i)
    if ($KEEP -notcontains $cl.Name) {
      try { $cl.Delete() } catch { Write-Output ("no pude borrar layout {0}" -f $cl.Name) }
    }
  }

  $tmp = [System.IO.Path]::Combine([System.IO.Path]::GetDirectoryName($Out), "_opt_tmp.pptx")
  if (Test-Path $tmp) { Remove-Item $tmp -Force }
  $pres.SaveAs($tmp, 24)   # 24 = ppSaveAsOpenXMLPresentation
  $pres.Close()
  Move-Item $tmp $Out -Force
  Write-Output ("OK -> {0}  ({1:N2} MB)  layouts: {2}" -f $Out, ((Get-Item $Out).Length / 1MB), ($KEEP -join ", "))
} finally {
  $pp.Quit()
  [System.Runtime.InteropServices.Marshal]::ReleaseComObject($pp) | Out-Null
}
