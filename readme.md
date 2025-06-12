# Image Processor

A Python script that converts a greyscale PNG input image into two binary bitmaps (stiff & soft materials) at precise DPIs.

## Features

- Detects near-black regions (stiff) and near-white regions (soft).
- Outputs 1-bit BMPs at two DPI settings (default: 63.5 and 31.75).
- Simple command-line interface powered by `argparse`.
- Uses `pathlib`, `fractions.Fraction`, `Pillow`, and `NumPy`.

## Requirements

- Python 3.7 or newer
- [Pillow](https://pypi.org/project/Pillow/)
- [NumPy](https://pypi.org/project/numpy/)

Install dependencies:

```bash
pip install Pillow numpy
```

## Installation & Setup

Before pushing or cloning, create an empty repository named `image-processor` under your GitHub account:  
https://github.com/travisbusbee/image-processor

1. **Clone the repository**

   ```bash
   git clone https://github.com/travisbusbee/image-processor.git
   cd image-processor
   ```

2. **Verify filenames**

   - Ensure your script is named `image_processor.py`.
   - If you accidentally committed it as `image_processor.py.py`, rename it:

     ```bash
     git mv image_processor.py.py image_processor.py
     git commit -m "Rename script to image_processor.py"
     ```

   - Ensure `README.md` (capital letters) is present at the project root.

## Usage

Run the script with an input image, an output folder, and optional DPI flags:

```bash
python image_processor.py \
  path/to/input.png \
  path/to/output_dir \
  --primary-dpi 63.5 \
  --secondary-dpi 31.75
```

- **`path/to/input.png`**: source image file.
- **`path/to/output_dir`**: directory where BMPs will be saved.
- DPI flags accept decimals or fractions (e.g., `127/2`).

This produces:

```
output_dir/mat_01_63.5.bmp
output_dir/mat_01_31.75.bmp
output_dir/mat_02_63.5.bmp
output_dir/mat_02_31.75.bmp
```

## Contributing

1. Fork this repo.
2. Create a new branch:

   ```bash
   git checkout -b feature/your-feature
   ```

3. Commit your changes:

   ```bash
   git commit -m "Add feature X"
   ```

4. Push to your fork:

   ```bash
   git push origin feature/your-feature
   ```

5. Open a Pull Request against `main`.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

