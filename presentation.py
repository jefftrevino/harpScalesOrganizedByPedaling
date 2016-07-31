from abjad import *


def make_sketch_lilypond_file(component):
    for voice in iterate(component).by_class(Voice):
        voice.remove_commands.append('Forbid_line_break_engraver')
        override(component).bar_line.stencil = False
        override(component).stem.stencil = False
        override(component).text_script.outside_staff_padding = 1
        override(component).time_signature.stencil = False
    lilypond_file = lilypondfiletools.make_basic_lilypond_file(component)
    lilypond_file.layout_block.indent = 0
    return lilypond_file


def make_sketch(rhythm_maker, divisions):
    # rhythmic creation
    selections = rhythm_maker(divisions)
    voice = Voice(selections)
    staff = Staff([voice], context_name='RhythmicStaff')
    score = Score([staff])
    lilypond_file = make_sketch_lilypond_file(score)
    return lilypond_file


__all__ = [
    'make_sketch',
    'make_sketch_lilypond_file',
    ]
