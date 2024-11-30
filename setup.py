import setuptools
import versioneer

# Cargar las dependencias desde el archivo requirements.txt
with open("requirements.txt", "r") as f:
    REQUIREMENTS = [line.strip() for line in f.readlines() if line.strip() and not line.startswith("-e")]

# Dependencias adicionales desde repositorios de Git
DEPENDENCY_LINKS = [
    "git+https://github.com/GRUNECO/eeg_harmonization.git@444ea6755b78a8428ac8534a5e721e52698f5513#egg=sovaharmony",
]

# Configuración de setuptools
setuptools.setup(
    name="sovaharmony",  # Cambia esto por el nombre de tu proyecto
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="sovaharmony",  # Actualiza la descripción
    packages=setuptools.find_packages(),
    python_requires=">=3.7",  # Especifica la versión mínima de Python requerida
    install_requires=REQUIREMENTS,  # Dependencias principales
    dependency_links=DEPENDENCY_LINKS,  # Dependencias desde Git
    setup_requires=["setuptools >= 38.3.0", "wheel", "versioneer"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Cambia según tu licencia
        "Operating System :: OS Independent",
    ],
)
