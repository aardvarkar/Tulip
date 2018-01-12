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
 
def partitionnement1(root, working, tp1_s, tp2_s, tp3_s, tp4_s, tp5_s, tp6_s, tp7_s, tp8_s, tp9_s, tp10_s, tp11_s, tp12_s, tp13_s, tp14_s, tp15_s, tp16_s, tp17_s):
  graphPartition = graph.addCloneSubGraph("GraphPartition")
  for n in graphPartition.getNodes():
    print(n)
  for n in graphPartition.getEdges():
    graphPartition.delEdge(n)
  listOfNodes=[]
  for n in graphPartition.getNodes():
    listOfNodes.append(n)
  for n in range(len(listOfNodes)):
    for m in range(n+1,len(listOfNodes)):
      graphPartition.addEdge(listOfNodes[n], listOfNodes[m])
  poids = graphPartition.getDoubleProperty("Weight")
  expression_lvl=graphPartition.getDoubleProperty("Expression_lvl")
  for n in graphPartition.getNodes():
    expression_lvl[n] = (tp1_s[n] + tp2_s[n] + tp3_s[n] + tp4_s[n] + tp5_s[n] + tp6_s[n] + tp7_s[n] + tp8_s[n] + tp9_s[n] + tp10_s[n] + tp11_s[n] + tp12_s[n] + tp13_s[n] + tp14_s[n] + tp15_s[n] + tp16_s[n] + tp17_s[n])/17
  for n in graphPartition.getEdges():
    poids[n] = abs(expression_lvl[graphPartition.source(n)]-expression_lvl[graphPartition.target(n)])
    if poids[n] > 0.05 or expression_lvl[graphPartition.source(n)] == 0:
      graphPartition.delEdge(n)

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

  print(Locus)
  pretraitement(working, Locus, Negative, Positive, viewColor, viewLabel, viewLayout, viewSize)
  applyModelForce(working, viewLayout)
  partitionnement1(graph, working, tp1_s, tp2_s, tp3_s, tp4_s, tp5_s, tp6_s, tp7_s, tp8_s, tp9_s, tp10_s, tp11_s, tp12_s, tp13_s, tp14_s, tp15_s, tp16_s, tp17_s)
