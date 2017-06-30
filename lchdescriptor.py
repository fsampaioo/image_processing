import cv2
import numpy as np

class LCHDescriptor:
	def __init__(self, bins):
		#Numero de celulas que sera divido o histograma de cada canal
		self.bins = bins

	def describe(self, image):
		#Converte a imagem para HSV
		image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		
		features = []
		#Calculo centro da imagem
		(h, w) = image.shape[:2]
		(cX, cY) = (int(w * 0.5), int(h * 0.5))

		#Divido a imagem em quatro retangulos
		segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h), (0, cX, cY, h)]

		#Gero elipse no centro da imagem
		(axesX, axesY) = (int(w * 0.75) / 2, int(h * 0.75) / 2)
		ellipMask = np.zeros(image.shape[:2], dtype = "uint8")
		cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)

		#Extrai o histograma da mascara (retangulo - elipse)
		for (startX, endX, startY, endY) in segments:
			#Gera uma mascara
			cornerMask = np.zeros(image.shape[:2], dtype = "uint8")
			cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
			cornerMask = cv2.subtract(cornerMask, ellipMask)

			hist = self.histogram(image, cornerMask)
			features.extend(hist)

		#Extrai o histograma da elipse
		hist = self.histogram(image, ellipMask)
		features.extend(hist)

		return features

	def histogram(self, image, mask):
		#Extrai o histograma da imagem atraves da mascara dada e normaliza
		#OpenCV usa Hue como um valor entre 0 e 180, Saturation e Value entre 0 e 255
		hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins, [0, 180, 0, 256, 0, 256])
		hist = cv2.normalize(hist,hist).flatten()

		return hist
