import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import mplcyberpunk
import io, base64


def generate_line_plot(data):
    x, y = data[0], data[1]
    matplotlib.use('Agg')
    plt.style.use('cyberpunk')
    plt.figure(figsize=(8, 4), dpi=300)
    plt.plot(x, y, marker='o')
    mplcyberpunk.make_lines_glow()
    plt.xlabel("day", fontsize=16)
    plt.ylabel("temperature", fontsize=16)
    plt.xticks(np.arange(1, 32, step=2))
    plt.yticks(np.arange(0, 45, step=5))

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300)
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')

    return f'<img src="data:image/png;base64,{img_str}" style="width:100%; height:100%;"/>'

