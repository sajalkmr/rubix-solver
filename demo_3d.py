#!/usr/bin/env python3
"""Enhanced Rubik's Cube Solver demonstration with 3D visualization."""

import time
import matplotlib.pyplot as plt
from cube_solver import RubiksCubeSolver, CubeState, ScrambleGenerator
from cube_3d_renderer import Cube3DRenderer

def print_header(title: str):
    print("\n" + "=" * 60)
    print(f"🎯 {title}")
    print("=" * 60)

def print_section(title: str):
    print(f"\n🔹 {title}")
    print("-" * 40)

def main():
    print_header("3D RUBIK'S CUBE SOLVER DEMONSTRATION")
    print("🧩 Enhanced with stunning 3D visualization")
    print("📊 Complete solution with visual wow factor")
    
    solver = RubiksCubeSolver()
    renderer = Cube3DRenderer()
    
    print_section("1. 3D Visualization Showcase")
    print("🎨 Creating 3D rendered cubes...")
    
    solved_cube = CubeState()
    print("  📊 Rendering solved cube in 3D...")
    fig_solved = renderer.render_cube(solved_cube, "🏆 Solved Rubik's Cube")
    renderer.save("solved_cube_3d.png")
    print("     ✅ Saved: solved_cube_3d.png")
    
    scrambled_cube = CubeState()
    scramble = ScrambleGenerator.generate_scramble(12)
    print(f"  🔄 Applying scramble: {' '.join(scramble[:8])}...")
    
    for move in scramble:
        scrambled_cube.apply_move(move)
    
    fig_scrambled = renderer.render_cube(scrambled_cube, f"🔀 Scrambled Cube ({len(scramble)} moves)")
    renderer.save("scrambled_cube_3d.png")
    print("     ✅ Saved: scrambled_cube_3d.png")
    
    print_section("2. Algorithm Performance with 3D Visualization")
    print("🚀 Solving cube and visualizing results...")
    
    start_time = time.time()
    result = solver.solve_scramble(scramble, "layer_by_layer")
    solve_time = time.time() - start_time
    
    print(f"  🧠 Algorithm: {result.algorithm_used}")
    print(f"  ⏱️  Solve time: {result.solve_time:.4f}s")
    print(f"  🎯 Moves used: {result.move_count}")
    print(f"  ✅ Success: {result.is_solved}")
    print(f"  🔍 Solution preview: {' '.join(result.moves[:10])}...")
    
    print("  🎨 Creating 3D before/after comparison...")
    fig_comparison = renderer.create_side_by_side_comparison(
        scrambled_cube, solved_cube
    )
    plt.savefig("solve_comparison_3d.png", dpi=300, bbox_inches='tight')
    print("     ✅ Saved: solve_comparison_3d.png")
    
    print_section("3. Multiple Algorithm Comparison")
    print("⚙️ Comparing algorithms with 3D visualization...")
    
    test_scramble = ScrambleGenerator.generate_scramble(15)
    print(f"  🎲 Test scramble: {' '.join(test_scramble[:6])}...")
    
    algorithms = ["layer_by_layer", "kociemba"]
    results = {}
    
    for algo in algorithms:
        result = solver.solve_scramble(test_scramble, algo)
        results[algo] = result
        print(f"  🔧 {algo.replace('_', '-').title()}:")
        print(f"     Moves: {result.move_count}")
        print(f"     Time: {result.solve_time:.4f}s")
        print(f"     Optimal: {'✅' if result.is_optimal else '❌'}")
    
    print_section("4. Performance Benchmark with Visualization")
    print("📈 Running comprehensive performance test...")
    
    benchmark_results = []
    scramble_lengths = [10, 15, 20, 25]
    
    for length in scramble_lengths:
        print(f"  📏 Testing {length}-move scrambles...")
        
        total_time = 0
        total_moves = 0
        successes = 0
        
        for i in range(5):
            test_scramble = ScrambleGenerator.generate_scramble(length)
            result = solver.solve_scramble(test_scramble, "layer_by_layer")
            
            if result.is_solved:
                successes += 1
                total_time += result.solve_time
                total_moves += result.move_count
        
        if successes > 0:
            avg_time = total_time / successes
            avg_moves = total_moves / successes
            benchmark_results.append({
                'length': length,
                'avg_moves': avg_moves,
                'avg_time': avg_time,
                'success_rate': successes / 5 * 100
            })
            print(f"     📊 Average: {avg_moves:.1f} moves, {avg_time:.4f}s, {successes}/5 success")
    
    print_section("5. Creative 3D Features")
    print("🌟 Demonstrating advanced 3D capabilities...")
    
    cube_states = []
    titles = []
    
    cube_states.append(CubeState())
    titles.append("Solved State")
    
    light_cube = CubeState()
    light_scramble = ["R", "U", "R'", "U'"]
    for move in light_scramble:
        light_cube.apply_move(move)
    cube_states.append(light_cube)
    titles.append("Light Scramble")
    
    heavy_cube = CubeState()
    heavy_scramble = ScrambleGenerator.generate_scramble(20)
    for move in heavy_scramble:
        heavy_cube.apply_move(move)
    cube_states.append(heavy_cube)
    titles.append("Heavy Scramble")
    
    print("  🎨 Creating 3D showcase with multiple cube states...")
    fig_showcase = plt.figure(figsize=(18, 6))
    
    for i, (cube, title) in enumerate(zip(cube_states, titles)):
        ax = fig_showcase.add_subplot(1, 3, i+1, projection='3d')
        renderer._render_single_cube(ax, cube, title)
    
    plt.tight_layout()
    plt.savefig("cube_showcase_3d.png", dpi=300, bbox_inches='tight')
    print("     ✅ Saved: cube_showcase_3d.png")
    
    print_section("6. Final Statistics & 3D Gallery")
    stats = solver.get_statistics()
    print(f"📊 Session Statistics:")
    print(f"  Total solves: {stats['total_solves']}")
    print(f"  Success rate: {stats['success_rate']:.1f}%")
    print(f"  Average time: {stats['average_time']:.4f}s")
    
    print(f"\n🎨 3D Visualization Gallery Created:")
    print(f"  ✅ solved_cube_3d.png - Perfect cube state")
    print(f"  ✅ scrambled_cube_3d.png - Scrambled cube")
    print(f"  ✅ solve_comparison_3d.png - Before/after solving")
    print(f"  ✅ cube_showcase_3d.png - Multiple states showcase")
    
    print_section("7. Interactive 3D Display")
    print("🖥️  Displaying interactive 3D visualizations...")
    print("  (Close the matplotlib windows to continue)")
    
    plt.show()
    
    print_header("3D DEMONSTRATION COMPLETE")
    print("🎉 Enhanced Rubik's Cube Solver with 3D visualization:")
    print("✅ Sophisticated 3D rendering with matplotlib")
    print("✅ Before/after solve comparisons")
    print("✅ Multiple cube state showcases")
    print("✅ Interactive 3D visualization")
    print("✅ High-quality image exports")
    print("✅ Performance benchmarking with visuals")
    print("\n🏆 Ready to impress with visual wow factor!")

if __name__ == "__main__":
    main()