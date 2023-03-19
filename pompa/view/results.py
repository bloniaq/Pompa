import tkinter as tk
import pompa.view.figures as graphs


class ResultsWindow(tk.Toplevel):

    def __init__(self, view, results, station):
        tk.Toplevel.__init__(self, view)
        self.view = view
        text_content = self.prepare_results(results, station)
        self.title('Wyniki')

        frame = tk.Frame(self, relief='groove')
        frame.pack(padx=15, pady=15)

        self.text_f = tk.Text(frame, height=50, width=60)
        self.text_f.pack(side=tk.LEFT, padx=10, pady=10)
        self.text_f.insert(1.0, text_content)

    def prepare_graphs(self, parent, pumpsets, data_provider):
        graphs_nbook = tk.ttk.Notebook(parent)
        title_dict = {
            0: "  1 pompa pracująca  ",
            1: "  2 pompy pracujące  ",
            2: "  3 pompy pracujące  ",
            3: "  4 pompy pracujące  ",
            4: "  5 pomp pracujących  ",
        }
        graphs_list = []

        for i, pumpset in enumerate(pumpsets):
            data = data_provider(pumpset).prepare_data()
            container = {}
            container['frame'] = tk.Frame(graphs_nbook)
            container['graph'] = graphs.ResultGraph(container['frame'],
                                                    800, 760,
                                                    data)
            container['graph'].pack(side=tk.RIGHT, padx=10, pady=10)
            graphs_nbook.add(container['frame'], text=title_dict[i])
            graphs_list.append(container)

        return graphs_nbook

    def prepare_results(self, results, station):
        content = ""
        content += "POMPA   POMPA   POMPA   POMPA   POMPA   POMPA   POMPA\n\n\n"

        config_dict = {
            'optimal': "Optymalne ustawienie pomp w pompowni\n",
            'singlerow': "Liniowe ustawienie pomp w pompowni\n"
        }
        content += config_dict[station.well.config.get()]
        content += f"Liczba pomp rezerwowych..............n={results.reserve_pumps}\n"
        content += "results"

        return content
