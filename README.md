# JSON to DataSet Converter

## Overview
This script converts JSON annotation files (from labelme) into a structured dataset containing images, semantic segmentation masks, and visualization files. It processes single or batch JSON files and generates organized output directories with corresponding images and labels.

## Features
- Converts labelme JSON annotations to image datasets
- Supports both embedded image data (base64) and external image files
- Generates semantic segmentation masks
- Creates label visualization images
- Produces label name mappings
- Handles multiple JSON files in batch processing
- Compatible with both old and new versions of labelme

## Requirements
- Python 3.6+
- See `requirements.txt` for dependencies

## Installation

### 1. Clone or Download the Repository
```bash
git clone <repository_url>
cd Json_to_DataSet
```

### 2. Create a Virtual Environment (Recommended)
```bash
python -m venv .venv
```

### 3. Activate Virtual Environment
- **Windows (PowerShell):**
  ```bash
  .venv\Scripts\Activate.ps1
  ```
- **Windows (Command Prompt):**
  ```bash
  .venv\Scripts\activate.bat
  ```
- **Linux/macOS:**
  ```bash
  source .venv/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
Place your JSON files in a folder, then run:
```bash
python json_to_dataset.py <folder_path>
```

### With Custom Output Directory
```bash
python json_to_dataset.py <folder_path> -o <output_directory>
```

### Example
```bash
python json_to_dataset.py ./annotations -o ./output_dataset
```

## Input Format
- **Input:** A folder containing `.json` files exported from labelme
- **JSON Structure:** Each JSON file should contain:
  - `imageData`: Base64 encoded image (optional if `imagePath` is provided)
  - `imagePath`: Path to external image file (used if `imageData` is not present)
  - `shapes`: Array of annotation objects with labels and point coordinates

## Output Structure
For each JSON file, the script creates a directory with:
```
output_dir/
├── json_filename_/
│   ├── img.png                 # Original image
│   ├── label.png               # Semantic segmentation mask
│   ├── label_viz.png           # Visualization overlay (if available)
│   ├── label_names.txt         # Label mappings (one per line)
│   └── info.yaml               # Legacy format label configuration
```

## Output Files Description
- **img.png:** The original image extracted from the JSON annotation file
- **label.png:** Semantic segmentation mask where each pixel value corresponds to a label class
- **label_viz.png:** Colored visualization of the segmentation overlaid on the original image
- **label_names.txt:** Text file listing all unique label names (one per line)
- **info.yaml:** YAML configuration file containing label information

## Important Notes
⚠️ **Warning:** This script is designed to demonstrate single JSON file conversion and may require modifications for production use with large-scale datasets.

## Troubleshooting

### Issue: "ModuleNotFoundError" for labelme or other packages
- **Solution:** Ensure virtual environment is activated and all dependencies are installed via `pip install -r requirements.txt`

### Issue: Visualization image (label_viz.png) is not generated
- **Solution:** This can occur if the `imgviz` library has issues. The script includes fallback handling, and the segmentation mask will still be generated.

### Issue: AttributeError with labelme functions
- **Solution:** The script includes compatibility code for different versions of labelme. If issues persist, try updating: `pip install --upgrade labelme`

## Dependencies
- **Pillow:** Image processing
- **PyYAML:** YAML file handling
- **numpy:** Numerical operations
- **labelme:** Annotation utilities and format handling
- **imgviz:** Image visualization

## Author
Yijin Chen