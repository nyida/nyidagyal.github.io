Scientific figures

Six vector plates and six single-panel thumbnails support SnakeGuide's technical articles. SVG typography is converted to paths for stable rendering and downloads across operating systems. The React component supplies descriptive alternative text and HTML captions.

Requirements: the repository source, Node.js 22.13 or newer, tsx, Python 3, numpy, and matplotlib. tsx is a development-only extraction tool and is not declared as a root dependency. Install it locally without altering package.json or package-lock.json before regenerating:

npm install --no-save --package-lock=false tsx
python -m pip install numpy matplotlib

Run from the repository root:

node --import tsx public/research/figures/extract-data.ts
python public/research/figures/generate.py

The default generator writes only SVG publication assets. Optional raster previews are enabled with an explicit path outside public, for example:

SNAKEGUIDE_FIGURE_PREVIEWS=/tmp/snakeguide-figure-previews python public/research/figures/generate.py

Existing plate-data.json is sufficient to regenerate the SVGs without rerunning TypeScript extraction. Re-extract after engine or benchmark changes. Both source scripts contain no network calls.

Evidence

- `state-order.svg`: exact `move` outputs for two explicitly distinct inputs. Tail entry and food consumption illustrate different successors.
- `search-landscape.svg`: `traceSearch` applied to weighted `makeCase(2031, true)`. BFS: 16 steps, cost 24, 66 expansions. Dijkstra: 18 steps, cost 22, 62 expansions. A*: 18 steps, cost 22, 33 expansions. Heatmaps share an expansion-rank scale.
- `cycle-invariant.svg`: the actual `cycle(10, 6)` construction and eight nongrowing engine transitions, beginning with a ten-cell contiguous body.
- `connectivity-cut.svg`: `connected` on a declared static terrain graph before and after removing passage (5, 3). Reachability falls from 64 to 35 cells. The difference includes the removed vertex.
- `reward-telescoping.svg`: a declared algebraic sequence of potentials, not learning measurements. Gamma is 0.90; potentials are [-6, -5, -4, -3, -2, 0]. Discounted interior contributions cancel, leaving six.
- `benchmark-results.svg`: all 72 retained algorithm-case rows from the 24-case default static-grid benchmark. Extraction reruns the current implementation and refuses to proceed if it differs from `lib/benchmark-baseline.json`. Twenty cases are solved; four are disconnected. Summary statistics and paired scatter use the twenty solved cases.

The retained `plate-data.json` contains inputs and computed outputs. Static-grid path finding is not evidence of full-game Snake performance. No training curves or broad algorithm-ranking claims are implied.
