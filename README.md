# Handwriting_Document_Generator

---

## Dependencies
```bash
pip install pillow==12.1.1
# or use uv
uv init
uv sync
```

## Add to source file `~/.bashrc` or `~/.zshrc` ...
```bash
export HAND_GEN_DIR="$HOME/<PATH TO PROJECT>"
alias handwriting_gen="uv run --project $HAND_GEN_DIR $HAND_GEN_DIR/main.py"
# or use python directly
alias handwriting_gen="python $HAND_GEN_DIR/main.py"
```

## Usage
```bash
handwriting_gen --sheet $HAND_GEN_DIR/handwriting_spritesheet00.png <input.txt>
```

