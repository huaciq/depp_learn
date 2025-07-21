from graphviz import Digraph

dot = Digraph(comment='YOLOv8m 改进结构')

# Backbone
dot.attr(rankdir='LR', size='10')
dot.node('0', 'Focus\n[64,3]')
dot.node('1', 'Conv\n[128,3,2]')
dot.node('2', 'C3STR x3\n[128]')
dot.node('3', 'Conv\n[256,3,2]')
dot.node('4', 'C3STR x6\n[256]')
dot.node('5', 'Conv\n[512,3,2]')
dot.node('6', 'C3STR x6\n[512]')
dot.node('7', 'Conv\n[768,3,2]')
dot.node('8', 'C3STR x3\n[768]')
dot.node('9', 'Conv\n[1024,3,2]')
dot.node('10', 'C2f x3\n[1024]')
dot.node('11', 'SPPCSPC\n[1024,5]')

# Head
dot.node('12', 'Upsample x2')
dot.node('13', 'Concat(P5)\n[11,8]')
dot.node('14', 'C2 x3\n[768]')

dot.node('15', 'Upsample x2')
dot.node('16', 'Concat(P4)\n[14,6]')
dot.node('17', 'C2 x3\n[512]')

dot.node('18', 'Upsample x2')
dot.node('19', 'Concat(P3)\n[17,4]')
dot.node('20', 'C2 x3\n[256]')

dot.node('21', 'DWConv\n[256,3,2]')
dot.node('22', 'Concat\n[21,17]')
dot.node('23', 'C2 x3\n[512]')

dot.node('24', 'DWConv\n[512,3,2]')
dot.node('25', 'Concat\n[24,14]')
dot.node('26', 'C2 x3\n[768]')

dot.node('27', 'DWConv\n[768,3,2]')
dot.node('28', 'Concat\n[27,11]')
dot.node('29', 'C2 x3\n[1024]')

dot.node('30', 'Detect\n[20,23,26,29]')

# Edges
dot.edges(['01','12','15','18'])
dot.edge('0', '1')
dot.edge('1', '2')
dot.edge('2', '3')
dot.edge('3', '4')
dot.edge('4', '5')
dot.edge('5', '6')
dot.edge('6', '7')
dot.edge('7', '8')
dot.edge('8', '9')
dot.edge('9', '10')
dot.edge('10', '11')
dot.edge('11', '12')
dot.edge('8', '13')
dot.edge('12', '13')
dot.edge('13', '14')

dot.edge('14', '15')
dot.edge('6', '16')
dot.edge('15', '16')
dot.edge('16', '17')

dot.edge('17', '18')
dot.edge('4', '19')
dot.edge('18', '19')
dot.edge('19', '20')

dot.edge('20', '21')
dot.edge('21', '22')
dot.edge('17', '22')
dot.edge('22', '23')

dot.edge('23', '24')
dot.edge('14', '25')
dot.edge('24', '25')
dot.edge('25', '26')

dot.edge('26', '27')
dot.edge('27', '28')
dot.edge('11', '28')
dot.edge('28', '29')

dot.edge('20', '30')
dot.edge('23', '30')
dot.edge('26', '30')
dot.edge('29', '30')

dot.render('yolov8m_improved_structure.gv', view=True)
