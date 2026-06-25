# JSON to Dataset — Annotation Visualizer

A Python script that batch-processes [LabelMe](https://github.com/wkentaro/labelme) JSON annotation files and renders the annotated shapes (linestrips, polygons, and vertices) on top of the original images. The resulting visualizations are saved as high-resolution PNG files.

## Features

- **Batch processing** — Automatically finds all `.json` files in the current directory and processes them one by one.
- **Annotation rendering** — Draws linestrips, polygons (closed-loop), and keypoints with configurable colors and sizes.
- **High-resolution output** — Exports 300 DPI PNG images with no borders or axes.
- **Auto-organized output** — All generated images are saved into an `output/` folder, keeping your working directory clean.

## Requirements

- Python 3.7+
- See [`requirements.txt`](./requirements.txt) for the full list of dependencies.

## Installation

```bash
# Clone or download the script, then install dependencies
pip install -r requirements.txt
```

## Usage

1. Place the script (`draw_vis.py`) in the same directory as your LabelMe JSON annotation files.
2. Make sure the original images referenced in the JSON files exist (or adjust the paths in the JSON).
3. Run the script:

```bash
python draw_vis.py
```

4. The rendered images will appear in the `output/` folder, each named after its corresponding JSON file (e.g., `image_001.json` → `output/image_001.png`).

## Configuration

You can tweak the visual appearance by modifying the constants at the top of `draw_vis.py`:

| Constant         | Default      | Description                         |
|------------------|--------------|-------------------------------------|
| `LINE_COLOR`     | `(0.5, 0, 0)` | RGB color of lines and nodes        |
| `OUTLINE_COLOR`  | `'black'`    | Outline color (reserved for future) |
| `LINE_WIDTH`     | `1`          | Stroke width of lines               |
| `NODE_RADIUS`    | `12`         | Size of vertex markers (`s` param)  |

## Output Format

- **Format**: PNG
- **DPI**: 300
- **Size**: Matches the original image dimensions
- **Background**: The original image (displayed in grayscale) with colored annotations overlaid

## License

This project is provided for educational and research purposes.
