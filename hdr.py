import numpy as np
import random

# Fonction weight selon le papier "Recovering High Dynamic Range Radiance Maps from Photographs" de Paul E. Debevec et Jitendra Malik
def Debevec_weight(Z):
    Z_min = 0.
    Z_max = 255.

    if Z <= (Z_min + Z_max) / 2.:
        return Z - Z_min

    return Z_max - Z


# Fonction weight selon le papier "Ghost removal in high dynamic range images" de E. A. Khan, A. O. Akyz, et E. Reinhard
def hat_weight(Z):
    return 1.- pow(2. * (Z / 255.) - 1., 12.)


# Fonction d'echantillonage de pixel pour N images
def pixelIntensitiesSampling(images):
    Z_min = 0
    Z_max = 255

    num_val_range = (Z_max - Z_min) + 1
    num_images = len(images)
    Z_samples = np.zeros((num_val_range, num_images), dtype=np.uint8)

    # Image de reference EV0
    mid_img = images[num_images // 2]

    for i in range(Z_min, Z_max + 1):
        ligs, cols = np.where(mid_img == i)
        if len(ligs) != 0:
            idx = random.randrange(len(ligs))
            for j in range(num_images):
                Z_samples[i, j] = images[j][ligs[idx], cols[idx]]

    return Z_samples


# Recherche de la fonction inverse de reponse g selon le papier de P. Debevec et al 1997
def get_camera_response_function(Z_samples, log_shutterSpeed, smoothness_lambda, weight_func):
    Z_min = 0
    Z_max = 255

    # Nombre d'echantillon de pixel mesuré par image: N
    num_samples = Z_samples.shape[0]
    # Nombre d'images: P
    num_imgs = log_shutterSpeed.shape[0]
    # Nombre de Valeur possible
    num_val_range = (Z_max - Z_min) + 1

    A = np.zeros((num_imgs * num_samples + num_val_range - 1, num_val_range + num_samples), dtype=np.float64)
    b = np.zeros((A.shape[0], 1), dtype=np.float64)

    # Algorithme de mesure et d'ajustement des données
    k = 0
    for i in range(num_samples):
        for j in range(num_imgs):
            z_ij = Z_samples[i, j]
            w_ij = weight_func(z_ij)

            A[k, z_ij] = w_ij
            A[k, num_val_range + i] = -w_ij
            b[k, 0] = w_ij * log_shutterSpeed[j]
            k = k + 1

    # Correction de la courbe en initialisant à 0 le pixel du milieu
    A[k, (num_val_range - 1) // 2] = 0
    k = k + 1

    # Lissage de l'equation
    for i in range(Z_min + 1, Z_max):
        w_i = weight_func(i)
        A[k, i - 1] = smoothness_lambda * w_i
        A[k, i] = -2 * smoothness_lambda * w_i
        A[k, i + 1] = smoothness_lambda * w_i
        k = k + 1

    x = np.dot(np.linalg.pinv(A), b)
    g = x[0 : num_val_range]

    return g


# Construction de la carte de radiance selon le papier de P. Debevec et al 1997
def buildRadianceMap(images, g, log_shutterSpeed, weight_func):
    # Nombre total d'images
    num_images = len(images)
    # Dimension des images
    imgDim = images[0].shape
    # Creation d'une image HDR
    img_HDR = np.zeros(imgDim, dtype=np.float64)

    mid_img = num_images // 2

    # On creer la carte de radiance L puis on fusionne les images LDR
    for i in range(imgDim[0]):
        for j in range(imgDim[1]):
            wz = np.array([weight_func(images[r][i, j]) for r in range(num_images)])
            gz = np.array([g[images[r][i, j]] for r in range(num_images)])
            SumWZ = np.sum(wz)

            # On essaie d'eviter de divisier par 0
            if SumWZ > 0:
                img_HDR[i, j] = np.sum(wz * np.exp(gz - log_shutterSpeed)) / SumWZ
            else:
                img_HDR[i, j] = np.exp(gz[mid_img] - log_shutterSpeed[mid_img])

    return img_HDR

# Point d'entree
"""
    images            : Tableau contenant les N images
    log_shutterSpeed  : Logarithme néperien du temps d'exposition
    smoothness_lambda : Coefficient de lissage de la function g.
                        Sa valeur par défaut est recommandé dans l'article de P.Debevec
"""
def LDR2HDR(images, log_shutterSpeed, smoothness_lambda=100):
    num_channels = images[0].shape[2]
    hdr_image = np.zeros(images[0].shape, dtype=np.float64)

    plot_g = []
    for channel in range(num_channels):
        image_channel = [img[:, :, channel] for img in images]

        g = get_camera_response_function(pixelIntensitiesSampling(image_channel), log_shutterSpeed, smoothness_lambda, Debevec_weight)
        plot_g.append(g)

        hdr_image[:, :, channel] = buildRadianceMap(image_channel, g, log_shutterSpeed, hat_weight)

    return hdr_image, plot_g

