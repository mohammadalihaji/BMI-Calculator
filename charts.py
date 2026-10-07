import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def plot_user_trend(user_name, records):
    """
    Plots the BMI trend over time for a given user using Matplotlib.
    
    records format: list of tuples (id, user_name, weight, height, bmi, category, created_at)
    """
    if not records:
        return None

    # Parse dates and BMI values
    dates = []
    bmis = []
    for r in records:
        date_str = r[6]
        # Parse timestamp safely
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            dt = datetime.fromisoformat(date_str)
        dates.append(dt)
        bmis.append(r[4])

    fig, ax = plt.subplots(figsize=(8, 5), dpi=100)

    # Shaded WHO BMI Classification Zones
    max_y = max(max(bmis) + 5, 36)
    min_y = min(min(bmis) - 3, 14)

    ax.axhspan(0, 18.5, color='#90caf9', alpha=0.35, label='Underweight (< 18.5)')
    ax.axhspan(18.5, 25.0, color='#a5d6a7', alpha=0.45, label='Normal (18.5 - 24.9)')
    ax.axhspan(25.0, 30.0, color='#ffe082', alpha=0.45, label='Overweight (25 - 29.9)')
    ax.axhspan(30.0, max(max_y, 45), color='#ef9a9a', alpha=0.45, label='Obese (≥ 30)')

    # Plot trend line with markers
    ax.plot(dates, bmis, marker='o', markersize=7, linewidth=2.5, color='#1565c0', 
            label='Recorded BMI', zorder=5)

    # Annotate each data point with its BMI value
    for dt, val in zip(dates, bmis):
        ax.annotate(f"{val:.1f}", (dt, val),
                    textcoords="offset points", xytext=(0, 9),
                    ha='center', fontsize=9, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#1565c0", alpha=0.85))

    # Format Axes
    ax.set_ylim(min_y, max_y)
    ax.set_title(f"BMI Progress & Trend — {user_name}", fontsize=13, fontweight='bold', pad=15)
    ax.set_xlabel("Date & Time", fontsize=10, fontweight='bold')
    ax.set_ylabel("BMI Value (kg/m²)", fontsize=10, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.5)

    # Format Date Ticks
    if len(dates) == 1:
        ax.set_xlim(dates[0], dates[0])
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d\n%H:%M'))
    fig.autofmt_xdate(rotation=0, ha='center')

    # Add legend outside or top
    ax.legend(loc='upper right', framealpha=0.9, fontsize=9)
    plt.tight_layout()

    return fig
