#!/usr/bin/env python3

from src.logic import StudiumLogic
from src.repository import JsonConfigRepository
from src.ui import DashboardApp

if __name__ == "__main__":
    repo = JsonConfigRepository("config.json")
    logic = StudiumLogic(repo)
    app = DashboardApp(logic)
    app.run()
