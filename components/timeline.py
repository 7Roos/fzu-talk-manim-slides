from cloup import Color
from manim import *

# from colour import Color
import os


class Timeline:
    """
    Uma linha do tempo vertical interativa que pode ser usada em vários slides. A linha permanece no lado esquerdo e destaca eventos históricos relevantes e personalidades associadas.
    """

    def __init__(self, scene, events, highlight_color=None, image_dir="assets"):
        """
        Inicializa a linha do tempo com eventos históricos.

        Args:
            scene: A cena Manim onde a linha será mostrada
            events: Dicionário dos eventos históricos {ano: {descrição, image}}
            highlight_color: Cor usada para destacar o evento atual
            image_dir: Diretório onde as imagens estão armazenadas
        """
        self.scene = scene
        # Obter tamanhos de fonte da cena
        if hasattr(scene, "FONT_SIZE_HEADING"):
            self.font_size_heading = scene.FONT_SIZE_HEADING
            self.font_size_text = scene.FONT_SIZE_TEXT
        else:
            # Valores padrão caso a cena não tenha esses atributos
            self.font_size_heading = 32
            self.font_size_text = 24

        self.events = dict(sorted(events.items()))  # Garantir ordem cronológica

        # Diretório onde as imagens estão armazenadas
        # Se o diretório não existir, ele será criado
        # e o usuário será solicitado a adicionar as imagens
        # dos cientistas
        # para que o código funcione corretamente
        # e o usuário não tenha que se preocupar com isso
        # se o diretório não existir.
        self.image_dir = image_dir
        # Verificar se o diretório de imagens existe
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
            print(
                f"Diretório de imagens '{image_dir}' criado. Por favor, adicione as imagens dos cientistas."
            )

        # Usar cores da paleta se disponível
        if hasattr(scene, "get_color"):
            self.highlight_color = highlight_color or scene.get_color(
                "highlight", "timeline"
            )
            line_color = scene.get_color("line", "timeline")
            marker_color = scene.get_color("marker", "timeline")
            text_color = scene.get_color("text", "timeline")
        else:
            # Fallback para cores padrão
            self.highlight_color = highlight_color or YELLOW
            line_color = WHITE
            marker_color = WHITE
            text_color = WHITE

        # Criar linha principal com cores da paleta
        self.line = Line(
            start=3.5 * UP + 6.9 * LEFT,
            end=3.5 * DOWN + 6.9 * LEFT,
            color=line_color,
            stroke_width=5,
        )

        # Criar marcadores e textos de anos
        self.year_marks = VGroup()
        self.year_labels = VGroup()
        self.event_descriptions = VGroup()
        self.event_images = Group()

        # Calcular posições para distribuir uniformemente na linha
        years = list(self.events.keys())
        num_events = len(years)

        for i, (year, event_data) in enumerate(self.events.items()):
            # Extrair descrição e caminho da imagem
            description = (
                event_data["description"]
                if isinstance(event_data, dict)
                else event_data
            )
            image_path = (
                event_data["image"] if isinstance(event_data, dict) else event_data
            )

            # Calcular posição vertical distribuída uniformemente
            t = i / (num_events - 1) if num_events > 1 else 0
            position = self.line.point_from_proportion(
                t
            )  # Gets the point at a proportion along the path of the VMobject

            # Criar marcador (um círculo preto sólido com borda branca)
            mark = Circle(
                radius=0.08,  # Ligeiramente maior para garantir que cubra a linha
                stroke_color=marker_color,  # Borda branca
                stroke_width=5,
                fill_color=BLACK,  # Interior preto
                fill_opacity=1,  # Totalmente opaco para esconder a linha
            ).move_to(position)

            # Criar texto do ano
            # Outras boas opções de fontes:
            # Antykwa Torunska, Antykwa Torunska Condensed
            # Berenis ADF Pro
            # Outra opção para números: Berenis ADF Pro SC
            year_text = Text(
                str(year),
                font="Berenis ADF Pro",
                font_size=scene.FONT_SIZE_HEADING,
                weight=BOLD,
                color=text_color,
            ).next_to(mark, RIGHT, buff=0.2)
            year_text.set_opacity(0)  # Inicialmente invisível

            # Criar descrição do evento (inicialmente invisível)
            event_text = (
                Text(
                    description,
                    font="CMU Classical Serif",
                    font_size=scene.FONT_SIZE_HEADING,
                    color=text_color,
                )
                .next_to(year_text, RIGHT, buff=0.4)
                .align_to(year_text, UP)
            )
            event_text.set_opacity(0)

            # Determinar se o evento está na metade inferior da timeline
            # Se estiver, posicionar a imagem acima da descrição para evitar corte
            is_bottom_half = i >= (num_events / 2)

            try:
                full_path = os.path.join(self.image_dir, image_path)
                # Se a imagem existir, carregá-la e posicioná-la
                # abaixo da descrição do evento, inicialmente invisível.
                if os.path.exists(full_path):
                    # Ajuste a escala conforme necessário
                    image = ImageMobject(full_path).scale(1)

                    if is_bottom_half:
                        # Posicionar imagem acima da descrição do evento
                        image.next_to(event_text, UP, buff=0.2).align_to(
                            event_text, LEFT
                        )
                        image.shift(0.2 * LEFT)  # Ajuste a posição horizontal
                    else:
                        # Posicionamento original: abaixo da descrição do evento
                        image.next_to(event_text, DOWN, buff=0.2).align_to(
                            event_text, LEFT
                        )
                        image.shift(0.2 * LEFT)  # Ajuste a posição horizontal

                    image.set_opacity(
                        0
                    )  # A opacidade será controlada para o grupo todo
                else:
                    # Se a imagem não existir, criar um retângulo cinza com texto de aviso.
                    # e definir a opacidade como 0 para que não apareça na cena.
                    print(f"Aviso: Imagem {full_path} não encontrada.")
                    image = Rectangle(height=1, width=0.8, color=GRAY, fill_opacity=0.3)

                    if is_bottom_half:
                        image.next_to(event_text, UP, buff=0.2).align_to(
                            event_text, LEFT
                        )
                    else:
                        image.next_to(event_text, DOWN, buff=0.2).align_to(
                            event_text, LEFT
                        )

                    missing_text = Text(
                        "Imagem não\nencontrada", font_size=10, color=GRAY
                    )
                    missing_text.move_to(image)
                    image = VGroup(image, missing_text)
                    image.set_opacity(0)
            except Exception as e:
                print(f"Erro ao carregar imagem para o ano {year}: {e}")
                image = Rectangle(height=1, width=0.8, color=RED, fill_opacity=0.3)

                # Aplicar a mesma lógica de posicionamento para casos de erro
                is_bottom_half = i >= (num_events / 2)
                if is_bottom_half:
                    image.next_to(event_text, UP, buff=0.2).align_to(event_text, LEFT)
                else:
                    image.next_to(event_text, DOWN, buff=0.2).align_to(event_text, LEFT)

                image.set_opacity(0)

            # Adicionar aos grupos
            self.year_marks.add(mark)
            self.year_labels.add(year_text)
            self.event_descriptions.add(event_text)
            self.event_images.add(image)

    def add_to_scene(self):
        """Adiciona a linha do tempo à cena com animação em sequência"""
        # Primeiro, cria apenas a linha principal
        self.scene.play(Create(self.line), run_time=1, rate_func=smooth)

        # Em seguida, adiciona todos os marcadores de anos em uma única animação sequencial (de baixo para cima)
        animations = [FadeIn(mark, scale=1.2) for mark in self.year_marks[::-1]]
        self.scene.play(
            Succession(*animations, lag_ratio=0.5),
            run_time=0.1
            * len(self.year_marks),  # Tempo proporcional ao número de marcadores
        )

        # Adicione as descrições e imagens à cena (inicialmente invisíveis)
        self.scene.add(self.event_descriptions, self.event_images)

    def highlight_event(self, year, animate=True):
        """Destaca um evento específico na linha do tempo, mostrando imagem e descrição"""
        if year not in self.events:
            print(f"Ano {year} não encontrado na linha do tempo")
            return

        # Encontrar índice do ano
        years = list(self.events.keys())
        idx = years.index(year)

        # Resetar todos os destaques
        for i in range(len(years)):
            mark = self.year_marks[i]
            year_text = self.year_labels[i]
            event_text = self.event_descriptions[i]
            event_image = self.event_images[i]

            if i == idx:
                # Destacar o evento selecionado
                if animate:
                    self.scene.play(
                        Succession(
                            mark.animate.set_color(self.highlight_color).scale(1.2),
                            year_text.animate.set_opacity(1)
                            .set_color(self.highlight_color)
                            .scale(1.2),
                            event_text.animate.set_opacity(1),
                            event_image.animate.set_opacity(1),
                            lag_ratio=0.5,
                        ),
                        run_time=1,
                    )

                    # Esperar um pouco e retirar o texto do evento para limpar a tela
                    self.scene.wait(4)
                    self.scene.play(
                        FadeOut(event_text),
                        FadeOut(event_image),
                    )
                    self.scene.wait(0.5)
                else:
                    mark.set_color(self.highlight_color).scale(1.5)
                    year_text.set_color(self.highlight_color).scale(1.2)
                    event_text.set_opacity(1)
                    event_image.animate.set_opacity(1)
            else:
                # Verificar se é o evento imediatamente anterior (i == idx-1)
                if i == idx - 1:
                    # Marcar apenas o evento anterior como GRAY
                    if animate:
                        self.scene.play(
                            mark.animate.set_color(GRAY).scale(1.0),
                            year_text.animate.set_color(GRAY).scale(1.0),
                            run_time=0.3,
                        )
                    else:
                        mark.set_color(GRAY).scale(1.0)
                        year_text.set_color(GRAY).scale(1.0)

                        # Mostrar cada elemento do grupo imagem separadamente
                        for submob in event_image:
                            submob.set_opacity(1)
