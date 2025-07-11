# test_cli.py
import typer

app = typer.Typer()

@app.command()
def generate():
    print("✅ generate() called")

if __name__ == "__main__":
    app()
