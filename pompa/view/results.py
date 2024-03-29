import tkinter as tk
import pompa.view.figures as graphs
import re
import textwrap
from pompa.exceptions import ErrorContainer


class ResultsWindow(tk.Toplevel):

    def __init__(self, view, results, station):
        tk.Toplevel.__init__(self, view)
        self.view = view
        self.errors = ErrorContainer().get_errors()
        text_content = self.prepare_results(results, station)
        self.title('Wyniki')


        self.pumpsets_number = len(results.pumpsets)

        frame = tk.Frame(self, relief='groove')
        frame.pack(padx=15, pady=15)

        self.text_f = tk.Text(frame, height=50, width=60)
        self.text_f.pack(side=tk.LEFT, padx=(10, 0), pady=10, fill=tk.BOTH)
        # wcięcie
        self.insert_text_with_indent(self.text_f, text_content,
                                     l_marg=20, r_marg=20)

        scrollbar = tk.Scrollbar(frame)
        self.text_f.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_f.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), pady=10)

        data_provider = station.result_data_provider

        nbook = self.prepare_graphs(frame, results.pumpsets, data_provider)
        nbook.pack(side=tk.RIGHT, padx=10, pady=10)

    def insert_text_with_indent(self, widget, text, l_marg, r_marg):
        lines = re.split('\n(?!\n)', text)
        for line in lines:
            widget.insert(tk.END, " " + line + "\n", ("indent",))
        widget.tag_configure("indent", lmargin1=l_marg, lmargin2=r_marg)

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
        content += f"Liczba pomp rezerwowych..............n={results.reserve_pumps:6}\n"
        content += f'Średnica koła opisującego pompę.....Dn={station.pump_type.contour.value:6}    [m]\n'

        pumps_count = len(results.pumpsets) + results.reserve_pumps
        if station.well.shape.get() == 'round':
            content += f'Średnica pompowni...................DN={station.well.diameter.value:6}    [m]\n'
            min_well_diam = station.min_well_dimension(pumps_count)
            content += f'Minimalna średnica pompowni......DNmin={min_well_diam:6}    [m]\n'
        elif station.well.shape.get() == 'rectangle':
            content += f'Długość pompowni.....................L={station.well.length.value:6}    [m]\n'
            content += f'Szerokość pompowni...................B={station.well.width.value:6}    [m]\n'
            min_w, min_l = station.min_well_dimension(pumps_count)
            content += f'Minimalna długość pompowni........Lmin={min_l:6}    [m]\n'
            content += f'Minimalna szerokość pompowni......Bmin={min_w:6}    [m]\n'

        content += f'Pole poziomego przekroju pompowni....F={station.well.cr_sec_area().value:6}   [m2]\n'
        content += f'Ilość przewodów tłocznych (kolektor)..{int(station.out_pipes_no.get()):7}\n'
        content += f'Długość kolektora tłocznego..........L={station.out_pipe.length.get():6}    [m]\n'
        content += f'Długość przewodu w pompowni..........L={station.ins_pipe.length.get():6}    [m]\n'
        content += f'Średnica kolektora tłocznego........Dn={station.out_pipe.diameter.get() * 1000:6}   [mm]\n'
        content += f'Średnica przewodu w pompowni........Dn={station.ins_pipe.diameter.get() * 1000:6}   [mm]\n'
        content += f'Chropowatość kolektora tłocznego.....k={station.out_pipe.roughness.get() * 1000:6}   [mm]\n'
        content += f'Chropowatość przewodu w pompowni.....k={station.ins_pipe.roughness.get() * 1000:6}   [mm]\n'
        content += f'Dopływ do pompowni...Qmin= {station.hydr_cond.inflow_min.value_lps:5}  Qmax= {station.hydr_cond.inflow_max.value_lps:5}  [l/s]\n'
        content += f'Rzędna terenu.........................{station.hydr_cond.ord_terrain.get():7}    [m]\n'
        content += f'Rzędna dopływu ścieków................{station.hydr_cond.ord_inlet.get():7}    [m]\n'
        content += 'Rzędna wylotu ścieków /przejście\n'
        content += f'osi rury przez ścianę pompowni/.......{station.hydr_cond.ord_outlet.get():7}    [m]\n'
        # content += f'Rzędna najwyższego pkt. na trasie.....{station.hydr_cond.ord_highest_point.get():7}    [m]\n'
        content += f'Rzędna zwierciadła w zbiorniku górnym.{station.hydr_cond.ord_upper_level.get():7}    [m]\n'
        content += f'Min. wysokość ścieków w  pompowni.....{station.pump_type.suction_level.get():7}    ' \
                   f'[m]\n'
        content += f'Suma wsp. oporów miejsc. kolektora....{station.out_pipe.resistances.sum():7}\n'
        content += f'Suma wsp. oporów miejsc. w pompowni...{station.ins_pipe.resistances.sum():7}\n\n'
        content += 'CHARAKTERYSTYKA ZASTOSOWANYCH POMP\n\n'
        content += self.prepare_pump_char_report(station.pump_type.characteristic.value)
        content += f'Rzędna dna pompowni...................{station.hydr_cond.ord_bottom.get():7}    [m]\n'
        content += f'Rzędna wyłączenia się pomp............{results.ord_shutdown.get():7}    [m]\n'

        if not self.critical_errors():
            content += self.prepare_well_report(results)
            for i, pumpset in enumerate(results.pumpsets):
                content += self.prepare_pset_report(i, pumpset)

        if len(self.errors) > 0:
            content += self.prepare_error_report()

        return content

    def prepare_pset_report(self, i, pset):
        report = '\n'
        report += f'PARAMETRY POMPY NR: {i+1}\n\n'
        report += f'Rzeczywisty czas cyklu pompy.......T={pset.cyc_time:7}     [s]\n'
        report += f'Rzeczywisty czas postoju pompy....Tp={pset.lay_time:7}     [s]\n'
        report += f'Rzeczywisty czas pracy pompy......Tr={pset.wor_time:7}     [s]\n'
        report += f'Obj. użyt. wyzn. przez pompę......Vu={pset.vol_u:7}    [m3]\n'
        report += f'Rzędna włączenia pompy..............{pset.ord_start.value:8}     [m]\n\n'
        report += 'Parametry początkowe pracy zespołu pomp\n'
        report += f'w chwili włączenia pompy nr {i+1}\n\n'
        report += f'-wys. lc. u wylotu pompy.........Hlc={pset.wpoint_start.height:7}     [m]\n'
        report += f'-geometryczna wys. podnoszenia.....H={pset.wpoint_start.geom_h:7}     [m]\n'
        report += f'-wydatek...........................Q={pset.wpoint_start.flow.value_lps:7}   [l/s]\n'
        report += f'-prędkość w kolektorze tłocznym....v={pset.wpoint_start.out_pipe_v:7}   [m/s]\n'
        report += f'-prędkość w przewodach w pompowni..v={pset.wpoint_start.ins_pipe_v:7}   [m/s]\n\n'
        report += f'Parametry końcowe pracy zespołu pomp\n\n'
        report += f'-wys. lc. u wylotu pompy.........Hlc={pset.wpoint_stop.height:7}     [m]\n'
        report += f'-geometryczna wys. podnoszenia.....H={pset.wpoint_stop.geom_h:7}     [m]\n'
        report += f'-wydatek...........................Q={pset.wpoint_stop.flow.value_lps:7}   [l/s]\n'
        report += f'-prędkość w kolektorze tłocznym....v={pset.wpoint_stop.out_pipe_v:7}   [m/s]\n'
        report += f'-prędkość w przewodach w pompowni..v={pset.wpoint_stop.ins_pipe_v:7}   [m/s]\n'
        report += f'-dopływ najniekorzystniejszy....Qdop={pset.worst_inflow.value_lps:7}   [l/s]\n'
        report += 'Zakres pracy pomp /maksymalna sprawność/\n'
        report += f'Q1={pset.opt_range[0].value_lps:5} [l/s]    Q2={pset.opt_range[1].value_lps:5} [l/s]\n\n'

        return report

    def prepare_pump_char_report(self, charact):
        report = ''
        for point in charact:
            report += f'Q={point[0].value_lps:5} [l/s]    H={point[1]:5} [m]\n'
        report += '\n'
        return report

    def prepare_well_report(self, results):
        content = ""

        total_v, useful_v, reserve_v, dead_v = results.calculate_volumes()

        content += f'Objętość całkowita pompowni..........Vc={total_v:5}   [m3]\n'
        content += f'Objętość użyteczna pompowni..........Vu={useful_v:5}   [m3]\n'
        content += f'Objętość rezerwowa pompowni..........Vr={reserve_v:5}   [m3]\n'
        content += f'Objętość martwa pompowni.............Vm={dead_v:5}   [m3]\n\n'
        content += f'Vu/Vc ={round(100 * useful_v / total_v, 1):5}%\n'
        content += f'Vr/Vu ={round(100 * reserve_v / useful_v, 1):5}%\n'
        content += f'Vr/Vc ={round(100 * reserve_v / total_v, 1):5}%\n'
        content += f'Vm/Vc ={round(100 * dead_v / total_v, 1):5}%\n\n'

        return content

    def prepare_error_report(self):
        content = "\n\n\nBŁĘDY:\n\n"
        for i, e in enumerate(self.errors):
            content += str(i + 1) + ". "
            content += textwrap.fill(e.get_message(), width=52)
            content += "\n\n"

        return content

    def critical_errors(self):
        result = False
        if len(self.errors) != 0:
            for e in self.errors:
                if e.critical_flag:
                    result = True
        return result
