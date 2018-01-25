# Powered by Python 2.7

# To cancel the modifications performed by the script
# on the current graph, click on the undo button.

# Some useful keyboards shortcuts :
#   * Ctrl + D : comment selected lines.
#   * Ctrl + Shift + D  : uncomment selected lines.
#   * Ctrl + I : indent selected lines.
#   * Ctrl + Shift + I  : unindent selected lines.
#   * Ctrl + Return  : run script.
#   * Ctrl + F  : find selected text.
#   * Ctrl + R  : replace selected text.
#   * Ctrl + Space  : show auto-completion dialog.

from tulip import tlp
import random
import math
import sys
import csv

# The updateVisualization(centerViews = True) function can be called
# during script execution to update the opened views

# The pauseScript() function can be called to pause the script execution.
# To resume the script execution, you will have to click on the "Run script " button.

# The runGraphScript(scriptFile, graph) function can be called to launch
# another edited script on a tlp.Graph object.
# The scriptFile parameter defines the script name to call (in the form [a-zA-Z0-9_]+.py)

# The main(graph) function must be defined
# to run the script on the current graph

# Partie 1

def pretraitement(graph, Locus, Negative, Positive, viewBorderColor, viewLabel, viewLayout, viewSize):
  '''
  Change la taille et la couleur des éléments du graphe afin qu'il soit plus lisible
  '''
  size = 1000
  for n in graph.getNodes():
    viewSize[n] = tlp.Size(10000,3000,10)
    viewLabel[n] = Locus[n]
  for n in graph.getEdges():
    if Negative[n] == True:
      if Positive[n] == True:
        viewBorderColor[n] = tlp.Color.Black
      else:
        viewBorderColor[n] = tlp.Color(0,0,225)
    elif Positive[n] == True:
      viewBorderColor[n] = tlp.Color(0,200,0)
      

def applyModelForce(graph, viewLayout):
  '''
  Modifie la visualisation du graphe selon un modèle de force
  '''
  params = tlp.getDefaultPluginParameters('FM^3 (OGDF)', graph)
  success = graph.applyLayoutAlgorithm('FM^3 (OGDF)', viewLayout, params)

# Partie 2

def createDistanceGraph(graph):
  '''
  Créé un sous graphe où les noeuds sont pondérés par la moyenne de leurs niveaux d'expression.
  Fait appel à la fonction computePearson sur ce nouveau graphe.
  '''
  if graph.getSubGraph("distanceGraph") != None:
    distanceGraph = graph.getSubGraph("distanceGraph")
    graph.delAllSubGraphs(distanceGraph)
  distanceGraph = graph.addCloneSubGraph("distanceGraph")
  
  poids = distanceGraph.getDoubleProperty("Weight")
  expression_lvl = distanceGraph.getDoubleProperty("Expression_lvl")
  tp1_s = distanceGraph.getDoubleProperty("tp1 s")
  tp10_s = distanceGraph.getDoubleProperty("tp10 s")
  tp11_s = distanceGraph.getDoubleProperty("tp11 s")
  tp12_s = distanceGraph.getDoubleProperty("tp12 s")
  tp13_s = distanceGraph.getDoubleProperty("tp13 s")
  tp14_s = distanceGraph.getDoubleProperty("tp14 s")
  tp15_s = distanceGraph.getDoubleProperty("tp15 s")
  tp16_s = distanceGraph.getDoubleProperty("tp16 s")
  tp17_s = distanceGraph.getDoubleProperty("tp17 s")
  tp2_s = distanceGraph.getDoubleProperty("tp2 s")
  tp3_s = distanceGraph.getDoubleProperty("tp3 s")
  tp4_s = distanceGraph.getDoubleProperty("tp4 s")
  tp5_s = distanceGraph.getDoubleProperty("tp5 s")
  tp6_s = distanceGraph.getDoubleProperty("tp6 s")
  tp7_s = distanceGraph.getDoubleProperty("tp7 s")
  tp8_s = distanceGraph.getDoubleProperty("tp8 s")
  tp9_s = distanceGraph.getDoubleProperty("tp9 s")
  total_tps=[tp1_s, tp2_s, tp3_s,  tp4_s,  tp5_s, tp6_s, tp7_s, tp8_s, tp9_s, tp10_s, tp11_s, tp12_s, tp13_s, tp14_s, tp15_s, tp16_s, tp17_s]
  
  for n in distanceGraph.getEdges():
    distanceGraph.delEdge(n)
  listOfNodes=[]
  for n in distanceGraph.getNodes():
    expression_lvl[n] = (tp1_s[n] + tp2_s[n] + tp3_s[n] + tp4_s[n] + tp5_s[n] + tp6_s[n] + tp7_s[n] + tp8_s[n] + tp9_s[n] + tp10_s[n] + tp11_s[n] + tp12_s[n] + tp13_s[n] + tp14_s[n] + tp15_s[n] + tp16_s[n] + tp17_s[n])/17
    if expression_lvl[n]==0:
      distanceGraph.delNode(n)
    else:
      listOfNodes.append(n)
  computePearson(distanceGraph, listOfNodes, total_tps)
  return distanceGraph


