import argparse
import plotly.graph_objects as go

def read_dot_file(file_path):
    nodes = {}
    edges = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('  '):  # Edge definition
                parts = line.strip().split('->')
                source_node = parts[0].strip()
                target_node = parts[1].split('[label=')[0].strip()
                edges.append((source_node, target_node))
            elif line.strip() and line.strip() != '}':  # Node definition
                parts = line.strip().split('[label=')
                node_id = parts[0].strip()
                node_label = parts[1].replace(']', '').strip('"')
                nodes[node_id] = node_label

    return nodes, edges

def create_plotly_graph(nodes, edges):
    plotly_edges = []
    for source, target in edges:
        plotly_edges.append((source, target))

    plotly_nodes = []
    for node_id, label in nodes.items():
        plotly_nodes.append(go.Scatter(x=[],
                                       y=[],
                                       text=[label],
                                       mode='markers+text',
                                       textposition='bottom center',
                                       hoverinfo='text',
                                       marker={'size': 10}))

    for source, target in plotly_edges:
        x0, y0 = plotly_nodes[int(source)]['x'], plotly_nodes[int(source)]['y']
        x1, y1 = plotly_nodes[int(target)]['x'], plotly_nodes[int(target)]['y']

        plotly_edges_trace = go.Scatter(x=x0 + x1 + [None],
                                        y=y0 + y1 + [None],
                                        mode='lines',
                                        line={'width': 1})

        plotly_nodes[int(source)]['x'] = x0
        plotly_nodes[int(source)]['y'] = y0
        plotly_nodes[int(target)]['x'] = x1
        plotly_nodes[int(target)]['y'] = y1

        plotly_nodes.append(plotly_edges_trace)

    layout = go.Layout(showlegend=False, hovermode='closest')
    fig = go.Figure(data=plotly_nodes, layout=layout)

    fig.show()

def main():
    parser = argparse.ArgumentParser(description='Visualize Hension .dot files using Plotly')
    parser.add_argument('dot_file', help='Path to the .dot file')
    args = parser.parse_args()

    dot_file_path = args.dot_file
    nodes, edges = read_dot_file(dot_file_path)
    create_plotly_graph(nodes, edges)

if __name__ == '__main__':
    main()
