class MusicScale:
    # noteMap is a simple dictionary of lists of strings, intended to create \
    # a reference that later functions can use for constructing scales chords, etc.
    # The values of this dictionary are lists because some notes have two names,
    # such as Gsharp and Aflat, or Csharp and Dflat, etc.
    # noteMap creates key-value pairs, where the values are notes, and the keys
    # are integers from 0 to 11. Each integer represents a half-step, musically
    # speaking. The values start at A and ends at G sharp/ A flat.
    noteMap = ([0, 'A', 'A'], [1, 'As', 'Bf'], [2, 'B', 'B'], [3, 'C', 'C'], [4, 'Cs', 'Df'], [5, 'D', 'D'],
                  [6, 'Ds', 'Ef'], [7, 'E', 'E'], [8, 'F', 'F'], [9, 'Fs', 'Gf'], [10, 'G', 'G'], [11, 'Gs', 'Af'])
    num_to_noteMap = {0: ['A', 'A'], 1: ['As', 'Bf'], 2: ['B', 'B'], 3: ['C', 'C'], 4: ['Cs', 'Df'], 5: ['D', 'D'],
                      6: ['Ds', 'Ef'], 7: ['E', 'E'], 8: ['F', 'F'], 9: ['Fs', 'Gf'], 10: ['G', 'G'], 11: ['Gs', 'Af']}
    note_to_numMap = {'A': 0, 'As': 1, 'Bf': 1, 'B': 2, 'C': 3, 'Cs': 4, 'Df': 4, 'D': 5, 'Ds': 6, 'Ef': 6, 'E': 7,
                      'F': 8, 'Fs': 9, 'Gf': 9, 'G': 10, 'Gs': 11}
    sharp_list = (3, 10, 5, 0, 7, 2, 9)
    flat_list = (8, 1, 6, 11, 4)
    note_list = ['A', 'A#']

    # intervalMap is another tuple that operates similarly to noteMap, except it
    # maps the modes to their intervals relative to the major scale. This tuple
    # is used to programmatically fill in text when outputting results to the user,
    # and the value at position 3 in the sublists are used to determine whether the
    # next step in the current scale is a half step or a whole step away.
    intervalMap = (
        [1, "Ionian", "major", "I", 2, 1],
        [2, "Dorian", "minor", "ii", 2, 2],
        [3, "Phrygian", "minor", "iii", 1, 2],
        [4, "Lydian", "major", "IV", 2, 1],
        [5, "Mixolydian", "major", "V", 2, 2],
        [6, "Aeolian", "minor", "vi", 2, 2],
        [7, "Locrian", "diminished", "vii", 1, 2]
    )

    romanMap = {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI', 7: 'VII'}

    @classmethod
    def num_to_note(cls, num, sharps=True):

        note_list = MusicScale.num_to_noteMap[num]
        if sharps:
            return note_list[0]
        else:
            return note_list[1]

    # end def

    @classmethod
    def note_to_num(cls, note_name):

        return MusicScale.note_to_numMap[note_name]

    # end def

    # next_step handles the transition between integers. If a proposed step exceeds
    # the bounds of our noteMap, it 'starts over' at the correct value
    @classmethod
    def next_step(cls, current_int, step_size, map):

        lower_bound = 0
        upper_bound = len(map) - 1
        if current_int < lower_bound or current_int > upper_bound:
            print("Error: noteMap range exceeded")
        elif current_int + step_size > upper_bound:
            return current_int + step_size - upper_bound - 1
        elif current_int + step_size < lower_bound:
            return current_int + step_size + upper_bound + 1
        else:
            return current_int + step_size
        # end else

    # end def

    @classmethod
    def num_to_roman(cls, num, upper_case=True):

        if num in MusicScale.romanMap:
            if upper_case:
                return MusicScale.romanMap[num]
            else:
                return MusicScale.romanMap[num].lower()
            # end else
        else:
            print("num_to_roman: Value not in romanMap")
            return -1
        # end else

    # end def

    # build_scale builds a scale based on an inputted root note, and other optional
    # parameters, such as sharps, mode, etc. Mode defaults to 1 for the major scale
    # (Ionian). Enter an integer corresponding to that modes interval in the major
    # scale (2 for Dorian, 3 for Phrygian, etc.).
    @classmethod
    def build_scale(cls, root_note, mode=1, sharps=True):

        note_pos = root_note
        mode_pos = mode
        new_scale = []
        key_sig = -1
        for num in range(1, 8):
            if mode_pos == 1:
                key_sig = note_pos
            # end if
            new_scale.append([note_pos, mode_pos])
            note_pos = cls.next_step(note_pos, cls.intervalMap[mode_pos - 1][4], cls.noteMap)
            mode_pos = cls.next_step(mode_pos, 1, cls.intervalMap)
        # end for

        if key_sig in cls.sharp_list:
            sharps = True
        elif key_sig in cls.flat_list:
            sharps = False
        # end elif
        for num in range(0, 7):
            note_pos, mode_pos = new_scale[num]
            new_scale[num] = [
                cls.num_to_note(note_pos, sharps),
                cls.intervalMap[mode_pos - 1][1],
                cls.intervalMap[mode_pos - 1][3],
                cls.intervalMap[mode_pos - 1][2]
            ]
            # intervalMap at mode_pos -1 because of count starting at one in
            # intervalMap. Consider fixing this.
            note_pos = cls.next_step(note_pos, cls.intervalMap[mode_pos - 1][4], cls.noteMap)
            mode_pos = cls.next_step(mode_pos, 1, cls.intervalMap)
        # end for
        return new_scale

    # end class

    def get_note_text_from_interval(self, a):

        if a > 7 or a < 1:
            print("Error in method get_mode_text_from_interval: invalid interval input")
            return -1
        else:
            return self.full_scale_info[a - 1]
        # end else

    # end def

    def print_scale(self, detailed_print=False):

        if detailed_print:
            print("\tNote\tInterval\tChord Type")
            for note in self.notes:
                print("\t  {}\t\t  {}\t\t   {}".format(note[0], note[1], note[2]))
        else:
            print("{} {}: {}".format(self.root_note, MusicScale.intervalMap[self.mode][1], self.notes))
        # end else

    # end def

    def __init__(self, _root_note, _mode):
        self.full_scale_info = MusicScale.build_scale(root_note=_root_note, mode=_mode)
        self.mode = _mode
        self.notes = list(map(lambda x: x[0], self.full_scale_info))
        self.tonality = MusicScale.intervalMap[_mode-1][1]
        self.root_note = self.notes[0][0]
    # end def


# end class
