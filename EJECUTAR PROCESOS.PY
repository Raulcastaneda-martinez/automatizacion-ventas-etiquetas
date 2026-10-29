import subprocess

# Lista de scripts a ejecutar en orden
scripts = [
    "ET.PY",  # Reemplaza con tu primer script
    "NP.py",  # Reemplaza con tu segundo script
    ]

for script in scripts:
    print(f"▶️ Ejecutando {script}...")
    try:
        subprocess.run(["python", script], check=True)
        print(f"✅ Finalizado: {script}\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al ejecutar {script}: {e}\n")
        break  # Detiene la ejecución si hay un error
