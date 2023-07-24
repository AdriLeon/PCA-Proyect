import web
import numpy as np
from sklearn.decomposition import PCA
from PIL import Image
import matplotlib.pyplot as plt

urls = (
    '/', 'Index',
    '/upload', 'Upload'
)

app = web.application(urls, globals())

render = web.template.render('templates/')

class Index:
    def GET(self):
        return render.index()

class Upload:
    def POST(self):
        data = web.input(file={})
        if 'file' not in data:
            return "No se ha seleccionado ningún archivo"
        
        file = data.file
        if file.filename == '':
            return "No se ha seleccionado ningún archivo"
        
        img = Image.open(file.file)
        img = img.convert('L')  # Se convierte la imagen a escala de grises
        img_array = np.array(img) # Se convierte la imagen en una matriz dando una representacion numerica de los pixeles

        # PCA
        pca = PCA(n_components=2) # Se crea un objeto con dos componentes principales
        img_pca = pca.fit_transform(img_array) # fit_transform reduce la dimencionalidad de la imagen en los dos componentes puestos previamente

        # Crear el gráfico de dispersión
        plt.figure(figsize=(8, 6))
        plt.scatter(img_pca[:, 0], img_pca[:, 1]) # Los valores se usan como cordenadas para X e Y en el grafico
        plt.xlabel('Componente Principal 1')
        plt.ylabel('Componente Principal 2')
        plt.title('Gráfico de Dispersión PCA')
        plt.grid(True)

        # Guardar el gráfico en un archivo temporal
        temp_img_path = 'static/temp_plot.png' # Se guarda la grafica
        plt.savefig(temp_img_path)
        plt.close()

        return render.result(img_pca=img_pca.tolist()) # Se renderiza y se manda a la pagina de result.html las cordenadas en forma de lista

if __name__ == '__main__':
    app.run()
