from manim import *
from components.custom_slide import CustomSlide
from components.references import ReferenceMixin, register_ref


class Slide4(ReferenceMixin, CustomSlide):
    def construct(self):
        # self.setup_scene()
        title = MathTex(
            "\\boldsymbol{J_{1}\\text{-}J_{2}\\text{-}J_{p}} \\textbf{ Ising model on the BSL}",
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
                "\\mathscr{H} = J_{1} \\sum_{\\langle ij \\rangle} \\sigma_{i}^{z} \\sigma_{j}^{z} + J_{2}\\sum_{\\langle\\langle ij \\rangle\\rangle} \\sigma_{i}^{z} \\sigma_{j}^{z} + J_{p}\\sum_{\\langle ij \\rangle'} \\sigma_{i}^{z} \\sigma_{j}^{z}- \\Gamma \\sum_{i} \\sigma_{i}^{x} .",
                font_size=self.FONT_SIZE_EQ_TEXT,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        model_ham[1][0][0][16:18].set_color(RED_D)
        model_ham[1][0][0][32:34].set_color(BLUE_D)

        bsl_lattice_img = ImageMobject("assets/lattice_BSL").scale(0.15).shift(DOWN)
        bsl_lattice_caption = self.caption(
            bsl_lattice_img,
            "\\text{Ground state } T = \\Gamma = 0.",
        )

        # Group
        bsl_lattice = Group(bsl_lattice_img, bsl_lattice_caption)

        method = VGroup(
            MathTex(
                "\\bullet \\text{Cluster mean-field (CMF):}",
                font_size=self.FONT_SIZE_EQ_TEXT,
                color=self.get_color("text"),
            ),
            self.create_numbered_equation(
                "\\mathscr{H}_{\\textrm{CMF}} = \\mathscr{H}_{0} \\left( \\{ \\sigma_{i}^{z} \\} \\right) +\\mathscr{H}_{\\textrm{MF}} \\left( \\{ \\sigma_{i}^{z}, m_{i}^{z} \\} \\right)- \\Gamma \\sum_{i=1}^{N_{s}} \\sigma_{i}^{x} .",
                font_size=self.FONT_SIZE_EQ_TEXT,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        bsl_cluster_img = (
            ImageMobject("assets/cluster_BSL").scale(0.13).shift(1.8 * DOWN)
        )
        bsl_cluster_caption = self.caption(
            bsl_cluster_img, "\\text{eight-site cluster}"
        )
        bsl_cluster = Group(bsl_cluster_img, bsl_cluster_caption)

        free_energy = VGroup(
            MathTex(
                "\\bullet \\text{Direct access to free energy:}",
                font_size=self.FONT_SIZE_EQ_TEXT,
                color=self.get_color("text"),
            ),
            self.create_numbered_equation(
                "F_{\\textrm{CMF}} = -\\beta^{-1} \\ln Z_{\\textrm{CMF}}, \\quad Z_{\\textrm{CMF}} = \\exp \\left(-\\beta \\mathscr{H}_{\\textrm{CMF}} \\right), \\quad \\beta = 1 / k_{B}T.",
                font_size=self.FONT_SIZE_EQ_TEXT,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        magnetization = VGroup(
            MathTex(
                "\\bullet \\text{Magnetization:}",
                font_size=self.FONT_SIZE_EQ_TEXT,
                color=self.get_color("text"),
            ),
            self.create_numbered_equation(
                "m_{i}^{\\alpha} = \\textrm{Tr } \\frac{\\sigma_{i}^{\\alpha}}{Z_{\\textrm{CMF}}} \\exp \\left( -\\beta \\mathscr{H}_{\\textrm{CMF}} \\right) .",
                font_size=self.FONT_SIZE_EQ_TEXT,
            ),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        # Para recuar levemente a equação em relação ao bullet (opcional):
        for group in [model_ham, method, free_energy, magnetization]:
            group[1].shift(RIGHT * 0.4)

        eqs = (
            VGroup(model_ham, method, free_energy, magnetization)
            .arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            .shift(0.15 * UP)
        )
        self.add(title)
        # Model and GS
        self.play(Write(eqs[0]))
        self.add(bsl_lattice)
        self.wait()

        # Method
        self.next_slide()
        self.play(FadeOut(bsl_lattice))
        self.play(Write(eqs[1]))
        self.add(bsl_cluster)
        self.wait()

        # Free energy
        self.next_slide()
        self.remove(bsl_cluster)
        self.play(Write(eqs[2]))
        self.wait()

        # Magnetization
        self.next_slide()
        self.play(Write(eqs[3]))
        self.wait()

        # Paper
        self.next_slide(update_number=True)
        paper_bsl_classic = (
            ImageMobject("assets/paper_BSL_classic").scale(1.2).shift(0.5 * DOWN)
        )
        self.wipe(Group(eqs[0], eqs[1], eqs[2], eqs[3]), paper_bsl_classic)
        self.wait()

        # Main result
        self.next_slide(update_number=True)
        title3 = Text(
            "Classical tricritical point",
            font="DejaVu Sans",
            weight=BOLD,
            font_size=self.FONT_SIZE_SUBTITLE,
            color=self.get_color("title"),
        ).to_edge(UP)

        # Phase diagram BSL image and caption
        phaseDiagram_BSL_img = (
            ImageMobject("assets/phaseDiagram_BSL").scale(0.16).shift(0.0 * DOWN)
        )
        phaseDiagram_BSL_caption = self.caption(
            phaseDiagram_BSL_img,
            "(J_2 / J_1)_{t} \\text{ and } (T / J_1)_{t} \\text{ are the coordinates at the tricritical point}",
        )
        phaseDiagram_BSL = Group(phaseDiagram_BSL_img, phaseDiagram_BSL_caption)

        # Citations
        register_ref(
            "Sandvick",
            "S. Jin, et al.",
            "Phase transitions in the frustrated Ising model on the square lattice",
            2013,
            "Phys. Rev. B",
        )
        register_ref(
            "Hansen",
            "P.L. Hansen, et al.",
            "Two coupled Ising planes: Phase diagram and interplanar force",
            1993,
            "J. Stat. Phys.",
            None,
        )
        c_phase_diagram = self.cite(
            phaseDiagram_BSL_caption, "Sandvick", "Hansen"
        )  # -> [1, 2]

        foot_phase_diagram = self.slide_references(
            keys=["Sandvick", "Hansen"], full=True
        )

        tricritical_point = Group(
            title3, phaseDiagram_BSL, c_phase_diagram, foot_phase_diagram
        )

        self.wipe(Group(title, paper_bsl_classic), tricritical_point, direction=UP)
        self.wait()

        # Quantum case
        self.next_slide(update_number=True)
        title2 = Text(
            "Quantum case",
            font="DejaVu Sans",
            weight=BOLD,
            font_size=self.FONT_SIZE_SUBTITLE,
            color=self.get_color("title"),
        ).to_edge(UP)
        paper_bsl_quantum = (
            ImageMobject("assets/paper_BSL_quantum").scale(1.1).shift(0.5 * DOWN)
        )
        quantum_case = Group(title2, paper_bsl_quantum)
        self.wipe(tricritical_point, quantum_case, direction=UP)
        self.wait()

        # Quantum Phase diagram
        self.next_slide(update_number=True)
        title = Text(
            "Quantum Annealed Criticality (QAC)",
            font="DejaVu Sans",
            weight=BOLD,
            font_size=self.FONT_SIZE_SUBTITLE,
            color=self.get_color("title"),
        ).to_edge(UP)

        # QAC image
        phaseDiagram_QAC_img = (
            ImageMobject("assets/phaseDiagram_QAC").scale(0.2).shift(0.3 * DOWN)
        )
        phaseDiagram_QAC_caption = self.caption(
            phaseDiagram_QAC_img,
            "\\text{Squares and circles denotes the quantum and classical tricritical points}",
        )

        # Ref QAC
        register_ref(
            "Chandra",
            "P.Chandra, et al.",
            "Quantum annealed criticality: A scaling description",
            2020,
            "Phys. Rev. Res",
            None,
        )
        register_ref(
            "Kellermann",
            "N. Kellermann, et al.",
            "Quantum Ising model on the frustrated square lattice",
            2019,
            "Phys. Rev. E",
            None,
        )
        c_qac = self.cite(phaseDiagram_QAC_caption, "Chandra", "Kellermann")
        foot_qac = self.slide_references(keys=["Chandra", "Kellermann"], full=True)

        QAC_phase_diagram = Group(
            title, phaseDiagram_QAC_img, phaseDiagram_QAC_caption, c_qac, foot_qac
        )
        self.wipe(quantum_case, QAC_phase_diagram, direction=UP)
        self.wait()

        # QAC plot T vs Gamma
        self.next_slide(update_number=True)
        title2 = (
            VGroup(
                Text(
                    "Experimentally accessible",
                    font="DejaVu Sans",
                    weight=BOLD,
                    font_size=self.FONT_SIZE_SUBTITLE,
                    color=self.get_color("title"),
                ),
                Text(
                    "phase diagrams",
                    font="DejaVu Sans",
                    weight=BOLD,
                    font_size=self.FONT_SIZE_SUBTITLE,
                    color=self.get_color("title"),
                ),
            )
            .arrange(DOWN, aligned_edge=ORIGIN, buff=0.1)
            .to_edge(UP, buff=0.2)
        )

        # QAC plot T vs Gamma img
        QAC_diagram_img = ImageMobject("assets/QAC").scale(0.17).shift(0.45 * DOWN)
        QAC_diagram_caption = self.caption(
            QAC_diagram_img, "\\text{QAC plot } T \\text{ vs } \\Gamma"
        )
        QAC_diagram = Group(QAC_diagram_img, QAC_diagram_caption)
        QAC_T_vs_Gamma = Group(title2, QAC_diagram)
        self.wipe(QAC_phase_diagram, QAC_T_vs_Gamma, direction=UP)
        self.wait()

        # Signatures of quantum criticality
        self.next_slide(update_number=True)
        title = Text(
            "Signatures of quantum criticality",
            font="DejaVu Sans",
            weight=BOLD,
            font_size=self.FONT_SIZE_SUBTITLE,
            color=self.get_color("title"),
        ).to_edge(UP)

        # Img
        quantum_signatures_img = (
            ImageMobject("assets/quantumTransition").scale(0.33).shift(0.5 * DOWN)
        )
        quantum_signatures_caption = self.caption(
            quantum_signatures_img, "\\text{QCP is the quantum critical point}"
        )
        quantum_signatures = Group(quantum_signatures_img, quantum_signatures_caption)
        quantum_signatures_group = Group(title, quantum_signatures)
        self.wipe(QAC_T_vs_Gamma, quantum_signatures_group, direction=UP)
        self.wait()

        # Entropy accumulation - quantum signature
        self.next_slide(update_number=True)
        title2 = Text(
            "Entropy accumulation",
            font="DejaVu Sans",
            weight=BOLD,
            font_size=self.FONT_SIZE_SUBTITLE,
            color=self.get_color("title"),
        ).to_edge(UP)

        # Entropy accumulation image and caption
        entropy_accumulation_img = (
            ImageMobject("assets/entropyACC").scale(0.25).shift(0.45 * DOWN)
        )
        entropy_accumulation_caption = self.caption(
            entropy_accumulation_img,
            "T = T_{N}(\\Gamma = 0) / 4, \\quad S_{0} \\equiv S(\\Gamma = 0), \\quad \\text{and} \\quad S^{*} \\equiv \\max_{\\Gamma} S(\\Gamma)",
        )
        entropy_accumulation = Group(
            entropy_accumulation_img, entropy_accumulation_caption
        )

        # Citations
        # N. Kellermann, M. Schmidt, F.M. Zimmer, Quantum Ising model on the frustrated square lattice, Phys. Rev. E 99 (2019) 012134.
        c_entropy_accumulation = self.cite(entropy_accumulation_caption, "Kellermann")
        foot_entropy_accumulation = self.slide_references(
            keys=["Kellermann"], full=True
        )

        entropy_accumulation_group = Group(
            title2,
            entropy_accumulation,
            c_entropy_accumulation,
            foot_entropy_accumulation,
        )
        self.wipe(quantum_signatures_group, entropy_accumulation_group, direction=UP)
        self.wait()
