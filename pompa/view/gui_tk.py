import tkinter as tk
from tkinter import ttk
import pompa.view.buttonframe as bf


class View:

    def __init__(self):
        self.root = tk.Tk()
        self.gui = Gui(self.root)

    def run(self):
        self.root.mainloop()


class Gui(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.mainframe = Mainframe(self)
        self.mainframe.pack(expand=True,
                            fill=tk.X,
                            side=tk.LEFT,
                            padx=(20, 10), pady=20)
        self.logoframe = Logo(self)
        self.logoframe.pack(side=tk.TOP,
                            padx=(10, 20), pady=(20, 10),
                            ipadx=10, ipady=10)
        self.buttonframe = bf.Buttonframe(self)
        self.buttonframe.pack(expand=True,
                              fill=tk.BOTH,
                              padx=(10, 20), pady=(10, 20),
                              ipadx=10, ipady=10)
        self.pack()

class Mainframe(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent

        self.notebook = tk.ttk.Notebook(self)
        self.notebook.pack()
        self.first_frame = tk.ttk.Frame(self.notebook)
        self.first_frame.pack()
        self.notebook.add(self.first_frame, text='pierwsza ramka')
        self.label = tk.Label(self.first_frame,
                              justify=tk.LEFT,
                              wraplength=400,
                              text="""Primus, lotus sagas etiam imperium de salvus, pius itineris tramitem.
Ausus de raptus genetrix, magicae candidatus!
valebats sunt musas de primus particula.
vitas sunt eleatess de gratis adelphis.
Sunt nixuses captis altus, bi-color victrixes.
impositio moris, tanquam fatalis habena.
cur parma persuadere?
Cum aonides congregabo, omnes imberes pugna flavum, dexter nomenes.
Pess sunt lactas de alter eleates.
altus liberi tandem attrahendams bubo est.
cum pulchritudine favere, omnes ollaes experientia azureus, audax barcases.
Valebats sunt hibridas de placidus repressor.
a falsis, fluctui raptus assimilatio.
germanus, gratis classiss aliquando acquirere de noster, bassus abactus. est bi-color devirginato, cesaris.
Hilotae de bi-color fraticinida, attrahendam magister!
aususs sunt fugas de festus cacula.
sunt absolutioes acquirere teres, rusticus itineris tramitemes.
Sunt zirbuses examinare alter, lotus brodiumes.
barbatus fortiss ducunt ad decor.
nunquam anhelare nomen.
Cum barcas experimentum, omnes abaculuses manifestum audax, germanus bullaes.
Hippotoxota de fidelis cannabis, visum bubo!
diatria de talis tumultumque, acquirere adiurator!
cum accola credere, omnes guttuses amor bassus, clemens indexes.
Absolutio de secundus mortem, anhelare turpis!
detriuss messis, tanquam domesticus lapsus.
verpa, visus, et capio. cum luba persuadere, omnes hilotaees contactus teres, raptus burguses.
Domuss sunt rationes de magnum omnia.
talis verpa aegre visums lura est.
gratis lacta virtualiter tractares hydra est.
Gratis triticum sed mire consumeres omnia est.
a falsis, mortem raptus planeta.
nunquam fallere itineris tramitem.
Cum guttus messis, omnes elevatuses dignus fortis, velox armariumes.
Mirabilis olla rare dignuss orgia est.
nuptias sunt ollas de albus devirginato.
brevis, placidus gloss acceleratrix imperium de flavum, alter repressor.
Lixas sunt fortiss de regius mons.
a falsis, zirbus gratis hilotae.
est primus zelus, cesaris.
Ausus de raptus genetrix, magicae candidatus!
valebats sunt musas de primus particula.
vitas sunt eleatess de gratis adelphis.
Sunt nixuses captis altus, bi-color victrixes.
impositio moris, tanquam fatalis habena.
cur parma persuadere?
""")

        self.label.pack(ipadx=20, ipady=20)

class Logo(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent,
                          relief='groove',
                          bd=2)
        self.parent = parent
        self.logo_label = tk.Label(self, font=("Courier New", 10, "bold"),
            text="""POMPA   POMPA  POMPA  POMPA  POMPA
__________________________________

 ****   ****  *     * ****   ***
 *   * *    * * * * * *   * *   *
 ****  *    * *  *  * ****  *****
 *     *    * *     * *     *   *
 *      ****  *     * *     *   *
__________________________________

POMPA    Wersja 2.01/2021r   POMPA""")
        self.logo_label.pack(expand=True)

if __name__ == "__main__":
    view = View()
    view.run()
