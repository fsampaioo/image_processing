import cv2
import argparse
import glob
import time
import sys
from fourierdescriptor import FourierDescriptor
from gchdescriptor import GCHDescriptor
from lchdescriptor import LCHDescriptor

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
parser.add_argument("--method", required = True,
                    help = "Descriptor (must to be 'fourier', 'ghc' or 'lhc')")
parser.add_argument("--mask", required = False, default = 7, type = check_mask,
                    help = "Mask size to be use in Fourier (must to be 3 or 7). Default=7")
args = vars(parser.parse_args())

t1 = time.time()

#Verifica o metodo a ser usado e inicializa um objeto para o respectivo metodo
if(args["method"].upper() == "FOURIER"):
    print "Creating index to method FOURIER with mask %dx%d ..." % (args["mask"], args["mask"])
    descriptor = FourierDescriptor(args["mask"])
    indexFilepath = "indexes/" + str(args["mask"]) + "fourierindex.csv"
elif(args["method"].upper() == "GCH"):
    print "Creating index to method GCH ..."
    descriptor = GCHDescriptor((9, 12, 4))
    indexFilepath = "indexes/gchindex.csv"
elif(args["method"].upper() == "LCH"):
    print "Creating index to method LCH ..."
    descriptor = LCHDescriptor((9, 12, 3))
    indexFilepath = "indexes/lchindex.csv"
else:
    sys.exit("Invalid descriptor!")

#Cria o arquivo
indexFile = open(indexFilepath, "w")

#Atraves da funcao glob do modulo glob busca os nomes da imagens
for imagePath in glob.glob(args["images"] + "/*.jpg"):
    #Extrai o numero da imagem
    ini = imagePath.rfind("/") + 1
    end = imagePath.rfind(".")
    imageID = imagePath[ini:end]

    #Carrega a imagem em memoria
    image = cv2.imread(imagePath)
    if image is not None:
        #Aplico o descritor na imagem
        features = descriptor.describe(image)

        #Escrevo o vetor de caracterisicas no arquivo de indice (cada linha e' uma imagem)
        features = [str(f) for f in features]
        indexFile.write("%s, %s\n" % (imageID, ",".join(features)))

indexFile.close()

t2 = time.time()
print "Time: %.2f s" % (t2 - t1)

print "Index file created!"