def computePearson(graph, listOfNodes, total_tps, threshold = 0.8):
  '''
  Calcule une similarité entre les noeuds selon le coefficient de Pearson.
  Ne garde que les similarités positives dont la valeur est supérieure à 0.8, et crée une arète entre les deux noeuds concernés.
  '''
  sommeListe=[]
  somme_carreListe=[]
  Nb=len(total_tps)
  poids = graph.getDoubleProperty("Weight")
  for i in range(len(listOfNodes)):
    somme_i=0
    somme_i_carre=0
    for k in range(Nb):
      value_k_of_i=total_tps[k][listOfNodes[i]]
      somme_i=somme_i+value_k_of_i
      somme_i_carre=somme_i_carre+math.pow(value_k_of_i,2)
    sommeListe.append(somme_i)
    somme_carreListe.append(somme_i_carre)
  for i in range(len(listOfNodes)):
    for j in range(i+1,len(listOfNodes)):
      somme_produit=0
      for k in range(Nb):
        value_k_of_i=total_tps[k][listOfNodes[i]]
        value_k_of_j=total_tps[k][listOfNodes[j]]
        somme_produit=somme_produit+(value_k_of_i*value_k_of_j)      
      denominator=math.sqrt((Nb*somme_carreListe[i]-math.pow(sommeListe[i],2)))*math.sqrt((Nb*somme_carreListe[j]-math.pow(sommeListe[j],2)))
      if denominator==0:
        r_value=0
      else:
        r_value=(Nb*somme_produit-sommeListe[i]*sommeListe[j])/denominator
      distance=1-r_value
      if r_value > threshold:
        newEdge = graph.addEdge(listOfNodes[i], listOfNodes[j])
        poids[newEdge] = r_value
  

def partitionnement(graph,nbPartitionMax = 1, currentPartition = 0):
  '''
  Crée un partitionnement multi-niveaux. Le nombre de niveaux est égal à nbPartitionMax.
  Le numéro du cluster pour un gène est indiqué dans la propriété 'cluster'. Le nombre suivant le nom de la propriété indique le niveau de profondeur du partitionnement.
  Par exemple, 'cluster1' correspond au premier niveau, 'cluster2' au deuxième niveau, etc...
  '''
  if currentPartition == nbPartitionMax:
    return None
    
  poids = graph.getDoubleProperty("Weight")
  min_lvl = poids.getEdgeDoubleMin()
  max_lvl = poids.getEdgeDoubleMax()
  for edge in graph.getEdges():
    poids[edge]=(poids[edge]-min_lvl)/(max_lvl-min_lvl)
    
  params=tlp.getDefaultPluginParameters('MCL Clustering')
  params['weights'] = graph.getDoubleProperty("Weight")
  cluster = graph.getDoubleProperty('cluster' + str(currentPartition+1))
  success = graph.applyDoubleAlgorithm('MCL Clustering', cluster, params)
  params = tlp.getDefaultPluginParameters('Equal Value', graph)
  params['Property'] = cluster
  success = graph.applyAlgorithm('Equal Value', params)
  for sousGraph in graph.getSubGraphs():  
    partitionnement(sousGraph, nbPartitionMax, currentPartition+1)
    
  
