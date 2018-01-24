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
#import scipy
#from scipy import stats
import random
import math

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
  params = tlp.getDefaultPluginParameters('FM^3 (OGDF)', graph)
  success = graph.applyLayoutAlgorithm('FM^3 (OGDF)', viewLayout, params)

# Partie 2

def createDistanceGraph(graph):
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
  calculPearson(distanceGraph, listOfNodes, total_tps)        
  '''
  for i in range(len(listOfNodes)):
    somme_i=0
    somme_i_carre=0
    Nb=len(total_tps)
    for k in range(Nb):
      value_k_of_i=total_tps[k][listOfNodes[i]]
      somme_i=somme_i+value_k_of_i
      somme_i_carre=somme_i_carre+math.pow(value_k_of_i,2)  
    for j in range(i+1,len(listOfNodes)):
      '''
  '''
      distance=0
      for k in range(len(total_tps)):
        distance=distance+math.pow(abs(total_tps[k][listOfNodes[i]]-total_tps[k][listOfNodes[j]]),2)        
      distance=math.sqrt(distance)
      '''
  '''
      distance=calculPearson(listOfNodes, i, value_k_of_i, somme_i, somme_i_carre, j, total_tps)
      if distance < 2:
        newEdge = distanceGraph.addEdge(listOfNodes[i], listOfNodes[j])
        poids[newEdge] = distance
        '''
  return distanceGraph

'''
def calculPearson(graph, listOfNodes, total_tps):
  poids = graph.getDoubleProperty("Weight")  
  Nb=len(total_tps)
  listTpsAll=[]
  for i in range(len(listOfNodes)):
    listTps_i=[]
    for k in range(Nb):
      listTps_i.append(total_tps[k][listOfNodes[i]])
    listTpsAll.append(listTps_i)
  for i in range(len(listOfNodes)):
    for j in range(i+1,len(listOfNodes)):
      pearson=scipy.stats.pearsonr(listTpsAll[i], listTpsAll[i])[0]
      if pearson > 0.9:
        newEdge = graph.addEdge(listOfNodes[i], listOfNodes[j])
        poids[newEdge] = pearson
'''


    
  
  

def calculPearson(graph, listOfNodes, total_tps):
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
      if r_value > 0.8:
      #if distance < 0.1:
        newEdge = graph.addEdge(listOfNodes[i], listOfNodes[j])
        poids[newEdge] = r_value
        #poids[newEdge] = distance
#  count=0
#  for n in graph.getNodes():
#    if graph.deg(n)==0:
#      count += 1
#  print(graph.numberOfNodes())
#  print(count)
  


'''
def partitionnement(graph,nbPartitionMax = 1, currentPartition = 0):
  if currentPartition == nbPartitionMax:
    return None
  params=tlp.getDefaultPluginParameters('MCL Clustering')
  params['weights'] = graph.getDoubleProperty("Weight")
  resultMetric = graph.getDoubleProperty('resultMetric' + str(currentPartition+1))
  success = graph.applyDoubleAlgorithm('MCL Clustering', resultMetric, params)
  params = tlp.getDefaultPluginParameters('Equal Value', graph)
  params['Property'] = resultMetric
  success = graph.applyAlgorithm('Equal Value', params)
  for sousGraph in graph.getSubGraphs():
    partitionnement(sousGraph, nbPartitionMax, currentPartition+1)
'''

def partitionnement(graph,nbPartitionMax = 1, currentPartition = 0):
  if currentPartition == nbPartitionMax:
    return None
    
  poids = graph.getDoubleProperty("Weight")
  min_lvl = poids.getEdgeDoubleMin()
  max_lvl = poids.getEdgeDoubleMax()
  for edge in graph.getEdges():
    poids[edge]=(poids[edge]-min_lvl)/(max_lvl-min_lvl)
    
  params=tlp.getDefaultPluginParameters('MCL Clustering')
  params['weights'] = graph.getDoubleProperty("Weight")
  resultMetric = graph.getDoubleProperty('resultMetric' + str(currentPartition+1))
  success = graph.applyDoubleAlgorithm('MCL Clustering', resultMetric, params)
  params = tlp.getDefaultPluginParameters('Equal Value', graph)
  params['Property'] = resultMetric
  success = graph.applyAlgorithm('Equal Value', params)
  for sousGraph in graph.getSubGraphs():
#    poids = sousGraph.getDoubleProperty("Weight")
#    min_lvl = poids.getEdgeDoubleMin()
#    max_lvl = poids.getEdgeDoubleMax()
#    for edge in sousGraph.getEdges():
#      poids[edge]=(poids[edge]-min_lvl)/(max_lvl-min_lvl)
  
    partitionnement(sousGraph, nbPartitionMax, currentPartition+1)
    
  
# Partie 3

