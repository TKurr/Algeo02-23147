import numpy as np
from PIL import Image
import os

def image_to_grayscale(image_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = img.load()
    width, height = img.size
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            grayscale = int(0.2989 * r + 0.5870 * g + 0.1140 * b) # I(x,y) = 0.2989⋅R(x,y) + 0.5870⋅G(x,y) + 0.1140⋅B(x,y)
            pixels[x, y] = (grayscale, grayscale, grayscale)
    return img

def resize_image(img, new_size=(128, 128)):
    width, height = img.size
    new_img = Image.new(img.mode, new_size) # Membuat gambar baru dengan ukuran yang diinginkan
    new_pixels = new_img.load() # Mengambil piksel gambar baru
    scale_x = new_size[0] / width # Menghitung faktor skala
    scale_y = new_size[1] / height
    for y in range(new_size[1]):
        for x in range(new_size[0]):
            original_x = int(x / scale_x) # Menghitung posisi piksel asli berdasarkan skala
            original_y = int(y / scale_y)
            original_pixel = img.getpixel((original_x, original_y))
            new_pixels[x, y] = original_pixel
    return new_img

def image_to_1d_vector(img):
    width, height = img.size
    pixels = img.load()
    vector = [pixels[x, y][0] for y in range(height) for x in range(width)] # Mengambil nilai r untuk setiap piksel (r, g, dan b pasti sama setelah grayscale)
    return vector

def image_standarization(directory_path, new_size=(128, 128)):
    image_vectors = []
    filenames = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if file_path.lower().endswith(('jpg', 'jpeg', 'png')): # Validasi extension file
            grayscale_img = image_to_grayscale(file_path)
            resized_img = resize_image(grayscale_img, new_size)
            image_vector = image_to_1d_vector(resized_img)
            image_vectors.append(image_vector)
            filenames.append(filename)
    num_images = len(image_vectors) # Validasi keberadaan file gambar
    if num_images == 0:
        # print("Tidak ada gambar yang ditemukan di direktori.") # Cek upload folder kosong
        return None, None, None, None
    image_vectors = np.array(image_vectors)
    pixel_average = np.zeros(image_vectors.shape[1]) # Inisialisasi array rata-rata pixel
    for i in range(image_vectors.shape[1]):
        total = 0
        for j in range(num_images):
            total += image_vectors[j, i]
        pixel_average[i] = total / num_images # Menghitung rata-rata pixel (μⱼ = (1/N) · (Σ[i=1 to N] (xᵢⱼ)))
    standardized_vectors = image_vectors - pixel_average # Standarisasi vektor (xᵢⱼ' = xᵢⱼ - μⱼ​)
    return standardized_vectors, filenames, pixel_average, new_size

def pca_computation(data, num_components):
    U, Sigma, Ut = np.linalg.svd(data, full_matrices=False) # Melakukan SVD pada data (C = (1 / N) · Xᵀ · X → C = UΣUᵀ)
    Ut_reduced = Ut[:num_components, :] # Mengambil n komponen utama dari Ut
    transformed_data = np.dot(data, Ut_reduced.T) # Proyeksi gambar ke komponen utama (Z = X'Uₖ)
    return transformed_data, Ut_reduced

def project_images_onto_pca(standardized_vectors, Ut_reduced, num_components):
    return np.dot(standardized_vectors, Ut_reduced.T)  # Memperbaiki perkalian matriks

def reconstruct_images_from_pca(projected_images, Ut_reduced): # Rekonstruksi gambar dari proyeksi PCA
    reconstructed_images = np.dot(projected_images, Ut_reduced)
    return reconstructed_images

def query_image_to_1d_vector(query_image_path, new_size=(128, 128)):
    grayscale_img = image_to_grayscale(query_image_path)
    resized_img = resize_image(grayscale_img, new_size)
    return image_to_1d_vector(resized_img)

def project_query_onto_pca(query_vector, pixel_average, Ut_reduced, num_components):
    standardized_query = query_vector - pixel_average
    return np.dot(standardized_query, Ut_reduced.T) # Proyeksi query (q = (q' - μ)Uₖ)

def euclidean_distance_computation(query_projection, dataset_projections):
    distances = [] # Inisialisasi array jarak Euclidean
    for projection in dataset_projections:
        distance = 0
        for i in range(len(query_projection)):
            distance += (query_projection[i] - projection[i]) ** 2
        distance = distance ** 0.5 # d(q, zᵢ) = sqrt(Σ[j=1 to k] ((qⱼ - zⱼ)²))
        distances.append(distance)
    return distances

def find_most_similar_images_manual(query_image_path, standardized_vectors, pixel_average, Ut_reduced, filenames, num_components):
    query_vector = query_image_to_1d_vector(query_image_path)
    query_projection = project_query_onto_pca(query_vector, pixel_average, Ut_reduced, num_components)
    dataset_projections = project_images_onto_pca(standardized_vectors, Ut_reduced, num_components)
    distances = euclidean_distance_computation(query_projection, dataset_projections)
    sorted_indices = sorted(range(len(distances)), key=lambda i: distances[i])
    results = [(filenames[idx], distances[idx]) for idx in sorted_indices]
    return results

def process_database():
    directory_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..",  "test", "dataset", "image_dataset"))
    directory_path = os.path.normpath(directory_path)
    standardized_vectors, filenames, pixel_average, new_size = image_standarization(directory_path)  # Standarisasi gambar
    num_images = standardized_vectors.shape[0]
    num_components = num_images 
    # print(f"Jumlah gambar yang ditemukan: {num_images}") # Cek jumlah gambar
    pca_result, Ut_reduced = pca_computation(standardized_vectors, num_components)
    # projected_images = project_images_onto_pca(standardized_vectors, Ut_reduced, num_components) # Cek proyeksi gambar ke ruang PCA
    # reconstructed_images = reconstruct_images_from_pca(projected_images, Ut_reduced) # Cek rekonstruksi gambar
    # for i, reconstructed_image in enumerate(reconstructed_images):
        # reconstructed_image_rgb = np.stack([reconstructed_image] * 3, axis=-1)
        # reconstructed_img = Image.fromarray(reconstructed_image_rgb.reshape(new_size[1], new_size[0], 3).astype(np.uint8))
        # reconstructed_img.save(f'reconstructed_{filenames[i]}')
        # print(f'Gambar {filenames[i]} telah direkonstruksi.')
    return standardized_vectors, filenames, pixel_average, Ut_reduced, num_components, new_size

def process_query(standardized_vectors, filenames, pixel_average, Ut_reduced, num_components, new_size, image_path):
    query_image_path = image_path
    query_image_path = os.path.normpath(query_image_path)
    if not os.path.exists(query_image_path):
        raise FileNotFoundError(f"Query image not found: {query_image_path}")
        # print("Tidak ada gambar query yang dipilih. Silakan pilih gambar query.") # Cek tidak ada query yang dipilih
    distances = find_most_similar_images_manual(query_image_path, standardized_vectors, pixel_average, Ut_reduced, filenames, num_components) # Menemukan gambar paling mirip
    return distances

def filter_similar_images(distances, filenames, threshold=9792):
    similar_images = []
    for i, distance in enumerate(distances):
        if distance < threshold: # Memfilter gambar dengan jarak < 9792 (kemiripan minimal 70%)
            similar_images.append(filenames[i])
    return similar_images

def process_image(image_path, threshold=9792):
    print("Starting database processing...")
    result = process_database()
    if result is None:
        print("No images found or an error occurred.")
        return []

    standardized_vectors, filenames, pixel_average, Ut_reduced, num_components, new_size = result
    print(f"Database processed successfully. {len(filenames)} images standardized.")

    print("Starting query process...")
    distances = process_query(
        standardized_vectors, filenames, pixel_average, Ut_reduced, num_components, new_size, image_path
    )

    # Extract filenames of similar images based on the threshold
    similar_images = filter_similar_images(
        [distance[1] for distance in distances], filenames, threshold
    )

    return similar_images