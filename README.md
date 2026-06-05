# Runway Sim Command Cli

A dependency-free Python CLI for modeling startup runway, burn, revenue growth, and scenario packs.

Runway Sim models monthly cash, burn, revenue growth, and base/lean/growth scenario packs without dependencies.

## Development

```powershell
python -m pip install -e .
runway-sim-command-cli --cash 250000 --burn 42000 --revenue 9000 --pack
python -m unittest discover -s tests
```
