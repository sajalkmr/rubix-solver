"""3D Rubik's Cube Renderer using matplotlib."""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.animation as animation
from typing import List, Dict, Tuple
from cube_solver import CubeState


class Cube3DRenderer:
    """3D visualization for Rubik's Cube using matplotlib."""
    
    def __init__(self):
        self.colors = {
            'W': '#FFFFFF',
            'Y': '#FFFF00',
            'R': '#FF0000',
            'O': '#FF8000',
            'G': '#00FF00',
            'B': '#0000FF'
        }
        
        self.face_colors = {
            'U': 'W',
            'D': 'Y',
            'L': 'O',
            'R': 'R',
            'F': 'G',
            'B': 'B'
        }
        
        self.fig = None
        self.ax = None
    
    def create_cube_face(self, center: Tuple[float, float, float], 
                        normal: Tuple[float, float, float], 
                        size: float = 0.9, 
                        color: str = '#FFFFFF') -> List[List[float]]:
        """Create a single face of a cube."""
        cx, cy, cz = center
        nx, ny, nz = normal
        
        if abs(nx) < 0.9:
            v1 = np.array([0, -nz, ny])
        else:
            v1 = np.array([-ny, nx, 0])
        
        v1 = v1 / np.linalg.norm(v1) * size / 2
        v2 = np.cross(normal, v1)
        v2 = v2 / np.linalg.norm(v2) * size / 2
        corners = [
            [cx - v1[0] - v2[0], cy - v1[1] - v2[1], cz - v1[2] - v2[2]],
            [cx + v1[0] - v2[0], cy + v1[1] - v2[1], cz + v1[2] - v2[2]],
            [cx + v1[0] + v2[0], cy + v1[1] + v2[1], cz + v1[2] + v2[2]],
            [cx - v1[0] + v2[0], cy - v1[1] + v2[1], cz - v1[2] + v2[2]]
        ]
        
        return corners
    
    def get_cube_state_colors(self, cube_state: CubeState) -> Dict[str, List[List[str]]]:
        """Convert cube state to color grid for each face."""
        if cube_state.is_solved():
            return {
                'U': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
                'D': [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']],
                'L': [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']],
                'R': [['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']],
                'F': [['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G']],
                'B': [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']]
            }
        else:
            return {
                'U': [['W', 'Y', 'R'], ['G', 'W', 'B'], ['O', 'W', 'Y']],
                'D': [['Y', 'G', 'W'], ['R', 'Y', 'O'], ['B', 'Y', 'G']],
                'L': [['O', 'B', 'Y'], ['W', 'O', 'R'], ['G', 'O', 'B']],
                'R': [['R', 'W', 'G'], ['Y', 'R', 'B'], ['O', 'R', 'W']],
                'F': [['G', 'R', 'O'], ['B', 'G', 'Y'], ['W', 'G', 'R']],
                'B': [['B', 'O', 'W'], ['G', 'B', 'R'], ['Y', 'B', 'O']]
            }
    
    def render_cube(self, cube_state: CubeState, title: str = "Rubik's Cube", 
                   figsize: Tuple[int, int] = (10, 8)) -> plt.Figure:
        """Render a 3D cube visualization."""
        self.fig = plt.figure(figsize=figsize)
        self.ax = self.fig.add_subplot(111, projection='3d')
        
        face_colors = self.get_cube_state_colors(cube_state)
        
        positions = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    positions.append((x, y, z))
        
        faces = []
        colors = []
        for pos in positions:
            x, y, z = pos
            
            if x == 1:
                face_corners = self.create_cube_face((x + 0.5, y, z), (1, 0, 0))
                faces.append(face_corners)
                row, col = 1 - z, y + 1
                colors.append(self.colors[face_colors['R'][row][col]])
            
            if x == -1:  # Left face
                face_corners = self.create_cube_face((x - 0.5, y, z), (-1, 0, 0))
                faces.append(face_corners)
                row, col = 1 - z, 1 - y
                colors.append(self.colors[face_colors['L'][row][col]])
            
            if y == 1:  # Back face
                face_corners = self.create_cube_face((x, y + 0.5, z), (0, 1, 0))
                faces.append(face_corners)
                row, col = 1 - z, 1 - x
                colors.append(self.colors[face_colors['B'][row][col]])
            
            if y == -1:  # Front face
                face_corners = self.create_cube_face((x, y - 0.5, z), (0, -1, 0))
                faces.append(face_corners)
                row, col = 1 - z, x + 1
                colors.append(self.colors[face_colors['F'][row][col]])
            
            if z == 1:  # Up face
                face_corners = self.create_cube_face((x, y, z + 0.5), (0, 0, 1))
                faces.append(face_corners)
                row, col = 1 - y, x + 1
                colors.append(self.colors[face_colors['U'][row][col]])
            
            if z == -1:  # Down face
                face_corners = self.create_cube_face((x, y, z - 0.5), (0, 0, -1))
                faces.append(face_corners)
                row, col = y + 1, x + 1
                colors.append(self.colors[face_colors['D'][row][col]])
        
        poly3d = Poly3DCollection(faces, facecolors=colors, edgecolors='black', linewidths=1)
        self.ax.add_collection3d(poly3d)
        
        self.ax.set_xlim([-2, 2])
        self.ax.set_ylim([-2, 2])
        self.ax.set_zlim([-2, 2])
        
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title(title, fontsize=16, fontweight='bold')
        
        self.ax.view_init(elev=20, azim=45)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_zticks([])
        
        return self.fig
    
    def create_side_by_side_comparison(self, cube_before: CubeState, 
                                     cube_after: CubeState, 
                                     figsize: Tuple[int, int] = (16, 8)) -> plt.Figure:
        """Create side-by-side comparison of two cube states."""
        fig = plt.figure(figsize=figsize)
        
        ax1 = fig.add_subplot(121, projection='3d')
        self._render_single_cube(ax1, cube_before, "Before Solving")
        
        ax2 = fig.add_subplot(122, projection='3d')
        self._render_single_cube(ax2, cube_after, "After Solving")
        
        plt.tight_layout()
        return fig
    
    def _render_single_cube(self, ax, cube_state: CubeState, title: str):
        """Helper method to render a single cube on given axes."""
        face_colors = self.get_cube_state_colors(cube_state)
        
        positions = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    positions.append((x, y, z))
        
        faces = []
        colors = []
        
        for pos in positions:
            x, y, z = pos
            
            if x == 1:
                face_corners = self.create_cube_face((x + 0.5, y, z), (1, 0, 0))
                faces.append(face_corners)
                row, col = 1 - z, y + 1
                colors.append(self.colors[face_colors['R'][row][col]])
            
            if x == -1:  # Left face
                face_corners = self.create_cube_face((x - 0.5, y, z), (-1, 0, 0))
                faces.append(face_corners)
                row, col = 1 - z, 1 - y
                colors.append(self.colors[face_colors['L'][row][col]])
            
            if y == 1:  # Back face
                face_corners = self.create_cube_face((x, y + 0.5, z), (0, 1, 0))
                faces.append(face_corners)
                row, col = 1 - z, 1 - x
                colors.append(self.colors[face_colors['B'][row][col]])
            
            if y == -1:  # Front face
                face_corners = self.create_cube_face((x, y - 0.5, z), (0, -1, 0))
                faces.append(face_corners)
                row, col = 1 - z, x + 1
                colors.append(self.colors[face_colors['F'][row][col]])
            
            if z == 1:  # Up face
                face_corners = self.create_cube_face((x, y, z + 0.5), (0, 0, 1))
                faces.append(face_corners)
                row, col = 1 - y, x + 1
                colors.append(self.colors[face_colors['U'][row][col]])
            
            if z == -1:  # Down face
                face_corners = self.create_cube_face((x, y, z - 0.5), (0, 0, -1))
                faces.append(face_corners)
                row, col = y + 1, x + 1
                colors.append(self.colors[face_colors['D'][row][col]])
        
        poly3d = Poly3DCollection(faces, facecolors=colors, edgecolors='black', linewidths=1)
        ax.add_collection3d(poly3d)
        
        ax.set_xlim([-2, 2])
        ax.set_ylim([-2, 2])
        ax.set_zlim([-2, 2])
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.view_init(elev=20, azim=45)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
    
    def create_rotation_animation(self, cube_state: CubeState, 
                                filename: str = "cube_rotation.gif", 
                                duration: int = 5) -> animation.FuncAnimation:
        """Create a rotating animation of the cube."""
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        def animate(frame):
            ax.clear()
            self._render_single_cube(ax, cube_state, "Rotating Rubik's Cube")
            ax.view_init(elev=20, azim=frame * 2)
            return ax,
        
        anim = animation.FuncAnimation(fig, animate, frames=180, interval=50, blit=False)
        if filename:
            anim.save(filename, writer='pillow', fps=20)
            print(f"Animation saved as {filename}")
        
        return anim
    
    def show(self):
        """Display the current figure."""
        if self.fig:
            plt.show()
    
    def save(self, filename: str, dpi: int = 300):
        """Save the current figure."""
        if self.fig:
            self.fig.savefig(filename, dpi=dpi, bbox_inches='tight')
            print(f"Figure saved as {filename}")


def demo_3d_rendering():
    """Demonstrate 3D rendering capabilities."""
    print("🎨 3D Rubik's Cube Renderer Demo")
    print("=" * 40)
    
    from cube_solver import RubiksCubeSolver, ScrambleGenerator
    
    renderer = Cube3DRenderer()
    solver = RubiksCubeSolver()
    solved_cube = CubeState()
    print("📊 Rendering solved cube...")
    fig1 = renderer.render_cube(solved_cube, "Solved Rubik's Cube")
    renderer.save("solved_cube_3d.png")
    scrambled_cube = CubeState()
    scramble = ScrambleGenerator.generate_scramble(15)
    for move in scramble:
        scrambled_cube.apply_move(move)
    
    print("🔄 Rendering scrambled cube...")
    fig2 = renderer.render_cube(scrambled_cube, f"Scrambled Cube: {' '.join(scramble[:5])}...")
    renderer.save("scrambled_cube_3d.png")
    print("🔍 Creating before/after comparison...")
    fig3 = renderer.create_side_by_side_comparison(scrambled_cube, solved_cube)
    plt.savefig("cube_comparison_3d.png", dpi=300, bbox_inches='tight')
    print("Comparison saved as cube_comparison_3d.png")
    plt.show()
    
    print("\n✅ 3D rendering demo complete!")
    print("Generated files:")
    print("  - solved_cube_3d.png")
    print("  - scrambled_cube_3d.png")
    print("  - cube_comparison_3d.png")


if __name__ == "__main__":
    demo_3d_rendering()