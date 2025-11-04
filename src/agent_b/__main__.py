import argparse
import asyncio
import os
from .planner import Planner
from .navigator import Navigator
from .dataset import DatasetInfo, DatasetWriter

def main():
    # --- Parse CLI arguments ---
    parser = argparse.ArgumentParser(
        description="Agent B – Generalizable UI State Capture System"
    )
    parser.add_argument("prompt", help="Natural-language task request")
    parser.add_argument("--seed", required=True, help="Seed URL for the app")
    parser.add_argument("--dataset", required=True, help="Output dataset directory")
    args = parser.parse_args()

    # --- Initialize dataset metadata ---
    ds = DatasetInfo(
        prompt=args.prompt,
        seed_url=args.seed,
        dataset_dir=args.dataset
    )
    os.makedirs(ds.dataset_dir, exist_ok=True)

    # Write basic dataset info (_about.json)
    writer = DatasetWriter(ds.dataset_dir, about={
        "prompt": ds.prompt,
        "seed_url": ds.seed_url
    })

    # --- Plan the workflow ---
    planner = Planner()
    plan = planner.make_plan(ds.prompt)
    print(f"[AgentB] Generated plan: {[step.label for step in plan.steps]}")

    # --- Navigate and capture ---
    nav = Navigator(writer)
    asyncio.run(nav.run(plan, ds.seed_url))

    # --- Save manifest after completion ---
    writer.save_manifest()
    print(f"[AgentB] Dataset saved at {ds.dataset_dir}")

if __name__ == "__main__":
    main()

