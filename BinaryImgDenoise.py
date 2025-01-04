import cv2 as cv
import numpy as np
import maxflow
from multiprocessing.pool import ThreadPool
from scipy import ndimage

# FILTERS
k1 = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]]).astype(np.uint8)
k2 = np.array([[0, -1, 0], [-1, 3, 1], [0, -1, 0]]).astype(np.uint8)

# Median Blur
def remove_noise(image, ksize=3):
    return cv.medianBlur(image, ksize)

# Thresholding
def thresholding(image):
    return cv.threshold(image, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]

# Scaling
def scale_image(img, scale_percent=75):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv.resize(img, dim, interpolation=cv.INTER_AREA)

# Descaling
def descale_image(img, dim):
    return cv.resize(img, dim, interpolation=cv.INTER_AREA)

# Algorithm
def denoising_algorithm(img, ksize=3, scale_percent=75, smoothing=10):
    img = scale_image(img, scale_percent)
    
    g = maxflow.Graph[int]()
    nodeids = g.add_grid_nodes(img.shape)
    g.add_grid_edges(nodeids, smoothing)
    g.add_grid_tedges(nodeids, img, 255 - img)
    g.maxflow()
    sgm = g.get_grid_segments(nodeids)
    
    img_denoised = np.logical_not(sgm).astype(np.uint8) * 255
    
    morph = img_denoised
    morph = ndimage.convolve(morph, k1, mode='constant', cval=10.0)
    morph = remove_noise(morph, ksize=ksize)
    morph = ndimage.convolve(morph, k1, mode='constant', cval=10.0)
    _, morph = cv.threshold(morph, 127, 255, cv.THRESH_BINARY)
    
    return morph

if __name__ == '__main__':
    total_time = 0.0
    start_timer = 0.0
    end_timer = 0.0

    start_timer = cv.getTickCount()

    image_path = "grayscale1_noise.jpg"
    image_binary = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
    
    if image_binary is None:
        print(f"Error: Unable to load image from {image_path}")
    else:
        image_output = None

        pool = ThreadPool(processes=128)
        
        scale_percent = 40
        k_size = 3
        smoothing = 10

        async_result = pool.apply_async(denoising_algorithm, (image_binary, k_size, scale_percent, smoothing,))
        image_output = async_result.get()

        if image_output is not None:
            org_dim = (image_binary.shape[1], image_binary.shape[0])
            image_output = descale_image(image_output, org_dim)

            cv.imshow("Output", image_output)
            cv.waitKey(0)
            cv.destroyAllWindows()
        else:
            print("Error: The output image is None.")
            
        # if image_output is not None:
        #   cv.imwrite('output_image.png', image_output)
        #   print("Output image saved as 'output_image.png'")

        end_timer = cv.getTickCount()
        total_time = (end_timer - start_timer) * 1000 / cv.getTickFrequency()
        print(f'Time taken: {total_time:.4f} ms')
        
    