def createHeatmap(graph, distanceGraph, timePoint):
  if graph.getSubGraph("heatmap") != None:
    heatmap = graph.getSubGraph("heatmap")
    graph.delSubGraph(heatmap)

  heatmap=graph.addCloneSubGraph("heatmap")
  heatmap.clear()
  tlp.copyToGraph(heatmap, distanceGraph)

  expression_lvl=heatmap.getDoubleProperty("Expression_lvl")
  tps=heatmap.getDoubleProperty("Tps")
  Locus = heatmap.getStringProperty("Locus")
  groupesHeatmap=heatmap.getDoubleProperty('resultMetric1')
  groupes=distanceGraph.getDoubleProperty('resultMetric1')
  for n in heatmap.getEdges():
    heatmap.delEdge(n)
  nodesListe=[]
  #for n in heatmap.getNodes():
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
  
'''
def construireGrille(gr):
    layout = gr.getLayoutProperty("viewLayout")
    tps = gr.getDoubleProperty("Tps")
    viewSize = gr.getSizeProperty("viewSize")
    decalageX = 100
    decalageY = 1.5
    nbTraites = 0
    Locus = gr.getStringProperty("Locus")
    locusToY = {}
    for n in gr.getNodes():
        currentLocus = Locus[n]
        viewSize[n]=tlp.Size(decalageX,decalageY,1)
        x = tps[n]
        y = nbTraites
        if currentLocus in locusToY :
          y = locusToY[currentLocus]
        else:
          nbTraites += 1
        locusToY[currentLocus] = y
       
        layout[n] = tlp.Coord(x * decalageX, y * decalageY, 0)
'''
        
'''
def construireGrille(distance, gr):
    increment = {}
    tmp = 0
    for graph in distance.getSubGraphs():
      resultMetric = graph.getDoubleProperty("resultMetric1")[graph.getOneNode()]
      increment[resultMetric] = tmp
      tmp += graph.numberOfNodes()
    
  
    layout = gr.getLayoutProperty("viewLayout")
    tps = gr.getDoubleProperty("Tps")
    groupes = gr.getDoubleProperty("resultMetric1")
    viewSize = gr.getSizeProperty("viewSize")
    decalageX = 100
    decalageY = 1.5
    Locus = gr.getStringProperty("Locus")
    locusToY = {}
    count = {}
    for n in gr.getNodes():
        currentLocus = Locus[n]
        viewSize[n]=tlp.Size(decalageX,decalageY,1)
        x = tps[n]
        if currentLocus in locusToY :
          y = locusToY[currentLocus]
        else:
          if groupes[n] not in count:
            count[groupes[n]] = 0
          y = increment[groupes[n]] + count[groupes[n]]
          count[groupes[n]] += 1
          locusToY[currentLocus] = y
       
        layout[n] = tlp.Coord(x * decalageX, y * decalageY, 0)
        
def getIncrement(gr):
  listeTmp = [0] * gr.numberOfSubGraphs()
  i = 0
  tmp = [0] * gr.numberOfSubGraphs()
  for graph in gr.getSubGraphs():
    resultMetric = graph.getDoubleProperty("resultMetric1")[graph.getOneNode()]
    listeTmp[int(resultMetric)] = graph.numberOfNodes()
    tmp[int(resultMetric)] = i
  liste = [0]
  for i in range(len(listeTmp)):
    liste.append(listeTmp[i] + liste[i])
  return liste
'''

def construireGrille(distance, gr):
    increment = getIncrement(distance, distance)
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
#        if currentLocus in locusToY :
#          y = locusToY[currentLocus]
#        else:
#          '''
#          print(int(groupes[n]))
#          print(tmp[int(groupes[n])])
#          print(increment[tmp[int(groupes[n])]])
#          '''
#          for node in distance.getNodes():
#            if Locus[node] == currentLocus:
#              y = positionY[node]
#          locusToY[currentLocus] = y
          
#          currentDepth = 1
#          groupe = gr.getDoubleProperty("resultMetric" + str(currentDepth))
#          tmp = increment[groupe[n]]
#          currentDepth += 1
#          groupe = gr.getDoubleProperty("resultMetric" + str(currentDepth))
#          tmp = tmp[groupe[n]]
#          currentDepth += 1
#          groupe = gr.getDoubleProperty("resultMetric" + str(currentDepth))
#          tmp[groupe[n]] += 1
#          y = tmp[groupe[n]]
##          print(y)
#          locusToY[currentLocus] = y
          
#          if groupes[n] not in count:
#              count[groupes[n]] = {}
#          branch = count[groupes[n]]
#          currentDepth = 2            
#          while currentDepth < maxDepth:
#            groupes = gr.getDoubleProperty("resultMetric" + str(currentDepth))
#            if groupes[n] not in branch:
#              branch[groupes[n]] = {}
#            branch = branch[groupes[n]]
#          
#          y = increment[groupes[n]] + count[groupes[n]]
#          count[groupes[n]] += 1
#          locusToY[currentLocus] = y
       
        
        
