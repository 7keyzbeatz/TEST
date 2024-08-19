name: Remove Duplicate Movies

on:
  workflow_dispatch:

jobs:
  remove-duplicates:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: pip install --upgrade pip

    - name: Run the remove duplicates script
      run: python scripts/moviesforremoval.py

    - name: Commit changes if any
      run: |
        git config --global user.email "medialtdcontact@gmail.com"
        git config --global user.name "med1altd"
        git add movies.json
        git diff --quiet || git commit -m "Removed duplicate movies based on Title and DirectVideo"
        git push || echo "No changes to commit"

    - name: Upload cleaned JSON as artifact
      uses: actions/upload-artifact@v3
      with:
        name: cleaned-movies-json
        path: movies.json
