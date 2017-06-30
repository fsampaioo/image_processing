import cv2
import argparse
import time
import sys
from fourierdescriptor import FourierDescriptor
from gchdescriptor import GCHDescriptor
from lchdescriptor import LCHDescriptor
from searcher import Searcher

def check_mask(value):
    ivalue = int(value)
	#Verifica se a mascara usada em Fourier tem um valor correto
    if ivalue != 3 and ivalue != 7:
        raise argparse.ArgumentTypeError("Mask size must to be 3 or 7")
    return ivalue

##############################################################################

#Le os argumentos
parser = argparse.ArgumentParser()
parser.add_argument("--images", required = True,
				help = "Directory of data base images")
parser.add_argument("-q", "--query", required = True,
				help = "Path and image that you want to search similiars")
parser.add_argument("-n", "--limit", required = True,
				help = "Number of similar images")
parser.add_argument("-m", "--method", required = True,
				help = "Descriptor (must to be 'fourier', 'ghc' or 'lhc')")
parser.add_argument("--mask", required = False, default = 7, type = check_mask,
                help = "Mask size to be use in Fourier (must to be 3 or 7). Default=7")
parser.add_argument("-d", "--distance", required = True,
				help = "Distance to compere the histrograms. Must to be 'chi2', 'manhattan' or 'euclidean'")
args = vars(parser.parse_args())

t1 = time.time()

#Define o descriptor a ser utilizado e seleciona o respectivo arquivo de indice para comparar
if(args["method"].upper() == "FOURIER"):
	queryDesc = FourierDescriptor(args["mask"])
	indexFilepath = "indexes/" + str(args["mask"]) + "fourierindex.csv"
elif(args["method"].upper() == "GCH"):
	queryDesc = GCHDescriptor((9, 12, 4))
	indexFilepath = "indexes/gchindex.csv"
elif(args["method"].upper() == "LCH"):
	queryDesc = LCHDescriptor((9, 12, 3))
	indexFilepath = "indexes/lchindex.csv"
else:
	sys.exit("Invalid descriptor!")

#Carrega a imagem de consulta em memoria e aplica o descritor
query = cv2.imread(args["query"])
queryFeatures = queryDesc.describe(query)

#Inicializa um objeto que ira fazer a comparacao da imagem de consulta com o banco de imagens
searcher = Searcher(indexFilepath)
#Realiza a consulta das n-imagens mais semelhantes 
results = searcher.search(queryFeatures, int(args["limit"]), args["distance"])

t2 = time.time()
print "Time: %.2f s" % (t2 - t1)

#Exibo imagem query
r = 800.0 / query.shape[1]
dim = (800, int(query.shape[0] * r))
resized = cv2.resize(query, dim, interpolation = cv2.INTER_AREA)
cv2.imshow("Query", resized)
cv2.waitKey(0)

#Exibo as imagens semelhantes a partir do id
for (score, resultID) in results:

	result = cv2.imread("images/"+resultID+".jpg")
	r = 800.0 / result.shape[1]
	dim = (800, int(result.shape[0] * r))
	resized = cv2.resize(result, dim, interpolation = cv2.INTER_AREA)
	cv2.imshow("Result", resized)
	cv2.waitKey(0)

