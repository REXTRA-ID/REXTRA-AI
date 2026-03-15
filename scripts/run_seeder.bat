@echo off
echo Menginstall psycopg2-binary...
pip install psycopg2-binary -q
echo.
echo Menjalankan seeder...
python "%~dp0run_seeder.py"
pause