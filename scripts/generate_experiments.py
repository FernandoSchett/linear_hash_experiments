import argparse
import json
from pathlib import Path


PAGE_SIZES = list(range(10, 101, 10))
ALPHA_MAX_VALUES = [0.40, 0.50, 0.60, 0.75, 0.80, 0.90, 0.95]
SEEDS = [42, 43, 44, 45, 46]

INITIAL_BUCKETS = 4
NUM_RECORDS = 100000
NUM_SUCCESSFUL_SEARCHES = 5000
NUM_UNSUCCESSFUL_SEARCHES = 5000


def alpha_tag(alpha: float) -> str:
    return f"a{int(round(alpha * 100)):03d}"


def build_config(page_size: int, alpha: float, seed: int, csv_dir: Path) -> dict:
    experiment_id = f"p{page_size}_{alpha_tag(alpha)}_s{seed}"
    return {
        "experiment_id": experiment_id,
        "page_size": page_size,
        "alpha_max": alpha,
        "initial_buckets": INITIAL_BUCKETS,
        "num_records": NUM_RECORDS,
        "num_successful_searches": NUM_SUCCESSFUL_SEARCHES,
        "num_unsuccessful_searches": NUM_UNSUCCESSFUL_SEARCHES,
        "seed": seed,
        "output_csv": str(csv_dir / f"{experiment_id}.csv").replace("\\", "/"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Gera configs do grid experimental.")
    parser.add_argument("--output-dir", default="build/generated_experiments")
    parser.add_argument("--csv-dir", default="resultados/csv/generated")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    csv_dir = Path(args.csv_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for old_config in output_dir.glob("*.json"):
        old_config.unlink()

    total = 0
    for page_size in PAGE_SIZES:
        for alpha in ALPHA_MAX_VALUES:
            for seed in SEEDS:
                config = build_config(page_size, alpha, seed, csv_dir)
                output_path = output_dir / f"{config['experiment_id']}.json"
                output_path.write_text(
                    json.dumps(config, indent=2, ensure_ascii=True) + "\n",
                    encoding="utf-8",
                )
                total += 1

    print(f"[OK] {total} configs geradas em {output_dir}")
    print(f"[OK] CSVs serao gravados em {csv_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
