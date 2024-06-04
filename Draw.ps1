param($model)
ForEach($file in Get-ChildItem .\Personnal_simulations\output_$model\strongly_connected_components\*.dot) {
    dot -Tsvg $file.FullName > .\Personnal_simulations\output_$model\strongly_connected_components\$($file.BaseName).svg
}