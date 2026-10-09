# Create a contents, list of subjects this talk
# M. Roos, 28/09/2026

from manim import *
from components.custom_slide import CustomSlide
from components.custom_slide import CustomMovingCameraSlide

class Overview(CustomMovingCameraSlide):
    def construct(self):
        # Título
        #self.setup_scene()
        title = Text(
            "Overview",
            font="DejaVu Sans",
            weight=BOLD,
            font_size=40,
            color=self.get_color("title"),
        )
        title.to_edge(UP, buff=0.5)

        # List
        list = MathTex(
            "&\\bullet \\text{What is frustration?} \\\\ ",
            "&\\bullet J_{1}\\text{-}J_{2}\\text{-}J_{p} \\text{ on the bilayer square lattice (BSL): QAC}; \\\\ ",
            "&\\bullet J_{1}\\text{-}J_{x}\\text{-}J_{p} \\text{ on the BSL: degeneracy and residual entropy}; \\\\ ",
            "&\\bullet J_{1}\\text{-}J_{x}\\text{-}J_{p} \\text{ on the BHL: magnetocaloric effect}; \\\\ ",
            "&\\bullet J_{1}\\text{-}J_{x}\\text{-}J_{p} \\text{ with magnetic field: non-trivial phase}; \\\\ ",
            "&\\bullet \\text{Conclusion}.",
            font_size=self.FONT_SIZE_EQ_TEXT,
            color=self.get_color("text")
        )

        self.add(title, list[0])
        self.wait()

        for i in range(1,6):
            self.next_slide()
            self.add(list[i])
            self.wait()