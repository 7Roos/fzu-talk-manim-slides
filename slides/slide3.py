from manim import *
from components.custom_slide import CustomSlide


class Slide3(CustomSlide):
    def construct(self):
        title = Text(
            "What is frustration?",
            font="DejaVu Sans",
            weight=BOLD,
            font_size=self.FONT_SIZE_SUBTITLE,
            color=self.get_color("title"),
        ).to_edge(UP)

        list = (
            MathTex(
                "&\\bullet \\text{Impossibility of satisfying all interactions simultaneously}; \\\\ ",
                "&\\bullet \\text{Geometric frustration}; \\\\ ",
                "&\\bullet \\text{Competitive interactions}; \\\\ ",
                "&\\bullet J_{1}\\text{-}J_{2} \\text{ Ising model on a square lattice}; \\\\ ",
                "&\\bullet \\text{Consequences of frustration:} \\\\ ",
                font_size=self.FONT_SIZE_EQ_TEXT,
                color=self.get_color("text"),
            )
            .to_edge(LEFT)
            .shift(1.7 * UP)
        )

        triangle = (
            RegularPolygon(n=3, color=BLACK, stroke_width=12).scale(2.1).shift(DOWN)
        )

        spins_triangle = VGroup()
        spin_label = VGroup(
            Text("Study", color=self.get_color("background"), weight=BOLD),
            Text("Sleep", color=self.get_color("background"), weight=BOLD),
            Text("Social", color=self.get_color("background"), weight=BOLD),
        )
        i = 0
        # Itera sobre os vértices do triângulo e cria um círculo em cada um
        for vertex in triangle.get_vertices():
            spin = Circle(radius=1.1, color=BLACK, fill_opacity=1)
            spin.move_to(vertex)
            spins_triangle.add(spin)
            spin_label[i].move_to(vertex)
            i = i + 1

        spinDown = self.get_color("line", category="timeline")
        spinUP = self.get_color("highlight")
        spins_triangle[0].set_color(spinDown)
        spins_triangle[1].set_color(spinUP)
        spins_triangle[2].set_color(spinDown)

        self.add(title, list[0], triangle, spins_triangle, spin_label)
        self.wait()

        self.next_slide()
        self.play(
            spins_triangle[1].animate.set_color(spinDown),
            spins_triangle[2].animate.set_color(spinUP),
            rate_functions=smooth,
        )
        self.add(list[1])
        self.wait()

        self.next_slide()
        self.remove(triangle, spins_triangle, spin_label)
        self.add(list[2])

        L = 4  # Rede L x L
        spacing = 0.9

        spins = {}
        vertices = VGroup()
        edges = VGroup()

        # 1. Criação dos sítios e atribuição do padrão Staggered
        for i in range(L):
            for j in range(L):
                # Posição centralizada
                pos = np.array(
                    [(j - (L - 1) / 2) * spacing, ((L - 1) / 2 - i) * spacing, 0]
                )

                # Verificação de paridade: (i + j) % 2
                is_up = (i + j) % 2 == 0
                color = spinUP if is_up else spinDown

                # Vértice no sítio
                circle = Circle(
                    radius=0.2,
                    color=WHITE,
                    fill_color=color,
                    fill_opacity=1,
                    stroke_width=1.5,
                )
                circle.move_to(pos)

                spins[(i, j)] = circle
                vertices.add(circle)

        # 2. Conexões de vizinhos mais próximos (Arestas da rede)
        for i in range(L):
            for j in range(L):
                if j + 1 < L:  # Vizinho à direita
                    edges.add(
                        Line(
                            spins[(i, j)].get_center(),
                            spins[(i, j + 1)].get_center(),
                            color=self.get_color("text"),
                            stroke_width=7,
                        )
                    )
                if i + 1 < L:  # Vizinho abaixo
                    edges.add(
                        Line(
                            spins[(i, j)].get_center(),
                            spins[(i + 1, j)].get_center(),
                            color=self.get_color("text"),
                            stroke_width=7,
                        )
                    )

        # Agrupa tudo
        lattice = VGroup(edges, vertices).center().shift(1.2 * DOWN + 1.5 * RIGHT)

        antiferromagnetic_text = (
            Text(
                "Antiferromagnetic interactions\n favour pairs anti-aligned",
                color=self.get_color("text"),
                font_size=self.FONT_SIZE_TEXT,
                font="Latin Modern Math",
            )
            .to_edge(LEFT)
            .shift(DOWN)
        )

        coupling_J1 = MathTex("J_{1}", color=self.get_color("text"))
        compare_coupling = MathTex(">", color=self.get_color("text"))
        coupling_J2 = MathTex("J_{2}", color=self.get_color("error"))
        couplings = (
            VGroup(coupling_J1, compare_coupling, coupling_J2)
            .arrange(RIGHT, buff=0.5)
            .next_to(antiferromagnetic_text, DOWN)
        )

        # Animação
        self.play(
            Create(edges),
            FadeIn(vertices, lag_ratio=0.05),
            FadeIn(antiferromagnetic_text),
            FadeIn(couplings[0]),
            run_time=1,
        )
        self.wait()

        # Highlight first-neighbours
        edges[10].set_color(self.get_color("error")).set_stroke_width(10)
        edges[9].set_color(self.get_color("error")).set_stroke_width(10)
        edges[3].set_color(self.get_color("error")).set_stroke_width(10)
        edges[7].set_color(self.get_color("error")).set_stroke_width(10)
        self.wait()

        # Add second-neighbours
        self.next_slide()
        # Restore
        edges[10].set_color(self.get_color("text")).set_stroke_width(7)
        edges[9].set_color(self.get_color("text")).set_stroke_width(7)
        edges[3].set_color(self.get_color("text")).set_stroke_width(7)
        edges[7].set_color(self.get_color("text")).set_stroke_width(7)

        J2_bonds = VGroup(
            Line(
                vertices[0],
                vertices[5],
                color=self.get_color("error"),
                buff=0.9,
                stroke_width=10,
            ),
            Line(
                vertices[2],
                vertices[5],
                color=self.get_color("error"),
                buff=0.9,
                stroke_width=10,
            ),
            Line(
                vertices[8],
                vertices[5],
                color=self.get_color("error"),
                buff=0.9,
                stroke_width=10,
            ),
            Line(
                vertices[10],
                vertices[5],
                color=self.get_color("error"),
                buff=0.9,
                stroke_width=10,
            ),
        )
        self.add(couplings[2], J2_bonds)

        J2_box = SurroundingRectangle(couplings[2], color=self.get_color("text"))
        frustrated_text = Text(
            "Frustrated",
            color=self.get_color("text"),
            font_size=self.FONT_SIZE_TEXT,
            font="Latin Modern Math",
        ).next_to(J2_box, DOWN)
        self.add(J2_box, frustrated_text)
        self.wait()

        self.next_slide()
        # phases
        self.add(list[3], couplings[1])
        phases = (
            MathTex(
                "&- \\text{Antiferromagnetic (AF)} \\\\ ",
                "&- \\text{Stripe antiferromagnetic (SAF)}",
                font_size=self.FONT_SIZE_EQ_TEXT,
                color=self.get_color("text"),
            )
            .to_edge(LEFT)
            .shift(0.3 * RIGHT)
        )
        self.remove(antiferromagnetic_text)
        self.add(phases[0])
        self.wait()

        self.next_slide()
        # J2 domain over J1
        compare_coupling2 = MathTex("<", color=self.get_color("text")).move_to(
            couplings[1].get_center()
        )
        self.play(
            Transform(couplings[1], compare_coupling2),
            J2_box.animate.move_to(couplings[0].get_center()),
            frustrated_text.animate.move_to(couplings[0].get_center() + 0.8 * DOWN),
        )
        for item in range(0, len(vertices)):
            is_up = (item) % 2 == 0
            color = spinUP if is_up else spinDown
            vertices[item].set_color(color)
        self.add(phases[1])
        self.wait()

        # Consequences of frustration
        self.next_slide()
        self.remove(
            phases[0],
            phases[1],
            couplings[0],
            couplings[1],
            couplings[2],
            frustrated_text,
            J2_box,
        )
        self.add(list[4])
        self.wait()
        consequences = (
            VGroup(
                Text(
                    "- Reduction of ordering temperature;",
                    font_size=self.FONT_SIZE_TEXT,
                    color=spinDown,
                ),
                Text(
                    "- Rich phase diagram;",
                    font_size=self.FONT_SIZE_TEXT,
                    color=self.get_color("secondary"),
                ),
            )
            .arrange(DOWN, aligned_edge=LEFT)
            .next_to(list, DOWN)
            .shift(1.5 * LEFT)
        )

        self.add(consequences[0])
        self.wait(0.5)

        for item in range(1, len(consequences)):
            self.next_slide()
            self.add(consequences[item])
            self.wait()
