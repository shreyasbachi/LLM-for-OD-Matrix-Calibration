#!/usr/bin/bash
#SBATCH --job-name=pipeline_initialize          # Name of your job
#SBATCH --mail-user=sbachira@asu.edu            # Replace with your email
#SBATCH --mail-type=ALL                         # Notifications for BEGIN, END, FAIL, etc.
#SBATCH --output=wine-build.log                 # Standard output log
#SBATCH --cpus-per-task=4
#SBATCH --error=wine-build.err                  # Error log
#SBATCH --partition=general                     # Partition name
#SBATCH --nodes=1                               # Number of nodes
#SBATCH --ntasks=4                              # Number of tasks (cores)
#SBATCH --time=02:00:00                         # Time limit for the job
#SBATCH --mem=16G                               # Memory allocation

# Stop script on any error
set -e

# Load necessary modules
module load gcc-11.2.0-gcc-11.2.0
module load cmake-3.26.5-gcc-11.2.0

# Navigate to the build directory
cd ~/wine-build

# Clone Wine source if not already cloned
if [ ! -d "wine" ]; then
    echo "Cloning Wine source repository..."
    git clone https://gitlab.winehq.org/wine/wine.git
fi

# Navigate to the source directory
cd wine

# Update repository to get the latest code
echo "Updating Wine source repository..."
git pull

# Configure Wine for building
echo "Configuring Wine for local build..."
./configure --enable-win64 --prefix=$HOME/.local/wine-build

# Build Wine using 4 cores
echo "Building Wine..."
make -j4

# Install Wine to the local directory
echo "Installing Wine locally..."
make install

# Add Wine to PATH (if not already added)
export PATH=$HOME/.local/wine-build/bin:$PATH
echo "Add the following to your shell profile to make Wine available globally:"
echo "export PATH=\$HOME/.local/wine-build/bin:\$PATH"

echo "Wine build and installation complete. Check logs for details."