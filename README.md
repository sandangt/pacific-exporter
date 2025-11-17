# Raison d'etre
An simple tool (with GUI) to export student results into details info card for Pacific Primary And High School

# Required OS libs:

- For MacOSX
  ```zsh
    brew install pango gdk-pixbuf cairo libffi glib
  ```

# Debug

  ```bash
    python3 -m app.main
  ```

# Code structure
  ```text
pacific-exporter/
├── .github/
│   └── workflows/
│       └── build-windows.yaml
├── app/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── db.py
│   │   └── report.py
│   ├── dto/
│   │   ├── __init__.py
│   │   ├── list_query.py
│   │   └── report.py
│   ├── exception/
│   │   ├── __init__.py
│   │   └── custom_exc.py
│   ├── main/
│   │   ├── view/
│   │   │   ├── __init__.py
│   │   │   ├── main_widget.py
│   │   │   └── main_window.py
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   └── dto.py
│   ├── model/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── learning_result.py
│   │   └── student.py
│   ├── repository/
│   │   ├── __init__.py
│   │   ├── crud.py
│   │   ├── learning_result.py
│   │   └── student.py
│   ├── service/
│   │   ├── __init__.py
│   │   ├── export_service.py
│   │   └── persist_service.py
│   ├── __init__.py
│   ├── constant.py
│   └── utils.py
├── resources/
│   ├── images/
│   │   └── .gitkeep
│   └── templates/
│       └── program-report.html
├── .editorconfig
├── .gitignore
├── pacific-exporter.spec
├── poetry.lock
├── pyproject.toml
├── README.md
└── requirements.txt
  ```
