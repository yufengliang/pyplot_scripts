
def kill_ticklabels(ax):
    labels = [item.get_text() for item in ax.get_xticklabels()]
    empty_string_labels = ['']*len(labels)
    ax.set_xticklabels(empty_string_labels)

def add_word(ax, px, py, word, **kwargs):
    ax.text(ax.get_xlim()[0] * (1 - px) + ax.get_xlim()[1] * px, 
            ax.get_ylim()[0] * (1 - py) + ax.get_ylim()[1] * py, 
            word, **kwargs)

def setticks(ax, m0, d, axis = 'x', offset = 0, all_int = False):
    import scipy as sp
    if axis == 'x':
        xl = ax.get_xlim()
        ticks = sp.arange(m0, max(xl) + d, d)
        if all_int: ticks = [int(t) for t in ticks]
        ax.set_xticks(ticks)
        ax.set_xticklabels([str(t + offset) for t in ticks])
    if axis == 'y':
        yl = ax.get_ylim()
        ticks = sp.arange(m0, max(yl) + d, d)
        if all_int: ticks = [int(t) for t in ticks]
        ax.set_yticks(ticks)
        ax.set_yticklabels([str(t + offset) for t in ticks])
    
