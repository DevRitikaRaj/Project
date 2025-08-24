#!/usr/bin/env python3
"""
Setup script for ChemAI - Chemical Analysis with 3D Visualization
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"⏳ {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def install_basic_dependencies():
    """Install basic dependencies that work in most environments"""
    basic_packages = [
        "flask",
        "flask-cors", 
        "numpy",
        "pandas",
        "scikit-learn",
        "matplotlib",
        "plotly"
    ]
    
    for package in basic_packages:
        success = run_command(
            f"pip install --user {package}",
            f"Installing {package}"
        )
        if not success:
            return False
    
    return True

def install_rdkit():
    """Attempt to install RDKit (may fail in some environments)"""
    print("\n🧪 Attempting to install RDKit for full chemical analysis functionality...")
    print("   This may take several minutes and might fail in some environments.")
    
    # Try conda first (if available)
    conda_success = run_command(
        "conda install -c conda-forge rdkit-pypi -y",
        "Installing RDKit via conda"
    )
    
    if conda_success:
        return True
    
    # Try pip as fallback
    pip_success = run_command(
        "pip install --user rdkit-pypi",
        "Installing RDKit via pip"
    )
    
    if not pip_success:
        print("⚠️  RDKit installation failed. The application will run with simplified functionality.")
        print("   For full functionality, please install RDKit manually:")
        print("   - Using conda: conda install -c conda-forge rdkit")
        print("   - Using pip: pip install rdkit-pypi")
        print("   - Or follow instructions at: https://www.rdkit.org/docs/Install.html")
    
    return pip_success

def create_run_script():
    """Create a simple run script"""
    script_content = """#!/bin/bash
# ChemAI Run Script

export PATH="$HOME/.local/bin:$PATH"

echo "🚀 Starting ChemAI..."
echo "📊 Chemical Analysis with 3D Visualization"
echo ""

# Check if RDKit is available
python3 -c "import rdkit" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ RDKit detected - running full version"
    python3 app.py
else
    echo "⚠️  RDKit not found - running simplified version"
    echo "   Install RDKit for full functionality"
    python3 app_simple.py
fi
"""
    
    with open("run.sh", "w") as f:
        f.write(script_content)
    
    os.chmod("run.sh", 0o755)
    print("✅ Created run script (run.sh)")

def main():
    """Main setup function"""
    print("🧪 ChemAI Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install basic dependencies
    print("\n📦 Installing basic dependencies...")
    if not install_basic_dependencies():
        print("❌ Failed to install basic dependencies")
        sys.exit(1)
    
    # Try to install RDKit
    print("\n🔬 Installing advanced chemistry libraries...")
    rdkit_available = install_rdkit()
    
    # Create run script
    print("\n📝 Creating run script...")
    create_run_script()
    
    # Final instructions
    print("\n" + "=" * 50)
    print("🎉 Setup completed!")
    print("")
    
    if rdkit_available:
        print("✅ Full functionality available")
        print("   Run: python3 app.py")
    else:
        print("⚠️  Simplified functionality available")
        print("   Run: python3 app_simple.py")
        print("   Or: ./run.sh")
    
    print("")
    print("🌐 Open http://localhost:5000 in your browser")
    print("📚 See README.md for detailed usage instructions")
    print("")

if __name__ == "__main__":
    main()