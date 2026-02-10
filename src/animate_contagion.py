#!/usr/bin/env python3
"""
Animate contagion spread graphs from experiment runs.

This script creates animated GIFs from the graph images generated during
contagion spread experiments. It can process individual runs or entire experiments.
"""

import argparse
from pathlib import Path
from PIL import Image
import re


def get_sorted_images(image_dir: Path) -> list[Path]:
    """
    Get all PNG images from a directory, sorted numerically by filename.

    Args:
        image_dir: Path to directory containing numbered PNG images

    Returns:
        List of image paths sorted by their numeric value
    """
    images = list(image_dir.glob("*.png"))

    # Sort by numeric value extracted from filename
    def get_number(path: Path) -> int:
        match = re.search(r'(\d+)', path.stem)
        return int(match.group(1)) if match else 0

    return sorted(images, key=get_number)


def create_animation(image_paths: list[Path], output_path: Path, duration: int = 100, loop: int = 0):
    """
    Create an animated GIF from a sequence of images.

    Args:
        image_paths: List of paths to images in the desired order
        output_path: Path where the animated GIF should be saved
        duration: Duration of each frame in milliseconds (default: 100ms)
        loop: Number of times to loop (0 = infinite, default: 0)
    """
    if not image_paths:
        print(f"No images found for {output_path}")
        return

    # Load all images
    frames = [Image.open(img) for img in image_paths]

    # Save as animated GIF
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=loop,
        optimize=False
    )

    print(f"Created animation: {output_path} ({len(frames)} frames)")


def animate_run(run_dir: Path, output_dir: Path, duration: int = 100):
    """
    Create animation for a single run.

    Args:
        run_dir: Path to run directory (e.g., out/experiment/run_0)
        output_dir: Path to output directory for animations
        duration: Frame duration in milliseconds
    """
    graph_images_dir = run_dir / "graph_images"

    if not graph_images_dir.exists():
        print(f"No graph_images directory found in {run_dir}")
        return

    image_paths = get_sorted_images(graph_images_dir)

    if not image_paths:
        print(f"No images found in {graph_images_dir}")
        return

    # Create output filename: experiment_name_run_X.gif
    experiment_name = run_dir.parent.name
    run_name = run_dir.name
    output_filename = f"{experiment_name}_{run_name}.gif"
    output_path = output_dir / output_filename

    create_animation(image_paths, output_path, duration)


def animate_experiment(experiment_dir: Path, output_dir: Path, duration: int = 100):
    """
    Create animations for all runs in an experiment.

    Args:
        experiment_dir: Path to experiment directory (e.g., out/experiment)
        output_dir: Path to output directory for animations
        duration: Frame duration in milliseconds
    """
    run_dirs = sorted([d for d in experiment_dir.iterdir() if d.is_dir() and d.name.startswith("run_")])

    if not run_dirs:
        print(f"No run directories found in {experiment_dir}")
        return

    print(f"Processing experiment: {experiment_dir.name}")
    for run_dir in run_dirs:
        animate_run(run_dir, output_dir, duration)


def animate_all(out_dir: Path, output_dir: Path, duration: int = 100):
    """
    Create animations for all experiments in the out directory.

    Args:
        out_dir: Path to out directory containing all experiments
        output_dir: Path to output directory for animations
        duration: Frame duration in milliseconds
    """
    experiment_dirs = sorted([d for d in out_dir.iterdir() if d.is_dir()])

    if not experiment_dirs:
        print(f"No experiment directories found in {out_dir}")
        return

    for experiment_dir in experiment_dirs:
        output_dir = output_dir / experiment_dir.name
        animate_experiment(experiment_dir, output_dir, duration)


def main():
    parser = argparse.ArgumentParser(
        description="Create animated GIFs from contagion spread graph images"
    )

    parser.add_argument(
        "--experiment",
        "-e",
        type=str,
        help="Name of specific experiment to animate (e.g., 'infect_dublin')"
    )

    parser.add_argument(
        "--run",
        "-r",
        type=int,
        help="Specific run number to animate (requires --experiment)"
    )

    parser.add_argument(
        "--out-dir",
        type=str,
        default="out",
        help="Directory containing experiment outputs (default: 'out')"
    )

    parser.add_argument(
        "--output-dir",
        "-o",
        type=str,
        default="animations",
        help="Directory to save animations (default: 'animations')"
    )

    parser.add_argument(
        "--duration",
        "-d",
        type=int,
        default=100,
        help="Frame duration in milliseconds (default: 100)"
    )

    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    output_dir = Path(args.output_dir + "/" + args.experiment)

    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)

    if args.run is not None:
        if not args.experiment:
            parser.error("--run requires --experiment to be specified")

        run_dir = out_dir / args.experiment / f"run_{args.run}"
        if not run_dir.exists():
            print(f"Error: Run directory not found: {run_dir}")
            return

        animate_run(run_dir, output_dir, args.duration)

    elif args.experiment:
        experiment_dir = out_dir / args.experiment
        if not experiment_dir.exists():
            print(f"Error: Experiment directory not found: {experiment_dir}")
            return

        animate_experiment(experiment_dir, output_dir, args.duration)

    else:
        # Animate all experiments
        animate_all(out_dir, output_dir, args.duration)

    print(f"\nAnimations saved to: {output_dir.absolute()}")


if __name__ == "__main__":
    main()
