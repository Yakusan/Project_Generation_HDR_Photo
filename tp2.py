import numpy as np
import cv2
import hdr
import utils
import sys

if __name__ == '__main__':
    nbArg       = len(sys.argv)
    imagesTypes = ('*.png', '*.jpg', '*.jpeg', '*.bmp')

    if(nbArg  < 7):
        print('Usage :')
        print('Programme <Dossier des images d\'entrée> '
              '<Nom du fichier de sortie (.hdr)> '
              'appliquer un ajustement d\'intensité avec l\'EV du milieu '
              '<tableau de temps d\'exposition par image>\n')

        print('Nombre d\'argument insuffisant (3 temps d\'exposition minimum')
        print('Exemple: <programme> myImagesDir myHDRImage 0 0.5 1 2')
        exit()

    shutterSpeed = [np.float64(sys.argv[i]) for i in range(4, nbArg)]

    images = utils.load_images_from_folder(sys.argv[1], imagesTypes)
    log_shutterSpeed = utils.toLog(shutterSpeed)

    if(log_shutterSpeed.shape[0] != len(images)):
        print('Error :')
        print('il doit y avoir autant de temps d\'exposition que d\'image d\'entrée')
        exit()

    # Creation de l'image HDR
    finale_img_hdr, plot_g = hdr.LDR2HDR(images, log_shutterSpeed, adjustementOpt=True if int(sys.argv[3]) == 1 else False)

    # On affiche l'aspect graphique de la courbe G
    utils.plot_ResponseCurves(plot_g)

    cv2.imwrite('result/' + sys.argv[2] + '.hdr', finale_img_hdr)