#def getIncrement(gr, depth = 1, tmp = 0):
#      
#    increment = {}
#    for graph in gr.getSubGraphs():
#      resultMetric = graph.getDoubleProperty("resultMetric"+ str(depth))[graph.getOneNode()]
#      tmp += graph.numberOfNodes()
#      if graph.numberOfSubGraphs() > 0:
#        increment[resultMetric] = getIncrement(graph, depth+1, tmp)
#      else:
#        increment[resultMetric] = tmp
#    return increment
    
def getIncrement(rootGraph, gr, tmp = 0):
#  print("**********************")

  
  for graph in gr.getSubGraphs():
    if graph.numberOfSubGraphs() == 0:
#      print("there are no subgraphs")
#      print("tmp = ", tmp)
#      print(graph.numberOfNodes())
      positionY = rootGraph.getDoubleProperty("PositionY")
      y = 0
      for n in graph.getNodes():
        positionY[n] = tmp + y
        y += 1
      tmp += graph.numberOfNodes()
    else:
#      print("there are subgraphs")
      tmp = getIncrement(rootGraph, graph, tmp)
  return tmp
      
  
  
#  if gr.numberOfSubGraphs() < 0:
#    return gr.numberOfNodes()
#  increment = {}
#  for graph in gr.getSubGraphs():
#    resultMetric = graph.getDoubleProperty("resultMetric"+ str(depth))[graph.getOneNode()]
#    t = rootGraph.getDoubleProperty("resultMetric"+ str(depth))
#    for n in graph.getNodes():
#      t[n] = resultMetric
#    tmp += getIncrement(rootGraph, graph, depth+1, tmp)
#    increment[resultMetric] = 
#    else:
#      increment[resultMetric] = tmp
#  return increment


#def changeGrille(graph):

# Partie 4

def trouverRegulateur(graph):
  regulators=[]
  for i in graph.getNodes():
    if graph.deg(i) > 50:
      regulators.append(i)
  return regulators
  
def trouverRegule(graph, distanceGraph, regulateurs):
  Locus = graph.getStringProperty("Locus")
  Cluster = distanceGraph.getDoubleProperty("resultMetric1")
  Negative = graph.getBooleanProperty("Negative")
  Positive = graph.getBooleanProperty("Positive")
  counterOfRegulateurs = 1
  for regulateur in regulateurs:
    genes_regules = []
    print("Genes regules pour " + Locus[regulateur] + " appartenant à " + str(Cluster[regulateur]))
    for node in graph.getInOutNodes(regulateur):
      edge = graph.existEdge(node, regulateur, directed=False)
#      if Positive[edge] == True and Negative[edge] == False:
      genes_regules.append(node)
    print(len(genes_regules))
    findCluster(distanceGraph, genes_regules)
    fileNames = open("input" + str(counterOfRegulateurs) + ".txt", "w")
    fileNames.write(Locus[regulateur] + "\n")
    for node in genes_regules:
      fileNames.write(Locus[node] + "\n")
    fileNames.close()
    counterOfRegulateurs += 1
  
      
    
  
def findCluster(graph, nodes):
  partition = graph.getDoubleProperty("resultMetric1")
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



# MAIN

def main(graph):
  working=graph.getSubGraph("Working")
  distanceGraph=working.getSubGraph("distanceGraph")
  #
#  if graph.getSubGraph("Clone") == None:
#    clone = graph.addCloneSubGraph("Clone")
#  else :
#    clone=graph.getSubGraph("Clone")
#  if graph.getSubGraph("Working") == None:
#    working = graph.addCloneSubGraph("Working")
#  else :
#    working=graph.getSubGraph("Working")
#    working.clear()
#    tlp.copyToGraph(working, clone)

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

  '''
  count=0
  for i in working.getNodes():
    count=count+1
    if count >100:
      working.delNode(i)
  '''


#  pretraitement(working, Locus, Negative, Positive, viewColor, viewLabel, viewLayout, viewSize)
#  applyModelForce(working, viewLayout)
#  distanceGraph = createDistanceGraph(working)
#  maxDepth = 3
#  partitionnement(distanceGraph, maxDepth)
#  heatmap = createHeatmap(working, distanceGraph, timePoint)
#  #heatmap = working.getSubGraph("heatmap")
#  colorHeatmap(heatmap)
#  construireGrille(distanceGraph, heatmap)
  clone=graph.getSubGraph("Clone")
  tmp=trouverRegulateur(clone)
  print(tmp)
  findCluster(distanceGraph, tmp)
  trouverRegule(clone, distanceGraph, tmp)
