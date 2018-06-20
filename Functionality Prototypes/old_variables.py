        self.ksztalt = ksztalt = Variables('kolo', self.builder.get_variable('ksztalt'),
            '2', {'0': 'prostokat', '1': 'kolo'}, True, ['type(var) is string', 'var == \'prostokat\'', 'var ==\'kolo\''], ['Label_Ksztalt'], 'treść wskazówki', 'self.ksztalt_wymiary()')

        self.uklad_pompowni = uklad_pompowni = Variables('optymalny',
               self.builder.get_variable('uklad_pompowni'),
               '3',
               {'0': 'jednorzedowy', '1': 'optymalny'},
               True,
               ['type(var) is string', 'var == \'jednorzedowy\'', 'var == \'optymalny\''],
               ['Label_Uklad_pomp'],
               'treść wskazówki')

        self.tryb_pracy = tryb_pracy = Variables('0',
                self.builder.get_variable('tryb_pracy'),
                '1',
                {'0': 'minimalizacja', '1': 'sprawdzenie', '2':
                    'optymalizacja'},
                True,
                ['type(var) is string', 'var == \'minimalizacja\' or var == \'optymalizacja\' or var == \'spradzenie\''],
                ['Frame_Tryb'],
                'treść wskazówki', 'self.zmien_tryb()')
        self.liczba_pomp_rez = liczba_pomp_rez = Variables('optymalna',
                self.builder.get_variable('liczba_pomp_rez'),
                '4',
                {'1': 'minimalna', '2': 'optymalna', '3': 'bezpieczna'},
                True,
                ['type(var) is string'],
                ['Label_Wariant_rezerwa'],
                'treść wskazówki',
                True)
        self.minimalna_wys = minimalna_wys = Variables(0.0,
                self.builder.get_variable('minimalna_wys'),
                '9',
                {},
                True,

                ['type(var) is double'],
                ['Label_Minimalna_wys'],
                'treść wskazówki')

        self.rzedna_terenu = rzedna_terenu = Variables(0.0,
                self.builder.get_variable('rzedna_terenu'),
                '10',
                {},
                True,
                
                ['type(var) is double'],
                ['Label_Rzedna_terenu'],
                'treść wskazówki')

        self.rzedna_wylotu = rzedna_wylotu = Variables(0.0,
                self.builder.get_variable('rzedna_wylotu'),
                '11',
                {},
                True,
                ['type(var) is double'],
                ['Label_Rzedna_wylotu'],
                'treść wskazówki')

        self.variables = variables = [ksztalt, uklad_pompowni, tryb_pracy, liczba_pomp_rez, minimalna_wys, rzedna_terenu, rzedna_wylotu]
