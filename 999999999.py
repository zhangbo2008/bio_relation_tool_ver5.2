import tkinter as tk
import klembord

root = tk.Tk()
text = tk.Text(root)
text.pack(fill='both', expand=True)

text.tag_configure('italic', font='TkDefaultFont 9 italic')
text.tag_configure('bold', font='TkDefaultFont 9 bold')

TAG_TO_HTML = {
    ('tagon', 'italic'): '<i>',
    ('tagon', 'bold'): '<b>',
    ('tagoff', 'italic'): '</i>',
    ('tagoff', 'bold'): '</b>',
}

def copy_rich_text(event):
    try:
        txt = text.get('sel.first', 'sel.last')
    except tk.TclError:
        # no selection
        return "break"
    content = text.dump('sel.first', 'sel.last', tag=True, text=True)
    html_text = []
    for key, value, index in content:
        if key == "text":
            html_text.append(value)
        else:
            html_text.append(TAG_TO_HTML.get((key, value), ''))
    klembord.set_with_rich_text(txt, ''.join(html_text))
    return "break"  # prevent class binding to be triggered

text.bind('<Control-c>', copy_rich_text)

text.insert("1.0", "Author et al. (2012). The title of the article. ")
text.insert("end", "Journal Name", "italic")
text.insert("end", ", ")
text.insert("end", "2", "bold")
text.insert("end", "(599), 1–5.")

root.mainloop()