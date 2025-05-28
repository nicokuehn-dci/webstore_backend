import plotext as plt

def setup_modern_chart(term, title):
    """Configure plotext with modern styling for terminal charts"""
    plt.clear_figure()
    plt.theme("dark")
    plt.plotsize(term.width - 20, term.height // 3)
    plt.title(title)
    plt.grid(True)
    return plt

def create_bar_chart(term, title, x_data, y_data, x_label="", y_label="", color="cyan"):
    """Create a styled bar chart for terminal display"""
    chart = setup_modern_chart(term, title)
    chart.xlabel(x_label)
    chart.ylabel(y_label)
    chart.bar(x_data, y_data, color=color)
    return chart

def create_line_chart(term, title, x_data, y_data, x_label="", y_label="", color="green", marker="braille"):
    """Create a styled line chart for terminal display"""
    chart = setup_modern_chart(term, title)
    chart.xlabel(x_label)
    chart.ylabel(y_label)
    chart.plot(x_data, y_data, marker=marker, color=color)
    # No need to uncolorize as it's a function that requires a string parameter, not a chart method
    return chart
