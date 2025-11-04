import argparse, os, asyncio
from .planner import plan_from_prompt
from .navigator import Navigator
from .dataset import DatasetInfo

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt", type=str, help="Natural-language task request")
    ap.add_argument("--seed", type=str, required=True, help="Seed URL for the app")
    ap.add_argument("--dataset", type=str, required=True, help="Output dataset dir")
    args = ap.parse_args()

    os.makedirs(args.dataset, exist_ok=True)
    ds = DatasetInfo(
        name=os.path.basename(args.dataset),
        path=args.dataset,
        task_prompt=args.prompt,
        seed_url=args.seed
    )
    ds.write_blurb()

    plan = plan_from_prompt(args.prompt, args.seed)
    nav = Navigator(dataset_dir=args.dataset)

    asyncio.run(nav.run(plan, args.seed))

if __name__ == "__main__":
    main()
