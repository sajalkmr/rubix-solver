#!/usr/bin/env python3
"""Quick test for 3D Rubik's Cube visualization."""

import sys
try:
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    print("✅ All required packages available")
except ImportError as e:
    print(f"❌ Missing package: {e}")
    print("Please install requirements: pip install -r requirements.txt")
    sys.exit(1)

from cube_solver import CubeState, ScrambleGenerator
from cube_3d_renderer import Cube3DRenderer

def quick_test():
    print("🧪 Quick 3D Visualization Test")
    print("=" * 30)
    
    renderer = Cube3DRenderer()
    cube = CubeState()
    
    print("📊 Creating solved cube...")
    fig = renderer.render_cube(cube, "Test Cube")
    
    print("🔄 Creating scrambled cube...")
    scrambled = CubeState()
    scramble = ["R", "U", "F", "L"]
    for move in scramble:
        scrambled.apply_move(move)
    
    fig2 = renderer.render_cube(scrambled, "Scrambled Test")
    
    print("✅ 3D rendering test successful!")
    print("Close the matplotlib windows to exit.")
    
    plt.show()

if __name__ == "__main__":
    quick_test()