from manim import *
from components.custom_slide import CustomSlide


class Slide7(CustomSlide):
    def construct(self):
        self.setup_scene()
        title = (
            VGroup(
                Text(
                    "With longitudinal magnetic field",
                    font="DejaVu Sans",
                    weight=BOLD,
                    font_size=self.FONT_SIZE_SUBTITLE,
                    color=self.get_color("title"),
                ),
                Text(
                    "on the bilayer square lattice",
                    font="DejaVu Sans",
                    weight=BOLD,
                    font_size=self.FONT_SIZE_SUBTITLE,
                    color=self.get_color("title"),
                ),
            )
            .arrange(DOWN, aligned_edge=ORIGIN, buff=0.1)
            .to_edge(UP, buff=0.2)
        )

        self.add(title)

        # Portal
        line = Line(2.9 * DOWN, 2.5 * UP, color=[BLACK, ORANGE, BLACK]).shift(
            1.5 * LEFT
        )
        whiteboard_right = Rectangle(
            width=5.4, height=5.5, color=WHITE, fill_opacity=1
        ).next_to(line, RIGHT, buff=0.04)
        gs_diagram_2D_img = (
            ImageMobject("assets/GSdiagram").scale(0.11).move_to(whiteboard_right)
        )

        whiteboard_left = Rectangle(
            width=6.67, height=5.5, color=WHITE, fill_opacity=1
        ).next_to(line, LEFT, buff=0.01)
        gs_diagram_3D_img = (
            ImageMobject("assets/GSdiagram_3D").scale(0.25).move_to(whiteboard_left)
        )

        # gs_diagram_full = Group(gs_diagram, gs_diagram_caption)
        # whiteboard_right.set_z_index(0)
        # gs_diagram_2D_img.set_z_index(1)
        # whiteboard_left.set_z_index(0)
        # gs_diagram_3D_img.set_z_index(1)

        self.add(gs_diagram_3D_img, whiteboard_left)
        self.add(gs_diagram_2D_img, whiteboard_right)
        self.add(line)
        self.wait()

        self.next_slide()
        self.play(
            gs_diagram_2D_img.animate.shift(5.5 * LEFT), run_time=1, rate_func=smooth
        )
        self.wait()

        self.next_slide()
        self.remove(whiteboard_right)
        self.play(
            gs_diagram_3D_img.animate.shift(7.6 * RIGHT), run_time=1, rate_func=smooth
        )
        self.remove(whiteboard_left)

        # Group the 2D and 3D diagrams and add a caption
        gs_diagram = Group(gs_diagram_2D_img, gs_diagram_3D_img)
        gs_diagram_caption = self.caption(
            gs_diagram,
            "\\text{PP is the partial phase and FP is the fully polarized phase}",
        )
        self.play(FadeIn(gs_diagram_caption), run_time=0.5)
        self.wait()

        # Spin configurations
        self.next_slide(update_number=True)
        spin_config_img = ImageMobject("assets/lattice_CBSL_field").scale(0.4)
        spin_config_caption = self.caption(
            spin_config_img,
            "\\text{The PP phase is macroscopically degenerate}",
        )
        spin_config = Group(spin_config_img, spin_config_caption)
        self.add(spin_config)
        self.wipe(
            Group(
                line, gs_diagram_2D_img, gs_diagram_3D_img, gs_diagram_caption, title
            ),
            spin_config,
        )
        self.wait()

        # Results
        self.next_slide(update_number=True)
        legend = self.create_numbered_equation(
            "m_{1}^{A} = (\\sigma_{1}+ \\sigma_{3})/2, \\quad m_{2}^{A} = (\\sigma_{2}+ \\sigma_{4})/2, \\quad m_{1}^{B} = (\\sigma_{5}+ \\sigma_{7})/2, \\quad \\text{and} \\quad m_{2}^{B} = (\\sigma_{6}+ \\sigma_{8})/2."
        ).to_edge(UP, buff=1)

        plateau_img = ImageMobject("assets/plateau").scale(0.7).shift(0.5*DOWN)
        plateau_caption = self.caption(
            plateau_img, "m_{\\text{DAF}} \\text{ is the order parameter and } m  \\text{ is the total magnetization}"
        )
        plateau = Group(legend, plateau_img, plateau_caption)
        self.wipe(spin_config, plateau)
        self.wait()