# Partie 3

def createHeatmap(graph, distanceGraph, timePoint):
  '''
  Crée une Heatmap en fonction des niveaux d'expression des gènes.
  Dans ce sous-graphe, chaque gène est présent en 17 exemplaire, un par pas de temps.
  '''
  if graph.getSubGraph("heatmap") != None:
    heatmap = graph.getSubGraph("heatmap")
    graph.delSubGraph(heatmap)

  heatmap=graph.addCloneSubGraph("heatmap")
  heatmap.clear()
  tlp.copyToGraph(heatmap, distanceGraph)

  expression_lvl=heatmap.getDoubleProperty("Expression_lvl")
  tps=heatmap.getDoubleProperty("Tps")
  Locus = heatmap.getStringProperty("Locus")
  groupesHeatmap=heatmap.getDoubleProperty('cluster1')
  groupes=distanceGraph.getDoubleProperty('cluster1')
  for n in heatmap.getEdges():
    heatmap.delEdge(n)
  nodesListe=[]
  count=0
  for n in heatmap.getNodes():
    count=count+1
    nodesListe.append(n)
  for n in nodesListe:
    expression_lvl[n]=timePoint[0][n]
    tps[n]=1
    addedNodes = heatmap.addNodes(17)
    tps=heatmap.getDoubleProperty("Tps")
    for m in range(len(addedNodes)):
      expression_lvl[addedNodes[m]]=timePoint[m][n]
      tps[addedNodes[m]]=m+1
      Locus[addedNodes[m]]=Locus[n]
      groupesHeatmap[addedNodes[m]]= groupesHeatmap[n]
  for n in nodesListe:
    heatmap.delNode(n)
  return heatmap
   
def colorHeatmap(graph):
  '''
  Colore la Heatmap en fonction de l'expression du gène. Les couleurs vont de jaune (faible expression) à rouge (forte expression)
  '''
  viewBorderColor = graph.getColorProperty("viewBorderColor")
  viewColor = graph.getColorProperty("viewColor")
  expression_lvl=graph.getDoubleProperty("Expression_lvl")
  min_lvl = expression_lvl.getNodeDoubleMin()
  max_lvl = expression_lvl.getNodeDoubleMax()
  colorScale = tlp.ColorScale([])
  colors = [tlp.Color.Yellow, tlp.Color.Red]
  colorScale.setColorScale(colors)
  for n in graph.getNodes():
    viewColor[n]=colorScale.getColorAtPos((expression_lvl[n]-min_lvl)/(max_lvl-min_lvl))
    viewBorderColor[n]=viewColor[n]

def construireGrille(distance, gr):
  '''
  Crée une grille où les gènes sont présents en ordonnée, et en abscisse les valeurs d'expression pour un gène.
  Les gènes sont ordonnés en fonction du partitionnement du graphe, quelque soit le niveau.
  '''
  computeY(distance)
  positionY = distance.getDoubleProperty("PositionY")

  layout = gr.getLayoutProperty("viewLayout")
  tps = gr.getDoubleProperty("Tps")
  viewSize = gr.getSizeProperty("viewSize")
  decalageX = 100
  decalageY = 1.5
  Locus = distance.getStringProperty("Locus")
  locusToY = {}
  for node in distance.getNodes():
    locusToY[Locus[node]] = positionY[node]
  Locus = gr.getStringProperty("Locus")
  count = {}
  for n in gr.getNodes():
      currentLocus = Locus[n]
      viewSize[n]=tlp.Size(decalageX,decalageY,1)
      x = tps[n]
      y = locusToY[Locus[n]]
      layout[n] = tlp.Coord(x * decalageX, y * decalageY, 0)

    
