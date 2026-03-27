def build_ui_graph(elements):

    graph = []

    for el in elements:

        graph.append({
            "type": "box",
            "position": el,
        })

    return graph