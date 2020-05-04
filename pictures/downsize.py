import glob
import os
import sys

import cv2 as cv

IMAGE_EXTENSIONS = ("jpg", "jpeg", "png")

def downsize_landscape(f, target, dims = (600, 400)):
    """Downsize and crop images for CoVoucher20 homepage."""

    assert f.lower().endswith(IMAGE_EXTENSIONS), "Problem with %s" % f

    img = cv.imread(f)
    img_height = img.shape[0]
    img_width = img.shape[1]

    target_width, target_height = dims
    
    # crop if needed
    aspect_ratio = img_width / img_height
    target_ratio = target_width / target_height

    if aspect_ratio > target_ratio:
        extra_pixels = int(img_width - img_height * target_width / target_height)
        left_pixels = int(extra_pixels / 2)
        right_pixels = extra_pixels - left_pixels
        img = img[:, left_pixels:(img_width - right_pixels), :]
    elif aspect_ratio < target_ratio:
        extra_pixels = int(img_height - img_width * target_height / target_width)
        top_pixels = int(extra_pixels / 2)
        bottom_pixels = extra_pixels - top_pixels
        img = img[top_pixels:(img_height - top_pixels), :, :]

    # Downsize
    downsized = cv.resize(img, (target_width, target_height), interpolation = cv.INTER_CUBIC)

    cv.imwrite(target, downsized)
    print("Prepared '%s'" % f)
        
def main():
    """Handle arguments and downsize images"""

    source_dir = sys.argv[1]
    target_dir = sys.argv[2]
    for f in glob.glob(os.path.join(source_dir, "*.*")):
        if f.lower().endswith(IMAGE_EXTENSIONS):
            
            target = os.path.join(target_dir, os.path.basename(f))
            downsize_landscape(f, target)
    
if "__main__" == __name__:
    main()
