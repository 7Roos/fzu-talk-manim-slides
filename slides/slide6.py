from manim import *
from components.custom_slide import CustomSlide


class Slide6(CustomSlide):
    def construct(self):
        self.setup_scene()
        title = (
            VGroup(
                Text(
                    "Quantum case on the",
                    font="DejaVu Sans",
                    weight=BOLD,
                    font_size=self.FONT_SIZE_SUBTITLE,
                    color=self.get_color("title"),
                ),
                Text(
                    "bilayer honeycomb lattice",
                    font="DejaVu Sans",
                    weight=BOLD,
                    font_size=self.FONT_SIZE_SUBTITLE,
                    color=self.get_color("title"),
                ),
            )
            .arrange(DOWN, aligned_edge=ORIGIN, buff=0.1)
            .to_edge(UP, buff=0.2)
        )

        paper_bsl_classic = (
            ImageMobject("assets/paper_CBHL").scale(1.2).shift(0.55 * DOWN)
        )

        self.add(title, paper_bsl_classic)
        self.wait()

        # Magnetocaloric effect result
        self.next_slide(update_number=True)
        magnetocaloric_effect_img = (
            ImageMobject("assets/magnetocaloric_effect").scale(0.22).shift(0.2 * DOWN)
        )
        magnetocaloric_effect_caption = self.caption(
            magnetocaloric_effect_img,
            "g_{i} = J_{i}/J_{p}, \\ \\gamma_{\\textrm{mag}} \\text{ is the Grüneisen parameter, and } T_{N} \\text{ is the Néel temperature}",
        )
        magnetocaloric_effect = Group(
            magnetocaloric_effect_img, magnetocaloric_effect_caption
        )
        self.wipe(paper_bsl_classic, magnetocaloric_effect)
        self.wait()
