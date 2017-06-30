import numpy as np 
import csv
import math
import sys

class Searcher:
	def __init__(self, indexPath):
		#Caminho para o indice 
		self.indexPath = indexPath

	def search(self, queryFeatures, limit, distance):
		#Inicializa o dicionario que contera os resultados seguindo a estrutura {imageID, score}
		#imageID = numero da imagem
		#score = quao similar a imageID e em relacao a query
		
		results = {}
		#Abre o arquivo com o indice
		with open(self.indexPath) as f:
			reader = csv.reader(f)
			#Percorre linhas
			for row in reader:
				features = [float(x) for x in row[1:]]
				#Calcula a similaridade entre uma imagem e a query dado metodo de distancia
				if distance.upper() == "CHI2":
					score = self.chi2_distance(features, queryFeatures)
				elif distance.upper() == "MANHATTAN": 
					score = self.manhattan_distance(features, queryFeatures)
				elif distance.upper() == "EUCLIDEAN":
					score = self.euclidean_distance(features, queryFeatures)
				else:
					sys.exit("Invalid Distance Method")

				results[row[0]] = score

			f.close()

		#Ordena os resultados em ordem decrescente ficando a imagem mais similar primeiro
		results = sorted([(v, k) for (k, v) in results.items()])
		return results[1:limit+1]


	def chi2_distance(self, histA, histB, eps = 1e-10):
		d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps) for (a, b) in zip(histA, histB)])

		return d

	def manhattan_distance(self, histA, histB):
		d = np.sum([abs((a - b)) for (a, b) in zip(histA, histB)])

		return d

	def euclidean_distance(self, histA, histB):
		d = math.sqrt(np.sum([(a - b) ** 2 for (a, b) in zip(histA, histB)]))

		return d


