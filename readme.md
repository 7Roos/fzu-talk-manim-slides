# Manim Slides Presentation — FZU (Prague)

Repository for the interactive presentation developed with **Manim** and **Manim-Slides** for the talk at **FZU (Institute of Physics of the Czech Academy of Sciences, Prague)**.

This presentation covers the frustrated Ising models subject.

---

## 📋 Prerequisites

It is necessary to install:

- **Python**: version `3.9` and less `3.12`
- **FFmpeg**: for video processing and rendering
- **TeX Live (Full)**: full LaTeX distribution required for mathematical typography and rendering
- **Pkg-config** & **Cairo**: vector graphics libraries used by Manim
- **Manim**

More details can be found in the official documentation of **Manim** in (https://www.manim.community/) and **Manim-Slides** in (https://manim-slides.eertmans.be/latest/).

### Installing System Dependencies.

For Ubuntu:
```bash
sudo apt update
sudo apt install build-essential python3-dev libcairo2-dev libpango1.0-dev texlive-full
```

For Fedora:
```bash
sudo dnf install texlive-scheme-full python3-devel pkg-config cairo-devel pango-devel
```

---

## 🚀 Virtual Environment Setup

Some updates may break the manim or manim-slides functionality. Therefore, it is recommended to use a virtual environment to isolate dependencies and maintain a stable development setup.

Follow these steps to set up the Python virtual environment, activate it, and install all required packages from `requirements.txt`:

1. **Create the virtual environment:**
   ```bash
   conda create --name manim python=3.9
   ```

2. **Activate the virtual environment:**
   - **Linux/macOS:**
     ```bash
     conda activate manim
     ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## 🎨 Asset & Image Management (`assets/`)

All static images, logos (e.g., `.png`, `.svg`) used throughout the slides and animations may be stored in the `assets/` directory:

```text
.
├── assets/
│   ├── logo_capes.png
│   ├── logo_SAIA.png
├── components/
│   ├── custom_slide.py
│   └── references.py
├── slides/
│   ├── cover.py
│   ├── overview.py
│   └── ...
├── main.py
├── presentation.py
└── slides.html
```

In your Python code, you can load images using relative paths pointing to the `assets/` folder:
```python
ImageMobject("assets/logo_capes.png")
```

---

## 🎬 Running and Rendering the Presentation

### 1. Overview of `main.py` vs. `presentation.py`

- **`presentation.py` (`FullPresentation`)**: Defines the unified presentation structure. It chains together all individual slide modules into a single, cohesive presentation sequence with consistent counters and themes.
- **`main.py`**: The primary execution entry point. It imports individual slide classes alongside `presentation.py` and parses command-line arguments to trigger rendering for specific slides, quality levels, or the entire presentation.

- **Note:** Your presentation will be saved as an HTML file (`slides.html`) after rendering. Thus, you can open this file in a web browser to view the complete presentation. For passing slides, you can use left and right arrow keys.

---

### 2. Execution via `main.py`

You can render specific slides individually, test scenes, or compile the full presentation.

#### Render an individual slide by index number:
```bash
# Render Slide 1 (Cover) in high quality ("h")
python main.py 1 h

# Render Slide 2 (Overview)
python main.py 2 h
```

*Available quality options:* `l` (low/fast), `m` (medium), `h` (high - default). It is recommended to start with low quality for faster previews.

#### Render a slide by its class name:
```bash
python main.py Cover h
python main.py Slide4 m
```

#### Render the unified full presentation:
To render the full sequential presentation (`FullPresentation`) defined in `presentation.py`:
```bash
python main.py 9 h
# Or by running the test class:
python main.py PresentationTest h
```

---

## 🛠️ Tips & Troubleshooting

- **Converting EPS files to PNG:**
  If you need to convert vector `.eps` images to transparent `.png` files for use in `assets/`, run ImageMagick:
  ```bash
  magick -density 300 assets/image.eps -background none assets/image.png
  ```
- **Black screen bug:**
  If a slide renders as a black screen during interactive playback, ensure that at least one slide trigger (`self.next_slide()`) is present inside the slide's `construct()` method.