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
    x = random.random() * size
    y = random.random() * size
    viewLayout[n] = tlp.Coord(x, y, 0)
    viewSize[n] = tlp.Size(10,3,10)
    viewLabel[n] = Locus[n]
  for n in graph.getEdges():
    if Negative[n] == True:
      if Positive[n] == True:
        viewBorderColor[n] = tlp.Color.Blue
      else:
        viewBorderColor[n] = tlp.Color.Green
    elif Positive[n] == True:
      viewBorderColor[n] = tlp.Color.Red
    else:
      viewBorderColor[n] = tlp.Color.Violet

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
  
  for n in distanceGraph.getEdges():
    distanceGraph.delEdge(n)
  listOfNodes=[]
  for n in distanceGraph.getNodes():
    listOfNodes.append(n)
    expression_lvl[n] = (tp1_s[n] + tp2_s[n] + tp3_s[n] + tp4_s[n] + tp5_s[n] + tp6_s[n] + tp7_s[n] + tp8_s[n] + tp9_s[n] + tp10_s[n] + tp11_s[n] + tp12_s[n] + tp13_s[n] + tp14_s[n] + tp15_s[n] + tp16_s[n] + tp17_s[n])/17
  for i in range(len(listOfNodes)):
    for j in range(i+1,len(listOfNodes)):
      distance = abs(expression_lvl[listOfNodes[i]]-expression_lvl[listOfNodes[j]])
      if distance < 0.05 and expression_lvl[listOfNodes[i]] != 0:
        newEdge = distanceGraph.addEdge(listOfNodes[i], listOfNodes[j])
        poids[newEdge] = distance
  return distanceGraph
   
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
  
  
# Partie 3

def createHeatmap(graph, distanceGraph, timePoint):
  if graph.getSubGraph("heatmap") != None:
    heatmap = graph.getSubGraph("heatmap")
    graph.delSubGraph(heatmap)

  heatmap=graph.addCloneSubGraph("heatmap")
  expression_lvl=heatmap.getDoubleProperty("Expression_lvl")
  tps=heatmap.getDoubleProperty("Tps")
  Locus = heatmap.getStringProperty("Locus")
  groupesHeatmap=heatmap.getDoubleProperty('resultMetric1')
  groupes=distanceGraph.getDoubleProperty('resultMetric1')
  for n in heatmap.getEdges():
    heatmap.delEdge(n)
  nodesListe=[]
  for n in heatmap.getNodes():
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
      groupesHeatmap[addedNodes[m]]= groupes[n]
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
  colors = [tlp.Color.Blue, tlp.Color.Red]
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
          '''
          print(int(groupes[n]))
          print(tmp[int(groupes[n])])
          print(increment[tmp[int(groupes[n])]])
          '''
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


#def changeGrille(graph):
  

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
    working.clear()
    tlp.copyToGraph(working, clone)

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
  partitionnement(distanceGraph, 2)
  heatmap = createHeatmap(working, distanceGraph, timePoint)
  #heatmap = working.getSubGraph("heatmap")
  colorHeatmap(heatmap)
  construireGrille(distanceGraph, heatmap)
