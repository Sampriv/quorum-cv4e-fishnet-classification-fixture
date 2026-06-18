#!/usr/bin/env python3
import importlib.util, json, pathlib

root = pathlib.Path(__file__).resolve().parent
data = json.loads((root / "fixtures" / "fishnet.json").read_text())
spec = importlib.util.spec_from_file_location("predict", root / "predict.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
labels = data["labels"]
hits = 0
confusion = {c: {d: 0 for d in data["classes"]} for c in data["classes"]}
for sample in labels:
    pred = mod.predict(sample)
    if pred not in data["classes"]:
        raise SystemExit("unknown predicted class: " + str(pred))
    confusion[sample["species"]][pred] += 1
    hits += int(pred == sample["species"])
acc = hits / len(labels)
out = {"score": round(acc, 6), "accuracy": round(acc, 6), "valid": True, "metric": "fixture_accuracy", "confusion": confusion}
(root / "score.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, sort_keys=True))
