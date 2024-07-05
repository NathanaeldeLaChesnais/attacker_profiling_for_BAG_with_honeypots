#!/bin/bash

model=$1

for file in ./Personnal_simulations/output_"$model"/strongly_connected_components/*.dot; do
    echo "Drawing $(basename "$file" .dot)"
    dot -Tpng "$file" > "./Personnal_simulations/output_$model/strongly_connected_components/$(basename "$file" .dot).png"
done