def computeY(rootGraph, gr = None, tmp = 0):
  '''
  Calcule la position Y de chaque gène pour les agencer sur une grille en fonction de leur partitionnement.
  Au sein d'un graphe, les gènes sont ordonnés par sous-graphe dans l'ordre dans lequel l'itérateur les renvoi.
  Prend en compte n'importe quel niveau de partitionnement.
  '''
  if gr == None:
    gr = rootGraph
  
  for graph in gr.getSubGraphs():
    if graph.numberOfSubGraphs() == 0:
      positionY = rootGraph.getDoubleProperty("PositionY")
      y = 0
      for n in graph.getNodes():
        positionY[n] = tmp + y
        y += 1
      tmp += graph.numberOfNodes()
    else:
      tmp = computeY(rootGraph, graph, tmp)
  return tmp
      


# Partie 4

def trouverRegulateur(graph, threshold = 50):
  '''
  Retourne une liste de gènes qui ont un degré dans le graph supérieur au threshold.
  '''
  regulators=[]
  for i in graph.getNodes():
    if graph.deg(i) > threshold:
      regulators.append(i)
  return regulators
  
def trouverRegule(graph, regulateurs):
  '''
  Pour chaque régulateur, trouve la liste des gènes régulés positivement ou négativement et sauvegarde la liste dans un fichier
  '''
  
  Locus = graph.getStringProperty("Locus")
  
  counterOfRegulateurs = 1

  for regulateur in regulateurs:   
    fileName = open("input" + str(counterOfRegulateurs) + ".txt", "w")
    for node in graph.getInOutNodes(regulateur):
      fileName.write(Locus[node] + "\n")   
    fileName.close()
    counterOfRegulateurs += 1

  
  
def findCluster(graph, nodes):
  '''
  Pour une liste de gènes, indique combien de gènes se retrouve dans quels clusters.
  Seuls les clusters avec au moins un gène présent sont indiqués.
  Les gènes dont le niveau d'expression est nul ne sont pas pris en compte.
  '''
  partition = graph.getDoubleProperty("cluster1")
  clusters = {}
  for n in nodes:
    try:
      cluster = partition[n]
      if cluster in clusters:
        clusters[cluster] += 1
      else:
        clusters[cluster] = 1
    except:
      pass
      #print("Node " + str(n) + " has a null expression level")
  for key in clusters.keys():
    print("Nodes at cluster " + str(key) + " : " + str(clusters[key]))
    
    
def saveClusters(graph, clusterNumber):
  '''
  clusterNumber est le numéro du cluster pour lequel on souhaite enregistrer les gènes.
  Cette fonction récupère tous les gènes appartenant au cluster et enregistre leurs noms dans un fichier appelé genesCluster + numéro du cluster
  '''
  Locus = graph.getStringProperty("Locus")
  f = open("genesCluster" + str(clusterNumber) + ".txt", "w")
  partition = graph.getDoubleProperty("cluster1")
  for node in graph.getNodes():
    if partition[node] == clusterNumber:
      f.write(Locus[node] + "\n")
  f.close()
  


# MAIN

