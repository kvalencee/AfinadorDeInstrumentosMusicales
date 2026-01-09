#!/bin/bash
# Script de lanzamiento para Afinador Musical
# Doble clic para abrir la aplicación

# Obtener el directorio donde está este script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activar el entorno conda y ejecutar la aplicación
cd "$DIR"
source /opt/anaconda3/etc/profile.d/conda.sh
conda activate instrumentos
python tuner_gui.py
