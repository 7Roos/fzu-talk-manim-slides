# Cria a capa da apresentação do seminário
# Assumimos que CustomSlide é uma classe personalizada que estende Slide e está corretamente implementada.
# M. Roos, 27/09/2026

from manim import *
from components.custom_slide import CustomSlide
from components.custom_slide import CustomMovingCameraSlide
import random


class Cover(CustomMovingCameraSlide):
    def create_lab_logo_animation(self):
        """
        Creates and animates the laboratory's logo consisting of a hexagon with connected spinning particles.
        The animation sequence:
        1. Displays spinning circles at hexagon vertices with random colors
        2. Creates connection lines between the center circle and vertex circles
        3. Animates the laboratory's name text appearing alongside the logo
        The logo consists of:
        - A hexagonal outline
        - Circles at each vertex of the hexagon (representing spins)
        - A central circle connected to all vertex circles
        - Connection lines between the central circle and vertex circles
        - The "Lab TMC" text displayed next to the hexagon
        Returns:
            tuple: A tuple containing:
                - logo_group (VGroup): Contains the text and line elements of the logo
                - all_circles (VGroup): Contains all the circle elements representing spins
        """
        # Cores para os spins (círculos)
        # Star in "T=0" with all spins aligned
        # Later, add a function to randomly choose RED or BLUE for each spin
        spin_color = self.get_color("primary")
        self.spinUpDown = [
            self.get_color("line", category="timeline"),
            self.get_color("marker", category="timeline"),
        ]

        # Draw the hexagon
        radius = 1.2  # Raio do hexágono
        rotation_angle = PI / 2  # Rotação do hexágono por pi/2
        origin_hexagon = 2.12 * LEFT  # Centro do hexágono
        hexagon = RegularPolygon(
            n=6,
            radius=radius,
            color=self.get_color("text"),
            fill_opacity=0,
            stroke_width=10,
            stroke_color=self.get_color("text"),
        ).move_to(origin_hexagon)
        # Transform honeycomb into hexagon
        hexagon.rotate(rotation_angle)
        # self.add(hexagon)
        # self.play(Create(hexagon), run_time=2)
        # self.wait(1)
        # center_circle = Circle(radius=2, color=BLUE, fill_opacity=0.8)

        # Criar os círculos nos vértices do hexágono
        vertex_circles = []
        for i in range(6):
            angle = (
                i * TAU / 6
            )  # Divide o círculo em 6 partes com rotação adicional de pi/2
            # Divide the circle into 6 parts with additional rotation of pi/2 for transform honeycomb into hexagon
            angle = i * TAU / 6 + rotation_angle
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            spin_color = random.choice(self.spinUpDown)
            circle = Circle(
                radius=0.2, color=spin_color, fill_opacity=1, stroke_width=0
            ).move_to(origin_hexagon + [x, y, 0])
            vertex_circles.append(circle)

        # Adding the center circle
        spin_color = random.choice(self.spinUpDown)
        center_circle = Circle(
            radius=0.19, color=spin_color, fill_opacity=1, stroke_width=0
        ).move_to(origin_hexagon + [0, 0, 0])
        vertex_circles.append(center_circle)

        # Criar as linhas de conexão
        connection_lines = []
        for circle in vertex_circles:
            # Calculate direction from center to vertex
            start_point = center_circle.get_center()
            end_point = circle.get_center()

            # Skip the center circle itself
            if np.array_equal(start_point, end_point):
                continue

            # Calculate direction vector
            direction = end_point - start_point
            # calculates the Euclidean norm (also called the L2 norm or 2-norm) of a vector stored in the variable direction
            # || direction|| = sqrt(x^2 + y^2 + z^2)
            direction = direction / np.linalg.norm(direction)

            # Offset the start and end points by the circle radius
            start_point = start_point + direction * center_circle.radius
            end_point = (
                end_point - direction * circle.radius
            )  # Use the radius of the specific vertex circle

            # Determine color based on iteration index
            # Get current index from the loop (relative to vertex_circles)
            current_index = vertex_circles.index(circle)
            line_color = (
                self.get_color("axes", category="graph")
                if current_index % 2 == 1
                else self.get_color("text")
            )

            line = Line(
                start_point,
                end_point,
                stroke_width=7,
                color=line_color,
            )
            connection_lines.append(line)

        # Texto "Lab TMC"
        # Ensure the file exists at the specified path or update the path if necessary
        logo_text = SVGMobject("assets/logo_text.svg")  # Update path if needed
        logo_text.set_color(self.get_color("text"))
        logo_text.next_to(VGroup(*vertex_circles), RIGHT, buff=0.5)

        # Grupos para animação
        all_circles = VGroup(*vertex_circles)
        all_lines = VGroup(*connection_lines, hexagon)

        all_circles.set_z_index(1)  # Coloca os círculos acima do logo
        all_lines.set_z_index(0)  # Coloca as linhas abaixo do logo

        #shift
        all_circles.shift(0.5*UP)
        all_lines.shift(0.5*UP)
        logo_text.shift(0.5*UP)

        # Animação: entrada dos círculos em rotação
        ## 1. The circles enter with some rotation
        # self.play(SpiralIn(all_circles, angle=2 * PI), run_time=2) # Old version
        self.play(SpiralIn(all_circles), run_time=2)

        ## 2. The lines appear with the text growing next to them
        self.play(*[Create(line) for line in all_lines], GrowFromEdge(logo_text, LEFT))

        ## Retorna o grupo completo do logo para uso posterior
        logo_group = VGroup(logo_text, all_lines)
        return logo_group, all_circles

    def construct(self):
        # Configure o fundo chamando o método da classe base
        # self.setup_background(white=True)  # True para branco, False para preto
        # self.setup_slide_number()  # Opcional, se quiser numeração
        # In the future, add a function to initialize counter

        title = Text(
            "Frustrated Ising models",
            font="DejaVu Sans",
            weight=BOLD,
            font_size=50,
            color=self.get_color("title"),
        ).to_edge(UP)

        # Start with full black background
        self.add(title)

        # Watermarker logo lab
        logo_lab = ImageMobject("assets/logo_lab")
        logo_lab.set_opacity(0.1).shift(6 * RIGHT + 3 * DOWN)
        self.add(logo_lab)
        self.wait()
        self.next_slide()

        # Crie o logo com animação personalizada
        logo_group, all_circles = self.create_lab_logo_animation()
        self.add(logo_group)
        self.wait()

        advisor = (
            Text(
                "Advisors: prof. Dr. M. Schmidt and prof. RNDr. M. Žukovič",
                font="CMU Serif Upright Italic",
                slant=ITALIC,
                font_size=20,
                color=self.get_color("text"),
            )
            .to_edge(DOWN)
            .shift(0.8 * UP)
        )

        author = (
            Text(
                "by M. Roos",
                font="CMU Serif Upright Italic",
                slant=ITALIC,
                font_size=30,
                color=self.get_color("title"),
            )
            .next_to(advisor, UP)
            .shift(0.1 * UP)
        )

        universities = Text(
            "Federal University of Santa Maria (UFSM), Brazil \n University Pavol Jozef Šafárik (UPJŠ), Slovakia",
            line_spacing=1,
            font="CMU Serif Upright Italic",
            slant=ITALIC,
            font_size=20,
            color=self.get_color("text"),
        ).next_to(advisor, DOWN)

        # Grupos para animação
        ## Animate color of the spins, inducing a fluctuation with temperature
        ### Create animation to change colors randomly between RED and BLUE
        def random_color_animations():
            animations = []

            # Then randomize colors
            for circle in all_circles:
                new_color = random.choice(self.spinUpDown)
                animations.append(circle.animate.set_color(new_color))
            return animations

        ## Run the color change animation a few times to simulate thermal fluctuation
        ### Definir títulos e textos com opacidade inicial 0
        # title.set_opacity(0)
        advisor.set_opacity(0)
        author.set_opacity(0)
        universities.set_opacity(0)

        ### Adicionar elementos à cena com opacidade 0
        self.add(advisor, author, universities)

        ## Animações em paralelo - cores alternando e fade in simultâneo
        ## Velocidades diferentes com animação sincronizada
        # Crie uma sequência de animações de cor rápidas
        color_sequence = []
        total_color_animations = 12  # Total de alternâncias de cor (3 por fade step)

        for _ in range(total_color_animations):
            color_sequence.append(
                AnimationGroup(*random_color_animations(), run_time=0.2)
            )

        # Crie animações de fade que ocorrem em 4 etapas
        fade_sequence = []
        fade_steps = 4

        for step in range(fade_steps):
            opacity = (step + 1) / fade_steps
            fade_group = AnimationGroup(
                author.animate.set_opacity(opacity),
                advisor.animate.set_opacity(opacity),
                universities.animate.set_opacity(opacity),
                run_time=1,
            )
        fade_sequence.append(fade_group)

        # Criar uma sequência de cor que executa todas as animações de cor em ordem
        colors_succession = Succession(*color_sequence)

        # Criar uma sequência de fade que executa todas as animações de fade em ordem
        fade_succession = Succession(*fade_sequence)

        # Executar ambas as animações ao mesmo tempo, mas com suas próprias velocidades
        self.play(colors_succession, fade_succession)

        # Garantir que a opacidade final seja 1
        # title.set_opacity(1)
        # advisor.set_opacity(1)
        # author.set_opacity(1)
        all_circles.set_color(self.spinUpDown[0])
        all_circles[6].set_color(self.spinUpDown[1])  # Center circle
        self.wait(0.5)
