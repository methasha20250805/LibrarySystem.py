from StoreData import load_transactions
# trend graph
def trend_graph():
    print("Trend Graph: Books issued by Date")

    transactions = load_transactions()

    issues = [t for t in transactions if t["type"] == "1"]
    if not issues:
        print("No issues yet.")
        return
#error handling
    try:
        _plot_with_pandas_plotly(issues)
    except ImportError:
        print("Plotly or Pandas are not installed.")
        try:
            _plot_with_matplotlib(issues)
        except ImportError:
            print("Matplotlib is also not installed.")
            _print_text_summary(issues)

def _plot_with_pandas_plotly(issues: list):
    import pandas as pd
    import plotly.express as px

    df = pd.DataFrame(issues)
    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
    daily = df.groupby("date").size().reset_index(name="Books issued")
    daily = daily.sort_values("date")

    fig = px.line(
        daily,
        x="date",
        y="Books issued",
        markers=True,
        title = "Books Issued by Date",
        labels = {"date": "Date", "books_issued": "Number of Books Issued"}
    )
    fig.update_layout(
        xaxis_title = "Date",
        yaxis_title="Books Issued",
        title_font_size=20,
        hovermode="x unified"
    )
    print("Opening trend graph in your browser...")
    fig.show()

def _plot_with_matplotlib(issues: list):
    from datetime import datetime
    import matplotlib.pyplot as plt
    from collections import Counter

    dates = [datetime.strptime(t["date"], "%d/%m/%Y") for t in issues]
    counts = Counter(dates)
    sorted_dates = sorted(counts.keys())
    values = [counts[d] for d in sorted_dates]

    plt.figure(figsize=(12, 6))
    plt.plot(sorted_dates, values, marker='o', linewidth=2, color='steelblue')
    plt.fill_between(sorted_dates, values, alpha=0.15, color='steelblue')
    plt.title("Books Issued by Date", fontsize=16)
    plt.xlabel("Date")
    plt.ylabel("Number of Books Issued")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid(True, linestyle='--', alpha=0.5)
    print("Displaying trend graph...")
    plt.show()

def _print_text_summary(issues: list):
    from collections import Counter
    counts = Counter(t["date"] for t in issues)
    print(" Books Issued by Date (Text Summary)")
    print(f"{'Date':<15} {'Count':<6} {'Bar'}")
    print("-" * 50)
    for date in sorted(counts.keys()):
        bar = "\u2588" * counts[date]
        print(f"{date:<15} {counts[date]:<6} {bar}")