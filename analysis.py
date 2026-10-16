"""Duración media por año y pista de mayor popularidad por año."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


DURATION_COLUMNS = {"year", "duration_ms"}
RANKING_COLUMNS = {"year", "name", "artist", "popularity", "energy"}


def duration_by_year(data_path: Path) -> pd.DataFrame:
    data = pd.read_csv(data_path)
    missing = DURATION_COLUMNS - set(data.columns)
    if missing:
        raise ValueError(f"Faltan columnas: {', '.join(sorted(missing))}")

    for column in DURATION_COLUMNS:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    data = data.loc[data["year"].between(1921, 2020)].copy()
    data = data.dropna(subset=list(DURATION_COLUMNS))
    data = data.loc[data["duration_ms"] > 0].copy()
    if data.empty:
        raise ValueError("No hay registros válidos entre 1921 y 2020")

    data["year"] = data["year"].astype(int)
    data["duration_min"] = data["duration_ms"] / 60_000
    summary = data.groupby("year", sort=True).agg(
        tracks=("duration_min", "size"),
        mean_duration_min=("duration_min", "mean"),
    )
    return summary


def top_track_by_year(data_path: Path) -> pd.DataFrame:
    data = pd.read_csv(data_path)
    missing = RANKING_COLUMNS - set(data.columns)
    if missing:
        raise ValueError(f"Faltan columnas: {', '.join(sorted(missing))}")

    for column in ("year", "popularity", "energy"):
        data[column] = pd.to_numeric(data[column], errors="coerce")
    data = data.loc[data["year"].between(1980, 2020)].copy()
    data = data.dropna(subset=["year", "name", "popularity", "energy"])
    data["year"] = data["year"].astype(int)
    data["artist"] = data["artist"].fillna("")

    # Primero popularidad; la energía desempata solo si la popularidad coincide.
    ranking = data.sort_values(
        ["year", "popularity", "energy", "name", "artist"],
        ascending=[True, False, False, True, True],
        kind="stable",
    )
    return ranking.drop_duplicates("year", keep="first")[
        ["year", "name", "artist", "popularity", "energy"]
    ].reset_index(drop=True)


def plot_duration(summary: pd.DataFrame, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(11, 5), constrained_layout=True)
    ax.plot(
        summary.index,
        summary["mean_duration_min"],
        color="#186c45",
        linewidth=1.7,
        marker="o",
        markersize=3.4,
    )
    ax.set(
        title="Duración media anual de los registros del archivo (1921–2020)",
        xlabel="Año de lanzamiento",
        ylabel="Duración media (minutos)",
    )
    ax.set_xlim(1920, 2021)
    ax.set_xticks(range(1920, 2021, 10))
    ax.grid(alpha=0.25)
    ax.spines[["top", "right"]].set_visible(False)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path,
                        default=Path("data/spotify_artists.csv"),
                        help="Ruta al CSV del módulo")
    args = parser.parse_args()

    summary = duration_by_year(args.data)
    ranking = top_track_by_year(args.data)
    Path("results").mkdir(exist_ok=True)
    summary.to_csv("results/duration_by_year.csv", float_format="%.6f")
    ranking.to_csv("results/top_track_by_year.csv", index=False, float_format="%.3f")
    plot_duration(summary, Path("images/duration_by_year.png"))
    print(f"Registros analizados: {int(summary['tracks'].sum()):,}")
    print(f"Años de duración: {len(summary)}")
    for year in (1980, 2000, 2020):
        print(f"Duración media {year}: {summary.loc[year, 'mean_duration_min']:.3f} min")
    print(f"Años del ranking: {len(ranking)}")


if __name__ == "__main__":
    main()
