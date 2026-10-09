# Presentation for group seminar about how construct
# the Landaus's expansion for two order parameters
#
# Obs: Se a renderização do slide apresentar apenas uma tela preta,
# verifique se há ao menos um marcador de slide (self.next_slide()).
# Caso não haja, esse será provavelmente o problema.
# 
# M. Roos, 11/10/2025
# Last updated: 2025-11-19

from manim import *
from manim_slides import Slide
from pathlib import Path
import os
import sys

# Importe e depois redefina as classes aqui para que o Manim as encontre
from slides.cover import Cover as CoverOriginal
from slides.overview import Overview as OverviewOriginal
from slides.slide3 import Slide3 as Intro
from slides.slide4 import Slide4 as IsingModelJ1J2
from slides.slide5 import Slide5 as IsingModelJ1JxJp
from slides.slide6 import Slide6 as QuantumCase
from slides.slide7 import Slide7 as MagneticField
from slides.slide8 import Slide8 as Conclusion
from presentation import FullPresentation as PresentationOriginal, PresentationTest as PresentationTestOriginal


# Redefina as classes no escopo deste arquivo para que o Manim possa encontrá-las
#class FullPresentation(PresentationOriginal):
#    pass

class Cover(CoverOriginal):
    pass


class Overview(OverviewOriginal):
    pass

class Slide3(Intro):
    pass

class Slide4(IsingModelJ1J2):
    pass

class Slide5(IsingModelJ1JxJp):
    pass

class Slide6(QuantumCase):
    pass

class Slide7(MagneticField):
    pass

class Slide8(Conclusion):
    pass

class PresentationTest(PresentationTestOriginal):
    pass


# Configuração padrão
DEFAULT_QUALITY = "h"  # l=low, m=medium, h=high
DEFAULT_SCENE = "Cover"  # Cena padrão a ser renderizada

# Parsing de argumentos da linha de comando
if len(sys.argv) > 1 and sys.argv[1] not in ["manim"]:  # Pula se for chamado pelo Manim
    # Se for um número, converte para nome do slide
    if sys.argv[1].isdigit():
        slide_number = int(sys.argv[1])
        if slide_number == 1:
            SCENE = "Cover"
        elif slide_number == 2:
            SCENE = "Overview"
        elif slide_number == 3:
            SCENE = "Slide3"
        elif slide_number == 4:
            SCENE = "Slide4"
        elif slide_number == 5:
            SCENE = "Slide5"
        elif slide_number == 6:
            SCENE = "Slide6"
        elif slide_number == 7:
            SCENE = "Slide7"
        elif slide_number == 8:
            SCENE = "Slide8"
        elif slide_number == 9:
            SCENE = "FullPresentation"
        elif slide_number == 10:
            SCENE = "PresentationTest"
        # ... adicione outros slides conforme necessário
    else:
        SCENE = sys.argv[1]

    # Obtém qualidade se especificada
    if len(sys.argv) > 2:
        QUALITY = sys.argv[2]
    else:
        QUALITY = DEFAULT_QUALITY
else:
    SCENE = DEFAULT_SCENE
    QUALITY = DEFAULT_QUALITY

# Configura flags para o manim
FLAGS = f"-q{QUALITY}"
CLEAN = "--flush_cache "


def render_slide(slide_name, quality=DEFAULT_QUALITY):
    """
    Renders a slide using Manim.

    This function invokes Manim to render a specified slide with a given quality level.

    Parameters
    ----------
    slide_name : str
        The name of the slide class to be rendered.
    quality : str, optional
        The quality setting for Manim rendering.
        Defaults to DEFAULT_QUALITY.

    Examples
    --------
    >>> render_slide("IntroductionScene")  # Renders the IntroductionScene with default quality
    >>> render_slide("ConclusionScene", "h")  # Renders the ConclusionScene in high quality
    """
    script_name = f"{Path(__file__).resolve()}"
    os.system(f"manim {script_name} {slide_name} -q{quality}")


def convert_to_html(scenes):
    """Converts specified Manim slides to HTML format."""
    scenes_str = " ".join(scenes)
    os.system(f"manim-slides convert {scenes_str} index.html")


# Define a lista de todos os slides em ordem
ALL_SLIDES = [
    "Cover",
    "Overview",
    "Slide1",
    "Slide4",
    "Slide5",
    "Slide6",
    "Slide7",
    "Slide8",
    "Slide9",
    "Slide10",
    "FullPresentation",
]  # Adicione todos os slides aqui

if __name__ == "__main__":
    if SCENE == "all":
        # Renderiza todos os slides
        for slide in ALL_SLIDES:
            render_slide(slide, QUALITY)
        # Converte todos para HTML
        convert_to_html(ALL_SLIDES)
    else:
        # Renderiza apenas o slide especificado
        script_name = f"{Path(__file__).resolve()}"
        os.system(f"manim {script_name} {FLAGS} {SCENE}")

        convert_to_html([SCENE])

# COnvert eps to png
#magick -density 300 imagem.eps -background none imagem.png