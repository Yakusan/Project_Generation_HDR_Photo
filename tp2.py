import cv2
import hdr
import utils

if __name__ == '__main__':
    images = utils.load_images_from_folder('aligned')

    shutterSpeed = [0.25, 0.5, 1., 2., 4.]
    log_shutterSpeed = utils.toLog(shutterSpeed)

    # Creation de l'image HDR
    finale_img_hdr, plot_g = hdr.LDR2HDR(images, log_shutterSpeed)

    # On affiche l'aspect graphique de la courbe G
    utils.plot_ResponseCurves(plot_g)

    cv2.imwrite('result/final_result.hdr', finale_img_hdr)

