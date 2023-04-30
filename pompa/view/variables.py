import tkinter as tk


class ViewVariable:
    """ Abstract class intended to provide additional id parameter for
    subclassed tkinter variables."""

    def __init__(self, var_id, view):
        self.id = var_id
        self.view = view
        self.sent_to_model = None
        self.get_value_for_unit = None
        self.type = None


class StringVar(tk.StringVar, ViewVariable):
    """Class to wrap id parameter around standard tk.StringVar """

    def __init__(self, id_, view, *args, **kwargs):
        ViewVariable.__init__(self, id_, view)
        tk.StringVar.__init__(self, *args, **kwargs)


class IntVar(tk.IntVar, ViewVariable):
    """Class to wrap id parameter around standard tk.IntVar"""

    def __init__(self, id_, view, *args, **kwargs):
        ViewVariable.__init__(self, id_, view)
        tk.IntVar.__init__(self, *args, **kwargs)


class BoolVar(tk.BooleanVar, ViewVariable):
    """Class to wrap id parameter around standard tk.IntVar"""

    def __init__(self, id_, view, *args, **kwargs):
        ViewVariable.__init__(self, id_, view)
        tk.BooleanVar.__init__(self, *args, **kwargs)


class DoubleVar(tk.DoubleVar, ViewVariable):
    """Class to wrap id parameter around standard tk.DoubleVar"""

    def __init__(self, id_, view, *args, **kwargs):
        ViewVariable.__init__(self, id_, view)
        tk.DoubleVar.__init__(self, *args, **kwargs)

    def get(self):
        try:
            value = tk.DoubleVar.get(self)
        except tk.TclError:
            return 0
        else:
            return value

    def get_current_unit(self):
        return self.view.get_current_unit()

    def convert_unit(self, unit):
        self.set(self.get_value_for_unit(unit))


class PumpCharVar(ViewVariable):
    # placeholder for now
    def __init__(self, id_, view):
        ViewVariable.__init__(self, id_, view)
        self.values = []
        self.treeview = None

    def add_point(self, unit, flow, height):
        id_ = self.treeview.insert('', tk.END, values=(flow, height))
        ls = [(float(self.treeview.set(k, "vflow")), k) for k in self.treeview.get_children('')]
        ls.sort()
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(ls):
            self.treeview.move(k, '', index)
        point = {
            'id': id_,
            'unit': unit,
            'flow': float(flow),
            'height': float(height)
        }
        print("Adding point: ", id_, point['flow'], point['height'])
        self.values.append(point)
        self.sent_to_model(self.values)

    def delete_point(self, id_):
        for p in self.values:
            if p['id'] == id_:
                print("deleting: ", id_, type(id_), p['flow'], p['height'])
                self.treeview.delete(id_)
                self.values.remove(p)
        self.sent_to_model(self.values)

    def convert_unit(self, unit):
        values_list = self.get_value_for_unit(unit)
        for i in range(len(self.values)):
            self.values[i]['unit'] = unit
            self.values[i]['flow'] = values_list[i]
            self.treeview.set(self.values[i]['id'], "vflow", values_list[i])

    def get(self):
        return self.values

    def clear_points(self):
        print("Points clearing")
        ids = [p['id'] for p in self.values]
        for id_ in ids:
            self.delete_point(id_)
