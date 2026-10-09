from manim import *
from components.custom_slide import CustomSlide
from components.references import ReferenceMixin, register_ref


class Slide5(ReferenceMixin, CustomSlide):
    def construct(self):
        # self.setup_scene()
        title = MathTex(
            "\\boldsymbol{J_{1}\\text{-}J_{x}\\text{-}J_{p}} \\textbf{ Ising model on the BSL}",
            font_size=self.FONT_SIZE_EQ,
            color=self.get_color("title"),
        ).to_edge(UP)

        model_ham = VGroup(
            MathTex(
                "\\bullet \\text{Hamiltonian:}",
                font_size=self.FONT_SIZE_EQ_TEXT,
                color=self.get_color("text"),
            ),
            self.create_numbered_equation(
                "\\mathscr{H} = J_{1} \\sum_{\\langle ij \\rangle} \\sigma_{i}^{z} \\sigma_{j}^{z} + J_{x}\\sum_{\\langle\\langle ij \\rangle\\rangle'} \\sigma_{i}^{z} \\sigma_{j}^{z} + J_{p}\\sum_{\\langle ij \\rangle'} \\sigma_{i}^{z} \\sigma_{j}^{z} .",
                font_size=self.FONT_SIZE_EQ_TEXT,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        model_ham[1][0][0][2:4].set_color(RED_D)
        model_ham[1][0][0][16:18].set_color(ORANGE)

        coef_Landau_expansion1 = VGroup(
            MathTex(
                "\\bullet \\text{Equilibrium condition:}",
                font_size=self.FONT_SIZE_EQ_TEXT,
                color=self.get_color("text"),
            ),
            self.create_numbered_equation(
                "F_{1} = \\left( \\frac{\\partial F_{\\textrm{CMF}}}{\\partial m} \\right)_{T} = \\left\\langle \\frac{\\partial \\mathscr{H}_{\\textrm{CMF}}}{\\partial m} \\right\\rangle \\quad \\rightarrow  \\quad F_{1} = 0 .",
                font_size=self.FONT_SIZE_EQ_TEXT,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        coef_Landau_expansion2 = VGroup(
            MathTex(
                "\\bullet \\text{Critical temperature:}",
                font_size=self.FONT_SIZE_EQ_TEXT,
                color=self.get_color("text"),
            ),
            self.create_numbered_equation(
                "F_{2} = \\left( \\frac{\\partial^{2} F_{\\textrm{CMF}}}{\\partial m^{2}} \\right)_{T} = \\left\\langle \\frac{\\partial^{2} \\mathscr{H}_{\\textrm{CMF}}}{\\partial m^{2}} \\right\\rangle_{m=0} - \\beta \\left\\langle \\left( \\frac{\\partial \\mathscr{H}_{\\textrm{CMF}}}{\\partial m} \\right)^{2} \\right\\rangle_{m=0} \\rightarrow F_{2} = 0 .",
                font_size=self.FONT_SIZE_EQ_TEXT,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        coef_Landau_expansion4 = VGroup(
            MathTex(
                "\\bullet \\text{Tricritical point:}",
                font_size=self.FONT_SIZE_EQ_TEXT,
                color=self.get_color("text"),
            ),
            self.create_numbered_equation(
                "F_{4} = \\left( \\frac{\\partial^{4} F_{\\textrm{CMF}}}{\\partial m^{4}} \\right)_{T} = - \\beta^{3} \\left( \\left\\langle \\left( \\frac{\\partial \\mathscr{H}_{\\textrm{CMF}}}{\\partial m} \\right)^{4} \\right\\rangle_{0} - 3 \\left\\langle \\left( \\frac{\\partial \\mathscr{H}_{\\textrm{CMF}}}{\\partial m} \\right)^{2} \\right\\rangle_{0}^{2} \\right) \\rightarrow F_{4} = 0 .",
                font_size=self.FONT_SIZE_EQ_TEXT,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)

        # Para recuar levemente a equação em relação ao bullet (opcional):
        for group in [
            model_ham,
            coef_Landau_expansion1,
            coef_Landau_expansion2,
            coef_Landau_expansion4,
        ]:
            group[1].shift(RIGHT * 0.4)

        eqs = (
            VGroup(
                model_ham,
                coef_Landau_expansion1,
                coef_Landau_expansion2,
                coef_Landau_expansion4,
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            .shift(0.4 * DOWN)
        )

        cbsl_GS_img = ImageMobject("assets/lattice_CBSL").scale(0.22).shift(0.93 * DOWN)
        cbsl_GS_caption = self.caption(cbsl_GS_img, "\\text{Ground-state diagram.} \\text{ Motivation: The magnetic properties of } \\textrm{Bi}_{3} \\textrm{Mn}_{4} \\textrm{O}_{12}(\\textrm{NO}_{3}) \\text{ in the BHL}")

        # Ref
        register_ref(
            "Smirnova",
            "O. Smirnova, et al.",
            "Synthesis, Crystal Structure, and Magnetic Properties ...",
            2009,
            "J. Am. Chem. Soc",
            None,
        )
        register_ref(
            "Albarracin",
            "E. F. A. Gómez Albarracín, et al.",
            "Phase transitions, order by disorder, and finite entropy ...",
            2018,
            "Phys. Rev. E",
            None,
        )

        c_exp_motivation = self.cite(cbsl_GS_caption, "Smirnova", "Albarracin")
        foot_motivation = self.slide_references(
            keys=["Smirnova", "Albarracin"], full=True
        )  # só as citadas NESTE slide

        # Group
        cbsl_GS_group = Group(
            cbsl_GS_img, cbsl_GS_caption, c_exp_motivation, foot_motivation
        )

        structure_img = ImageMobject("assets/structure").scale(0.9).shift(12 * RIGHT).shift(DOWN)
        self.add(title, eqs[0], cbsl_GS_group, structure_img)
        self.wait()

        # structure
        self.next_slide()
        self.play(cbsl_GS_group[0].animate.shift(5 * LEFT), structure_img.animate.shift(9 * LEFT))
        self.wait()

        # paper
        self.next_slide(update_number=True)
        paper = ImageMobject("assets/paper_CBSL_classic").scale(1).shift(1 * DOWN)
        self.wipe(Group(cbsl_GS_group, structure_img), paper)
        self.wait()

        # Small clusters
        self.next_slide(update_number=True)
        small_clusters_img = (
            ImageMobject("assets/small_clusters").scale(0.3).shift(DOWN)
        )
        small_clusters_caption = self.caption(
            small_clusters_img, "q \\text{  is the number of intercluster bonds}"
        )
        small_clusters = Group(small_clusters_img, small_clusters_caption)
        self.wipe(paper, small_clusters)
        self.wait()

        # Large clusters
        self.next_slide(update_number=True)
        large_clusters_img = (
            ImageMobject("assets/large_clusters").scale(0.25).shift(DOWN)
        )
        large_clusters_caption = self.caption(
            large_clusters_img, "\\text{Sublattice structure}"
        )
        large_clusters = Group(large_clusters_img, large_clusters_caption)
        self.wipe(small_clusters, large_clusters)
        self.wait()

        # Landau free energy for two order parameters
        self.next_slide(update_number=True)
        landau_free_energy_img = (
            ImageMobject("assets/LandauFreeEnergy").scale(0.15).shift(DOWN)
        )
        landau_free_energy_caption = self.caption(
            landau_free_energy_img, "\\text{12-site cluster}"
        )
        landau_free_energy_group = Group(
            landau_free_energy_img, landau_free_energy_caption
        )
        self.wipe(large_clusters, landau_free_energy_group)
        self.wait()

        # Landau expansion
        self.next_slide(update_number=True)
        self.remove(landau_free_energy_group[0], landau_free_energy_group[1])
        self.add(eqs[1])
        self.wait()

        for item in range(2, len(eqs)):
            self.next_slide()
            self.play(Write(eqs[item]))
            self.wait()

        # Multiple sublattice order parameters
        self.next_slide()
        eff_order_param = (
            self.create_numbered_equation(
                "m_{\\textrm{eff}} &= \\frac{a m_{a} + b m_{b}}{n} \\\\ m & \\equiv m_{\\textrm{eff}}.",
                font_size=self.FONT_SIZE_EQ_TEXT,
            )
            .to_corner(UR)
            .shift(1.2 * DOWN)
        )
        box = SurroundingRectangle(eff_order_param)
        self.play(Write(eff_order_param), Create(box))
        self.wait()

        # First-order Landau expansion to two order parameters
        self.next_slide()
        f1_two_order_parameter = (
            self.create_numbered_equation(
                " F_{1} = \\left( \\frac{\\partial F(m_{a}, m_{b})}{\\partial m_{\\textrm{eff}}} \\right)_{T} =  \\left(\\frac{\\partial m_{a}}{\\partial m_{\\textrm{eff}}}\\right) \\left(\\frac{\\partial F}{\\partial m_{a}}\\right) + \\left(\\frac{\\partial m_{b}}{\\partial m_{\\textrm{eff}}}\\right) \\left(\\frac{\\partial F}{\\partial m_{b}}\\right) ",
                font_size=self.FONT_SIZE_EQ_TEXT,
            )
            .move_to(eqs[1][1])
            .shift(1.16 * RIGHT)
        )
        self.remove(eqs[1][1])
        self.play(TransformFromCopy(eqs[1][1], f1_two_order_parameter))
        self.wait()

        # Phase diagram
        self.next_slide(update_number=True)
        phase_diagram_img = ImageMobject("assets/phaseDiagram_CBSL").scale(0.25)
        phase_diagram_caption = self.caption(
            phase_diagram_img, "\\text{Eight-site cluster phase diagram}"
        )

        # Ref
        register_ref(
            "Rossato",
            "L. C. Rossato, et al.",
            "The Ising bilayer honeycomb lattice: A cluster mean-field study",
            2023,
            "Phys. A",
            None,
        )
        register_ref(
            "Fan",
            "Y. Fan, et al.",
            "Liquid-gas analog multicriticality in a frustrated Ising bilayer",
            2025,
            "Phys. Rev. B",
            None,
        )
        c_exp_motivation = self.cite(phase_diagram_caption, "Albarracin", "Rossato", "Fan")
        foot_motivation = self.slide_references(
            keys=["Albarracin", "Rossato", "Fan"], full=True
        )

        # Group
        phase_diagram_group = Group(
            phase_diagram_img, phase_diagram_caption, c_exp_motivation, foot_motivation
        )

        self.wipe(
            VGroup(
                title,
                eqs[0],
                eqs[1][0],
                eqs[2],
                eqs[3],
                eff_order_param,
                box,
                f1_two_order_parameter,
            ),
            phase_diagram_group,
        )
        self.wait()

        # Residual entropy
        # img
        self.next_slide(update_number=True)
        residual_entropy_img = ImageMobject("assets/residualEntropy").scale(0.25)
        residual_entropy_caption = self.caption(
            residual_entropy_img, "\\text{Residual entropy}"
        )

        # Ref
        c_residual_entropy = self.cite(residual_entropy_caption, "Albarracin", "Rossato")
        foot_residual_entropy = self.slide_references(
            keys=["Albarracin", "Rossato"], full=True
        )

        # Group
        residual_entropy_group = Group(residual_entropy_img, residual_entropy_caption, c_residual_entropy, foot_residual_entropy)
        self.wipe(phase_diagram_group, residual_entropy_group)
        self.wait()

        # Tricritical points
        self.next_slide(update_number=True)
        tricritical_points_img = ImageMobject("assets/tricriticalPoints").scale(0.20)
        tricritical_points_caption = self.caption(
            tricritical_points_img,
            "\\text{Tricritical points. (c) exhibits the ratio intracluster-intercluster bonds to several clusters size}",
        )
        tricritical_points_group = Group(
            tricritical_points_img, tricritical_points_caption
        )
        self.wipe(residual_entropy_group, tricritical_points_group)
        self.wait()