def main(graph):
  #

  if graph.getSubGraph("Clone") == None:
    clone = graph.addCloneSubGraph("Clone")
  else :
    clone=graph.getSubGraph("Clone")
  
  if graph.getSubGraph("Working") == None:
    working = graph.addCloneSubGraph("Working")
  else :
    working=graph.getSubGraph("Working")
    working.clear()           #A commenter si le projet est déjà chargé et l'on souhaite éviter de tout relancer
    tlp.copyToGraph(working, clone)       #A commenter si le projet est déjà chargé et l'on souhaite éviter de tout relancer

  Locus = working.getStringProperty("Locus")
  Negative = working.getBooleanProperty("Negative")
  Positive = working.getBooleanProperty("Positive")
  tp1_s = working.getDoubleProperty("tp1 s")
  tp10_s = working.getDoubleProperty("tp10 s")
  tp11_s = working.getDoubleProperty("tp11 s")
  tp12_s = working.getDoubleProperty("tp12 s")
  tp13_s = working.getDoubleProperty("tp13 s")
  tp14_s = working.getDoubleProperty("tp14 s")
  tp15_s = working.getDoubleProperty("tp15 s")
  tp16_s = working.getDoubleProperty("tp16 s")
  tp17_s = working.getDoubleProperty("tp17 s")
  tp2_s = working.getDoubleProperty("tp2 s")
  tp3_s = working.getDoubleProperty("tp3 s")
  tp4_s = working.getDoubleProperty("tp4 s")
  tp5_s = working.getDoubleProperty("tp5 s")
  tp6_s = working.getDoubleProperty("tp6 s")
  tp7_s = working.getDoubleProperty("tp7 s")
  tp8_s = working.getDoubleProperty("tp8 s")
  tp9_s = working.getDoubleProperty("tp9 s")
  viewBorderColor = working.getColorProperty("viewBorderColor")
  viewBorderWidth = working.getDoubleProperty("viewBorderWidth")
  viewColor = working.getColorProperty("viewColor")
  viewFont = working.getStringProperty("viewFont")
  viewFontSize = working.getIntegerProperty("viewFontSize")
  viewIcon = working.getStringProperty("viewIcon")
  viewLabel = working.getStringProperty("viewLabel")
  viewLabelBorderColor = working.getColorProperty("viewLabelBorderColor")
  viewLabelBorderWidth = working.getDoubleProperty("viewLabelBorderWidth")
  viewLabelColor = working.getColorProperty("viewLabelColor")
  viewLabelPosition = working.getIntegerProperty("viewLabelPosition")
  viewLayout = working.getLayoutProperty("viewLayout")
  viewMetric = working.getDoubleProperty("viewMetric")
  viewRotation = working.getDoubleProperty("viewRotation")
  viewSelection = working.getBooleanProperty("viewSelection")
  viewShape = working.getIntegerProperty("viewShape")
  viewSize = working.getSizeProperty("viewSize")
  viewSrcAnchorShape = working.getIntegerProperty("viewSrcAnchorShape")
  viewSrcAnchorSize = working.getSizeProperty("viewSrcAnchorSize")
  viewTexture = working.getStringProperty("viewTexture")
  viewTgtAnchorShape = working.getIntegerProperty("viewTgtAnchorShape")
  viewTgtAnchorSize = working.getSizeProperty("viewTgtAnchorSize")
  timePoint = [tp1_s, tp2_s, tp3_s, tp4_s, tp5_s, tp6_s, tp7_s, tp8_s, tp9_s, tp10_s, tp11_s, tp12_s, tp13_s, tp14_s, tp15_s, tp16_s, tp17_s]


  pretraitement(working, Locus, Negative, Positive, viewColor, viewLabel, viewLayout, viewSize)
  applyModelForce(working, viewLayout)
  distanceGraph = createDistanceGraph(working)
  maxDepth = 3
  partitionnement(distanceGraph, maxDepth)
  heatmap = createHeatmap(working, distanceGraph, timePoint)
  #heatmap = working.getSubGraph("heatmap")
  colorHeatmap(heatmap)
  construireGrille(distanceGraph, heatmap)
  #clone=graph.getSubGraph("Clone")
  regulateurs=trouverRegulateur(clone)
  trouverRegule(clone, regulateurs)
  saveClusters(distanceGraph, 0.0)
  saveClusters(distanceGraph, 1.0)
