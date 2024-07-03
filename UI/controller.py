import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []
        self.listWeightNodes = []

    def fillDD(self):
        years = self._model.getYears()
        yearsDD = []
        for y in years:
            yearsDD.append(ft.dropdown.Option(y))
        self._view.ddyear.options = yearsDD
        self._view.update_page()

    def getShapes(self, e):
        self._view.ddshape.options.clear()
        self._listShape = self._model.getShapes(self._view.ddyear.value)
        shapesDD = []
        for s in self._listShape:
            shapesDD.append(ft.dropdown.Option(s))
        self._view.ddshape.options.extend(shapesDD)
        self._view.update_page()

    def readYear(self, e):
        if e.control.data is None:
            self.year = None
        else:
            self.year = e.control.data
            self.getShapes()

    def handle_graph(self, e):
        self.listWeightNodes = []
        self._view.txt_result.controls.clear()
        self._view.update_page()
        year = self._view.ddyear.value
        shape = self. _view.ddshape.value
        if year is None:
            self._view.create_alert("Seleziona anno")
            return
        if shape is None:
            self._view.create_alert("Seleziona forma")
            return
        self._model.buildGraph(year, shape)
        for n in self._model.graph.nodes:
            self.listWeightNodes.append((n,self._model.sommaArchi(n)))
        self.listWeightNodes.sort(key=lambda x : x[0].id)
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {self._model.numNodes()} nodi e {self._model.numEdges()} archi"))
        for n in self.listWeightNodes:
            self._view.txt_result.controls.append(ft.Text(f"Nodo {n[0].id}, somma pesi su archi = {n[1]}"))
        self._view.update_page()
    def handle_path(self, e):
        self._view.txtOut2.controls.clear()
        self._model.calcola_Percorso()
        self._view.txtOut2.controls.append(ft.Text(f"Peso cammino massimo: {self._model.bestSol} km"))
        for i in range (0, len(self._model.bestPath)-1):
            self._view.txtOut2.controls.append(ft.Text(f"{self._model.bestPath[i].id} --> {self._model.bestPath[i+1].id}: weight {self._model.graph[self._model.bestPath[i]][self._model.bestPath[i+1]]['weight']} distance {self._model.distanza(self._model.bestPath[i],self._model.bestPath[i+1])}"))
        self._view.update_page()

    def handle_graph_tema_passato(self, e):
        xGiorni = 150
        try:
            intG = int(xGiorni)
        except:
            self._view.create_alert("Inserire un numero di giorni intero")
            return
        if intG < 1 or intG > 180:
            self._view.create_alert("Il valore deve essere compreso tra 1 e 180")
            return
        year = self._view.ddyear.value
        self._model.build_graph_tema_passato(year, intG)
        for n in self._model.graph.nodes:
            self.listWeightNodes.append((n,self._model.sommaArchi(n)))
        self.listWeightNodes.sort(key=lambda x : x[0].id)
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {self._model.numNodes()} nodi e {self._model.numEdges()} archi"))
        for n in self.listWeightNodes:
            self._view.txt_result.controls.append(ft.Text(f"Nodo {n[0].id}, somma pesi su archi = {n[1]}"))
        self._view.update_page()