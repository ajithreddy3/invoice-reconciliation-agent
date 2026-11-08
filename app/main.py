import argparse
import json
from pathlib import Path
from app.graph import app
from utils.schemas import AgentState


def serialize(obj):
    if hasattr(obj, 'model_dump'):
        return obj.model_dump()
    if isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [serialize(i) for i in obj]
    return obj


def main():
    parser = argparse.ArgumentParser(description='Reconcile invoice PDFs against local purchase orders')
    parser.add_argument('invoices', nargs='*', help='PDF files or directories; defaults to bundled samples')
    args = parser.parse_args()
    paths = args.invoices or [str(Path(__file__).resolve().parents[1] / 'data' / 'invoices')]
    invoices = []
    for value in paths:
        path = Path(value)
        if path.is_dir():
            invoices.extend(sorted(file for file in path.iterdir() if file.suffix.lower() == '.pdf'))
        else:
            invoices.append(path)
    if not invoices:
        parser.error('No PDF files found')
    for path in invoices:
        print(f'\n=== Processing {path.name} ===\n')
        result = app.invoke(AgentState(filename=str(path)))
        print(json.dumps(serialize(result), indent=2))


if __name__ == '__main__':
    main()
