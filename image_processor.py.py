
#!/usr/bin/env python3
"""
Image Processor Script
Processes an input image to generate two binary bitmaps (stiff and soft materials)
 at two specified DPIs, saving each as a 1-bit BMP.
"""
import argparse
import logging
from fractions import Fraction
from pathlib import Path

import numpy as np
from PIL import Image


class ImageProcessor:
    """
    Processes images to produce binary bitmaps for two material types
    at specified DPIs.
    """
    def __init__(
        self,
        primary_dpi: Fraction = Fraction('127/2'),
        secondary_dpi: Fraction = Fraction('635/20')
    ):
        self.primary_dpi = primary_dpi
        self.secondary_dpi = secondary_dpi

    def load_image(self, path: Path) -> Image.Image:
        """
        Load an image from disk and ensure it's in RGB mode.
        """
        if not path.exists():
            raise FileNotFoundError(f"Input file not found: {path}")
        img = Image.open(path)
        return img.convert('RGB')

    def process_first_bitmap(self, img: Image.Image) -> Image.Image:
        """
        Generate a bitmap for Material 1 (stiff):
        Black-ish pixels (<35) become white (255), others become black (0).
        """
        arr = np.array(img)
        mask = np.all(arr < 35, axis=2)
        out = np.zeros(arr.shape[:2], dtype=np.uint8)
        out[mask] = 255
        return Image.fromarray(out, mode='L')

    def process_second_bitmap(self, img: Image.Image) -> Image.Image:
        """
        Generate a bitmap for Material 2 (soft):
        White-ish pixels (>225) become white (255); black-ish (<30) become black (0).
        All other pixels (void) are black (0).
        """
        arr = np.array(img)
        mask_white = np.all(arr > 225, axis=2)
        out = np.zeros(arr.shape[:2], dtype=np.uint8)
        out[mask_white] = 255
        return Image.fromarray(out, mode='L')

    def save_bitmap(self, bitmap: Image.Image, path: Path, dpi: Fraction) -> None:
        """
        Save the bitmap as a 1-bit BMP file with specified DPI.
        """
        bitmap_1bit = bitmap.convert('1', dither=Image.NONE)
        dpi_val = float(dpi)
        # Ensure output directory exists
        path.parent.mkdir(parents=True, exist_ok=True)
        bitmap_1bit.save(path, format='BMP', dpi=(dpi_val, dpi_val))
        logging.info(f"Saved {path} at DPI {dpi_val}")

    def get_output_path(self, output_dir: Path, mat_num: int, dpi: Fraction) -> Path:
        """
        Construct an output filename based on material number and DPI (decimal).
        """
        # Use decimal representation for DPI in filename
        dpi_str = f"{float(dpi):.2f}".rstrip('0').rstrip('.')
        return output_dir / f"mat_{mat_num:02d}_{dpi_str}.bmp"


def main():
    parser = argparse.ArgumentParser(
        description="Process images into binary bitmaps with precise DPI control"
    )
    parser.add_argument(
        "input_file", type=Path, help="Path to input image"
    )
    parser.add_argument(
        "output_dir", type=Path, help="Directory to save output files"
    )
    parser.add_argument(
        "--primary-dpi",
        type=Fraction,
        default=Fraction('127/2'),
        help='Primary DPI (e.g., "127/2" for 63.5)'
    )
    parser.add_argument(
        "--secondary-dpi",
        type=Fraction,
        default=Fraction('635/20'),
        help='Secondary DPI (e.g., "635/20" for 31.75)'
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(message)s')

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    processor = ImageProcessor(
        primary_dpi=args.primary_dpi,
        secondary_dpi=args.secondary_dpi
    )
    image = processor.load_image(args.input_file)

    # Generate bitmaps for both materials
    bitmaps = {
        1: processor.process_first_bitmap(image),
        2: processor.process_second_bitmap(image),
    }

    # Save each bitmap at both DPIs
    for mat_num, bmp in bitmaps.items():
        for dpi in (processor.primary_dpi, processor.secondary_dpi):
            out_path = processor.get_output_path(output_dir, mat_num, dpi)
            processor.save_bitmap(bmp, out_path, dpi)


if __name__ == "__main__":
    main()