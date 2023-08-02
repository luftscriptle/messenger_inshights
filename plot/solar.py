import numpy as np
import matplotlib.pyplot as plt


def show_polar(count, title, figname):
    ax = plt.subplot(111, projection="polar")

    x = np.arange(0, 2 * np.pi, 2 * np.pi / len(count)) + np.pi / len(count)

    ax.bar(x, count, width=2 * np.pi / len(count), alpha=0.4, color="#e76f51", bottom=0)

    max_ind = np.argmax(count)
    ax.bar(
        x[max_ind],
        count[max_ind],
        bottom=0,
        width=2 * np.pi / len(count),
        alpha=1,
        color="#e76f51",
    )

    ax.bar(
        x,
        np.max(count) * np.ones(len(count)),
        width=2 * np.pi / len(count),
        alpha=0.15,
        bottom=0,
        color="#cb997e",
        edgecolor="black",
    )

    ax.set_theta_direction(-1)
    ax.grid(False)
    ax.spines["polar"].set_visible(False)
    ax.set_theta_offset(np.pi / 2)
    ax.set_xticks(np.linspace(0, 2 * np.pi, 24, endpoint=False))
    ticks = [
        "12 AM",
        "",
        "",
        "3 AM",
        "",
        "",
        "6 AM",
        "",
        "",
        "9 AM",
        "",
        "",
        "12 PM",
        "",
        "",
        "3 PM",
        "",
        "",
        "6 PM",
        "",
        "",
        "9 PM",
        "",
        "",
    ]
    ax.set_xticklabels(ticks)
    ax.set_title(title, fontdict={"fontsize": 15})
    plt.setp(ax.get_yticklabels(), visible=False)
    return ax
    # plt.savefig(figname)
    # plt.tight_layout()
    # plt.show()
