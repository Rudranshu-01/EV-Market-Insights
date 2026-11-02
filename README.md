# EV Market Atlas — Friend Edition

A distinct website implementation using the dataset and **attributed original Tableau reference views** from the EV Market Performance & Insights project. It is not a new Tableau dashboard/story and should not be submitted as independently authored Tableau work.

## Windows quick start

1. Extract the ZIP and open the `EV-Market-Insights-Friend` folder in VS Code.
2. In PowerShell run:

```powershell
python -m pip install -r requirements.txt
python app.py
```

3. Open http://127.0.0.1:5000

The dataset is bundled in `data/compressed_data-2.csv.gz`. The Flask website works locally without Tableau access, but Tableau embedded views need internet access and public availability.

## Use your own Tableau dashboard and story

Publish your own views, then set their links in PowerShell before running:

```powershell
$env:TABLEAU_DASHBOARD_URL="https://public.tableau.com/views/YOUR_WORKBOOK/YOUR_DASHBOARD?:showVizHome=no"
$env:TABLEAU_STORY_URL="https://public.tableau.com/views/YOUR_WORKBOOK/YOUR_STORY?:showVizHome=no"
python app.py
```

## Files

- `app.py` — Flask routes, CSV data aggregation and region filter.
- `templates/index.html` — refreshed responsive website and Chart.js visualizations.
- `data/compressed_data-2.csv.gz` — supplied EV dataset.
- `reference/Original_Tableau_Workbook_Reference.twbx` — original Tableau workbook, retained as reference only.
- `requirements.txt` — Python dependencies.
- `run_windows.bat` — one-click Windows launcher (requires Python installed).

## Attribution

The Tableau reference dashboard and story were previously published under the original EV Market Performance & Insights project (Tableau Public profile: `mausam.kumar.pandit`). They are shown for demonstration and comparison, not claimed as new work. The bundled original workbook must not be presented as your friend's own original Tableau analysis.

## Limitations

- Summed annual sales units are dataset aggregates, not externally validated sales figures.
- Tableau embed success depends on public links and network/browser settings.
- This project is intended for local demonstration; use a production WSGI server and appropriate configuration for deployment.
